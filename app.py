from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from datetime import datetime
import re
from demo_data import get_demo_weather_data
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'YOUR_OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini
if GEMINI_API_KEY:
    print(f"Configuring Gemini with API key: {GEMINI_API_KEY[:10]}...")
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-pro')
    print("Gemini model configured successfully")
else:
    print("No Gemini API key found")
    gemini_model = None

# Weather data storage
weather_data = {}
DEMO_MODE = OPENWEATHER_API_KEY == 'YOUR_OPENWEATHER_API_KEY'

@app.route('/')
def index():
    """Serve the main weather dashboard page"""
    return render_template('index.html')

@app.route('/api/weather/<city>')
def get_weather_data(city):
    """Get weather data for a specific city"""
    try:
        if DEMO_MODE:
            # Use demo data when no API key is configured
            demo_data = get_demo_weather_data(city)
            weather_data[city] = {
                'current': demo_data['current'],
                'forecast': demo_data['forecast'],
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify({
                'success': True,
                'current': demo_data['current'],
                'forecast': demo_data['forecast'],
                'demo_mode': True
            })
        
        # Fetch current weather
        current_url = f"{OPENWEATHER_BASE_URL}/weather"
        current_params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        current_response = requests.get(current_url, params=current_params)
        current_response.raise_for_status()
        current_data = current_response.json()
        
        # Fetch 5-day forecast
        forecast_url = f"{OPENWEATHER_BASE_URL}/forecast"
        forecast_params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        forecast_response = requests.get(forecast_url, params=forecast_params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Store data for chatbot
        weather_data[city] = {
            'current': current_data,
            'forecast': forecast_data,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'current': current_data,
            'forecast': forecast_data,
            'demo_mode': False
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Could not fetch weather data for {city}. Please check the city name and try again.'
        }), 400

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Handle chatbot queries"""
    try:
        data = request.get_json()
        message = data.get('message', '').lower()
        city = data.get('city', 'London')
        
        # Get weather data for the city
        city_data = weather_data.get(city)
        if not city_data:
            return jsonify({
                'success': False,
                'response': f"I don't have weather data for {city}. Please search for a city first."
            })
        
        current_data = city_data['current']
        forecast_data = city_data['forecast']
        
        # Process the message and generate response
        response = process_chat_message(message, current_data, forecast_data)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'response': f"Sorry, I encountered an error: {str(e)}"
        }), 500

def process_chat_message(message, current_data, forecast_data):
    """Process chat messages and generate intelligent responses"""
    
    # Temperature queries
    if any(word in message for word in ['temperature', 'temp']):
        if any(word in message for word in ['current', 'now']):
            temp = round(current_data['main']['temp'])
            return f"The current temperature is {temp}°C."
        elif any(word in message for word in ['highest', 'max']):
            temps = [item['main']['temp'] for item in forecast_data['list']]
            max_temp = round(max(temps))
            return f"The highest temperature in the forecast is {max_temp}°C."
        elif any(word in message for word in ['lowest', 'min']):
            temps = [item['main']['temp'] for item in forecast_data['list']]
            min_temp = round(min(temps))
            return f"The lowest temperature in the forecast is {min_temp}°C."
        elif any(word in message for word in ['average', 'avg']):
            temps = [item['main']['temp'] for item in forecast_data['list']]
            avg_temp = round(sum(temps) / len(temps))
            return f"The average temperature is {avg_temp}°C."
        else:
            current_temp = round(current_data['main']['temp'])
            temps = [item['main']['temp'] for item in forecast_data['list']]
            max_temp = round(max(temps))
            min_temp = round(min(temps))
            return f"The current temperature is {current_temp}°C. The forecast shows temperatures ranging from {min_temp}°C to {max_temp}°C."
    
    # Humidity queries
    if 'humidity' in message:
        if any(word in message for word in ['current', 'now']):
            humidity = current_data['main']['humidity']
            return f"The current humidity is {humidity}%."
        elif any(word in message for word in ['average', 'avg']):
            humidities = [item['main']['humidity'] for item in forecast_data['list']]
            avg_humidity = round(sum(humidities) / len(humidities))
            return f"The average humidity is {avg_humidity}%."
        else:
            current_humidity = current_data['main']['humidity']
            humidities = [item['main']['humidity'] for item in forecast_data['list']]
            avg_humidity = round(sum(humidities) / len(humidities))
            return f"The current humidity is {current_humidity}% and the average humidity is {avg_humidity}%."
    
    # Wind queries
    if 'wind' in message:
        wind_speed = round(current_data['wind']['speed'] * 3.6)  # Convert m/s to km/h
        return f"The current wind speed is {wind_speed} km/h."
    
    # Weather condition queries
    if any(word in message for word in ['weather', 'condition']):
        weather_desc = current_data['weather'][0]['description']
        return f"The current weather is {weather_desc}."
    
    # Visibility queries
    if 'visibility' in message:
        visibility_km = round(current_data['visibility'] / 1000, 1)
        return f"The current visibility is {visibility_km} km."
    
    # Rain queries
    if any(word in message for word in ['rain', 'precipitation']):
        weather_desc = current_data['weather'][0]['description'].lower()
        if 'rain' in weather_desc:
            return f"Yes, there is rain in the forecast. The current conditions show {current_data['weather'][0]['description']}."
        else:
            return f"No rain is currently forecasted. The weather is {current_data['weather'][0]['description']}."
    
    # General weather summary
    if any(word in message for word in ['summary', 'overview']):
        city_name = current_data['name']
        country = current_data['sys']['country']
        temp = round(current_data['main']['temp'])
        weather_desc = current_data['weather'][0]['description']
        humidity = current_data['main']['humidity']
        wind_speed = round(current_data['wind']['speed'] * 3.6)
        
        return f"Here's a weather summary for {city_name}, {country}: Current temperature is {temp}°C with {weather_desc}. Humidity is {humidity}% and wind speed is {wind_speed} km/h."
    
    # Help
    if any(word in message for word in ['help', 'what can you do']):
        return "I can help you with weather information! Ask me about temperature (current, highest, lowest, average), humidity, wind speed, weather conditions, visibility, rain, or request a weather summary."
    
    # Default response
    return "I'm here to help with weather information! You can ask me about temperature, humidity, wind, weather conditions, or request a summary. What would you like to know?"

def process_advanced_chat_message(query, weather_data):
    """Enhanced rule-based processing for complex weather queries"""
    query_lower = query.lower()
    
    # Extract weather information from the data
    if not weather_data:
        return "I don't have weather data available. Please search for a city first."
    
    # Parse the weather data to extract information
    lines = weather_data.split('\n')
    current_weather = {}
    forecast_days = []
    temp_stats = {}
    
    # Parse current weather
    for line in lines:
        if 'Current Weather in' in line:
            city_info = line.split('Current Weather in ')[1].split(':')[0]
        elif 'Temperature:' in line:
            temp_match = re.search(r'(\d+)°C', line)
            if temp_match:
                current_weather['temp'] = int(temp_match.group(1))
        elif 'Weather:' in line:
            weather_match = re.search(r'Weather: (.+)', line)
            if weather_match:
                current_weather['weather'] = weather_match.group(1)
        elif 'Humidity:' in line:
            humidity_match = re.search(r'(\d+)%', line)
            if humidity_match:
                current_weather['humidity'] = int(humidity_match.group(1))
    
    # Parse forecast
    in_forecast = False
    for line in lines:
        if '5-Day Forecast:' in line:
            in_forecast = True
            continue
        elif in_forecast and line.strip() and ':' in line and '°C' in line:
            # Parse forecast line like "Mon (Aug 5): 20°C, clear sky, 60% humidity"
            parts = line.split(': ')
            if len(parts) == 2:
                day_info = parts[0]
                weather_info = parts[1]
                
                temp_match = re.search(r'(\d+)°C', weather_info)
                weather_match = re.search(r', (.+?),', weather_info)
                humidity_match = re.search(r'(\d+)% humidity', weather_info)
                
                if temp_match:
                    forecast_days.append({
                        'day': day_info,
                        'temp': int(temp_match.group(1)),
                        'weather': weather_match.group(1) if weather_match else 'unknown',
                        'humidity': int(humidity_match.group(1)) if humidity_match else 0
                    })
    
    # Parse temperature statistics
    for line in lines:
        if 'Highest:' in line:
            temp_match = re.search(r'(\d+)°C', line)
            if temp_match:
                temp_stats['highest'] = int(temp_match.group(1))
        elif 'Lowest:' in line:
            temp_match = re.search(r'(\d+)°C', line)
            if temp_match:
                temp_stats['lowest'] = int(temp_match.group(1))
        elif 'Average:' in line:
            temp_match = re.search(r'(\d+)°C', line)
            if temp_match:
                temp_stats['average'] = int(temp_match.group(1))
    
    # Process specific query types
    if any(word in query_lower for word in ['umbrella', 'rain', 'precipitation']):
        rainy_days = [day for day in forecast_days if any(word in day['weather'].lower() for word in ['rain', 'drizzle', 'shower'])]
        if rainy_days:
            days_list = ', '.join([day['day'] for day in rainy_days])
            return f"Yes, you might need an umbrella! I see rain in the forecast for: {days_list}. The weather shows {len(rainy_days)} rainy days this week."
        else:
            return "No, you probably don't need an umbrella this week. The forecast shows clear or partly cloudy conditions with no significant rain expected."
    
    elif 'summarize' in query_lower or 'summary' in query_lower:
        if forecast_days:
            summary = f"Here's a 5-day weather summary: "
            for day in forecast_days:
                summary += f"{day['day']}: {day['temp']}°C, {day['weather']}. "
            return summary
        else:
            return "I can't provide a detailed summary without forecast data. Please search for a city first."
    
    elif any(word in query_lower for word in ['outdoor', 'activities', 'best day']):
        # Find the day with the best weather (sunny, warm, low humidity)
        best_day = None
        best_score = -1
        
        for day in forecast_days:
            score = 0
            # Prefer sunny weather
            if 'clear' in day['weather'].lower() or 'sunny' in day['weather'].lower():
                score += 3
            # Prefer moderate temperatures (15-25°C)
            if 15 <= day['temp'] <= 25:
                score += 2
            # Prefer lower humidity
            if day['humidity'] < 70:
                score += 1
            
            if score > best_score:
                best_score = score
                best_day = day
        
        if best_day:
            return f"The best day for outdoor activities looks like {best_day['day']} with {best_day['temp']}°C and {best_day['weather']}. It has comfortable conditions for outdoor activities."
        else:
            return "I can't determine the best day without detailed forecast data. Please search for a city first."
    
    elif any(word in query_lower for word in ['average', 'highest', 'temperature']):
        if temp_stats:
            response = f"Temperature statistics: "
            if 'highest' in temp_stats:
                response += f"Highest: {temp_stats['highest']}°C. "
            if 'average' in temp_stats:
                response += f"Average: {temp_stats['average']}°C. "
            if 'lowest' in temp_stats:
                response += f"Lowest: {temp_stats['lowest']}°C. "
            return response
        else:
            return "I can't provide temperature statistics without forecast data. Please search for a city first."
    
    elif 'pack' in query_lower or 'trip' in query_lower:
        if temp_stats and current_weather:
            suggestions = []
            if temp_stats.get('highest', 0) > 25:
                suggestions.append("light clothing")
            if temp_stats.get('lowest', 0) < 15:
                suggestions.append("a jacket or sweater")
            if any('rain' in day['weather'].lower() for day in forecast_days):
                suggestions.append("an umbrella or raincoat")
            if current_weather.get('humidity', 0) > 70:
                suggestions.append("moisture-wicking clothes")
            
            if suggestions:
                return f"Based on the weather forecast, you should pack: {', '.join(suggestions)}. The temperature will range from {temp_stats.get('lowest', 'unknown')}°C to {temp_stats.get('highest', 'unknown')}°C."
            else:
                return "The weather looks mild and comfortable. Pack regular clothing suitable for the current season."
        else:
            return "I can't provide packing suggestions without detailed weather data. Please search for a city first."
    
    elif 'rain more than' in query_lower or 'rainy days' in query_lower:
        rainy_days = [day for day in forecast_days if any(word in day['weather'].lower() for word in ['rain', 'drizzle', 'shower'])]
        rainy_count = len(rainy_days)
        
        # Extract number from query (e.g., "more than 3 times")
        number_match = re.search(r'more than (\d+)', query_lower)
        if number_match:
            threshold = int(number_match.group(1))
            if rainy_count > threshold:
                return f"Yes, it will rain more than {threshold} times this week. I count {rainy_count} rainy days in the forecast."
            else:
                return f"No, it won't rain more than {threshold} times this week. I count {rainy_count} rainy days in the forecast."
        else:
            return f"There are {rainy_count} rainy days in the forecast this week."
    
    elif 'compare' in query_lower and 'last week' in query_lower:
        return "I can't compare to last week's weather as I only have current forecast data. This feature would require historical weather data integration."
    
    else:
        # Fallback to basic weather info
        if current_weather:
            return f"Current weather: {current_weather.get('temp', 'unknown')}°C, {current_weather.get('weather', 'unknown conditions')}. Humidity: {current_weather.get('humidity', 'unknown')}%."
        else:
            return "I can help with weather information! Try asking about temperature, rain, outdoor activities, or packing suggestions."

@app.route('/chat', methods=['POST'])
def chat_with_gemini():
    """Handle chat requests using Gemini LLM"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        weather_data = data.get('weatherData', '')
        
        if not query:
            return jsonify({
                'success': False,
                'response': 'Please provide a query.'
            }), 400
        
        if not gemini_model:
            print("Gemini model is not available")
            return jsonify({
                'success': False,
                'response': 'Gemini API is not configured. Please check your API key.'
            }), 500
        
        print(f"Attempting to use Gemini for query: {query[:50]}...")
        
        # Create context for Gemini
        context = f"""
        You are a helpful weather assistant. A user is asking about weather information.
        
        Weather Data Summary:
        {weather_data}
        
        User Question: {query}
        
        Please provide a helpful, friendly, and concise response based on the weather data provided. 
        Focus on being practical and actionable. If the weather data doesn't contain enough information 
        to answer the question, politely say so.
        
        Keep your response conversational and under 150 words.
        """
        
        # Generate response using Gemini
        try:
            print("Calling Gemini API...")
            response = gemini_model.generate_content(context)
            print("Gemini API call successful")
            return jsonify({
                'success': True,
                'response': response.text
            })
        except Exception as gemini_error:
            # Fallback to enhanced rule-based responses if Gemini fails
            print(f"Gemini error: {gemini_error}")
            return jsonify({
                'success': False,
                'response': process_advanced_chat_message(query, weather_data)
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'response': f'Sorry, I encountered an error: {str(e)}'
        }), 500

@app.route('/api/cities')
def get_cities():
    """Get a list of popular cities for suggestions"""
    cities = [
        'London', 'New York', 'Tokyo', 'Paris', 'Sydney', 'Mumbai', 'Beijing',
        'Berlin', 'Rome', 'Madrid', 'Amsterdam', 'Vienna', 'Prague', 'Budapest',
        'Warsaw', 'Stockholm', 'Oslo', 'Copenhagen', 'Helsinki', 'Reykjavik'
    ]
    return jsonify(cities)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🌤️ Weather Dashboard with Python Chatbot")
    print("=" * 50)
    print(f"OpenWeather API Key: {'✅ Set' if OPENWEATHER_API_KEY != 'YOUR_OPENWEATHER_API_KEY' else '❌ Not Set'}")
    print("To set your API key, either:")
    print("1. Set the OPENWEATHER_API_KEY environment variable")
    print("2. Edit the OPENWEATHER_API_KEY variable in app.py")
    print("\nStarting server...")
    print("Access the dashboard at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 