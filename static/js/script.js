// Weather data storage
let currentWeatherData = null;
let forecastData = null;
let currentCity = 'London';

// DOM Elements
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const chatbotToggle = document.getElementById('chatbotToggle');
const chatbot = document.getElementById('chatbot');
const closeChatbot = document.getElementById('closeChatbot');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendMessage = document.getElementById('sendMessage');

// Weather display elements
const cityName = document.getElementById('cityName');
const dateTime = document.getElementById('dateTime');
const temperature = document.getElementById('temperature');
const weatherIcon = document.getElementById('weatherIcon');
const weatherDesc = document.getElementById('weatherDesc');
const humidity = document.getElementById('humidity');
const windSpeed = document.getElementById('windSpeed');
const visibility = document.getElementById('visibility');
const forecastContainer = document.getElementById('forecastContainer');
const maxTemp = document.getElementById('maxTemp');
const minTemp = document.getElementById('minTemp');
const avgTemp = document.getElementById('avgTemp');
const avgHumidity = document.getElementById('avgHumidity');

// Event Listeners
searchBtn.addEventListener('click', handleSearch);
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSearch();
});

chatbotToggle.addEventListener('click', toggleChatbot);
closeChatbot.addEventListener('click', toggleChatbot);
sendMessage.addEventListener('click', handleChatMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleChatMessage();
});

// Initialize with default city
document.addEventListener('DOMContentLoaded', () => {
    getWeatherData('London');
});

// Search functionality
async function handleSearch() {
    const city = cityInput.value.trim();
    if (city) {
        await getWeatherData(city);
        cityInput.value = '';
    }
}

// Fetch weather data from Python backend
async function getWeatherData(city) {
    try {
        // Show loading state
        showLoading(true);
        
        // Fetch weather data from Python backend
        const response = await fetch(`/api/weather/${encodeURIComponent(city)}`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'City not found');
        }
        
        currentWeatherData = data.current;
        forecastData = data.forecast;
        currentCity = city;
        
        // Update UI
        updateCurrentWeather();
        updateForecast();
        updateStatistics();
        
        // Add bot message about new data
        addBotMessage(`I've updated the weather data for ${city}. Ask me anything about the current conditions or forecast!`);
        
    } catch (error) {
        console.error('Error fetching weather data:', error);
        addBotMessage(`Sorry, I couldn't find weather data for "${city}". Please try a different city name.`);
    } finally {
        showLoading(false);
    }
}

// Update current weather display
function updateCurrentWeather() {
    if (!currentWeatherData) return;
    
    const data = currentWeatherData;
    
    cityName.textContent = data.name + ', ' + data.sys.country;
    dateTime.textContent = new Date().toLocaleString();
    temperature.textContent = Math.round(data.main.temp);
    weatherDesc.textContent = data.weather[0].description;
    humidity.textContent = data.main.humidity;
    windSpeed.textContent = Math.round(data.wind.speed * 3.6); // Convert m/s to km/h
    visibility.textContent = (data.visibility / 1000).toFixed(1);
    
    // Update weather icon
    const iconCode = data.weather[0].icon;
    weatherIcon.className = getWeatherIconClass(iconCode);
}

// Update forecast display
function updateForecast() {
    if (!forecastData) return;
    
    forecastContainer.innerHTML = '';
    
    // Group forecast by day and get daily data
    const dailyData = groupForecastByDay(forecastData.list);
    
    dailyData.forEach(day => {
        const card = document.createElement('div');
        card.className = 'forecast-card';
        
        const date = new Date(day.dt * 1000);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        const temp = Math.round(day.main.temp);
        const iconCode = day.weather[0].icon;
        
        card.innerHTML = `
            <h4>${dayName}</h4>
            <div class="weather-icon">
                <i class="${getWeatherIconClass(iconCode)}"></i>
            </div>
            <div class="temp">${temp}°C</div>
            <p>${day.weather[0].description}</p>
        `;
        
        forecastContainer.appendChild(card);
    });
}

// Update statistics
function updateStatistics() {
    if (!forecastData) return;
    
    const temps = forecastData.list.map(item => item.main.temp);
    const humidities = forecastData.list.map(item => item.main.humidity);
    
    const maxTempValue = Math.round(Math.max(...temps));
    const minTempValue = Math.round(Math.min(...temps));
    const avgTempValue = Math.round(temps.reduce((a, b) => a + b, 0) / temps.length);
    const avgHumidityValue = Math.round(humidities.reduce((a, b) => a + b, 0) / humidities.length);
    
    maxTemp.textContent = maxTempValue;
    minTemp.textContent = minTempValue;
    avgTemp.textContent = avgTempValue;
    avgHumidity.textContent = avgHumidityValue;
}

// Group forecast data by day
function groupForecastByDay(forecastList) {
    const dailyData = {};
    
    forecastList.forEach(item => {
        const date = new Date(item.dt * 1000);
        const day = date.toDateString();
        
        if (!dailyData[day]) {
            dailyData[day] = item;
        }
    });
    
    return Object.values(dailyData);
}

// Get weather icon class based on OpenWeather icon code
function getWeatherIconClass(iconCode) {
    const iconMap = {
        '01d': 'fas fa-sun',
        '01n': 'fas fa-moon',
        '02d': 'fas fa-cloud-sun',
        '02n': 'fas fa-cloud-moon',
        '03d': 'fas fa-cloud',
        '03n': 'fas fa-cloud',
        '04d': 'fas fa-cloud',
        '04n': 'fas fa-cloud',
        '09d': 'fas fa-cloud-rain',
        '09n': 'fas fa-cloud-rain',
        '10d': 'fas fa-cloud-sun-rain',
        '10n': 'fas fa-cloud-moon-rain',
        '11d': 'fas fa-bolt',
        '11n': 'fas fa-bolt',
        '13d': 'fas fa-snowflake',
        '13n': 'fas fa-snowflake',
        '50d': 'fas fa-smog',
        '50n': 'fas fa-smog'
    };
    
    return iconMap[iconCode] || 'fas fa-cloud';
}

// Chatbot functionality
function toggleChatbot() {
    chatbot.classList.toggle('active');
}

function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function handleChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    addUserMessage(message);
    chatInput.value = '';
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing';
    typingDiv.innerHTML = '<p>🤖 Thinking...</p>';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        // Use Gemini for intelligent responses
        const response = await chatWithGemini(message);
        
        // Remove typing indicator
        chatMessages.removeChild(typingDiv);
        
        // Add bot response
        addBotMessage(response);
        
    } catch (error) {
        // Remove typing indicator
        chatMessages.removeChild(typingDiv);
        
        console.error('Error sending message to chatbot:', error);
        
        // Try fallback to original chatbot
        try {
            const fallbackResponse = await fetch('/api/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    city: currentCity
                })
            });
            
            const fallbackData = await fallbackResponse.json();
            if (fallbackData.success) {
                addBotMessage(fallbackData.response);
            } else {
                // If the original chatbot also fails, show a helpful message
                addBotMessage('I\'m having trouble processing your request right now. Try asking a simple weather question like "What is the temperature?" or "What is the humidity?"');
            }
        } catch (fallbackError) {
            addBotMessage('Sorry, I encountered an error. Please try again.');
        }
    }
}

// Loading state
function showLoading(show) {
    const elements = [temperature, humidity, windSpeed, visibility];
    elements.forEach(el => {
        if (show) {
            el.textContent = '--';
        }
    });
}

// Generate weather summary for Gemini
function generateWeatherSummary() {
    if (!currentWeatherData || !forecastData) {
        return 'No weather data available.';
    }
    
    const current = currentWeatherData;
    const forecast = forecastData;
    
    // Current weather summary
    let summary = `Current Weather in ${current.name}, ${current.sys.country}:\n`;
    summary += `- Temperature: ${Math.round(current.main.temp)}°C (feels like ${Math.round(current.main.feels_like)}°C)\n`;
    summary += `- Weather: ${current.weather[0].description}\n`;
    summary += `- Humidity: ${current.main.humidity}%\n`;
    summary += `- Wind Speed: ${Math.round(current.wind.speed * 3.6)} km/h\n`;
    summary += `- Visibility: ${Math.round(current.visibility / 1000)} km\n`;
    summary += `- Pressure: ${current.main.pressure} hPa\n\n`;
    
    // 5-day forecast summary
    summary += `5-Day Forecast:\n`;
    const dailyData = groupForecastByDay(forecast.list);
    
    dailyData.forEach((day, index) => {
        const date = new Date(day.dt * 1000);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        
        summary += `${dayName} (${dateStr}): ${Math.round(day.main.temp)}°C, ${day.weather[0].description}, ${day.main.humidity}% humidity\n`;
    });
    
    // Temperature statistics
    const temps = forecast.list.map(item => item.main.temp);
    const maxTemp = Math.round(Math.max(...temps));
    const minTemp = Math.round(Math.min(...temps));
    const avgTemp = Math.round(temps.reduce((a, b) => a + b, 0) / temps.length);
    
    summary += `\nTemperature Statistics:\n`;
    summary += `- Highest: ${maxTemp}°C\n`;
    summary += `- Lowest: ${minTemp}°C\n`;
    summary += `- Average: ${avgTemp}°C\n`;
    
    return summary;
}

// Chat with Gemini LLM
async function chatWithGemini(query) {
    try {
        const weatherSummary = generateWeatherSummary();
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                weatherData: weatherSummary
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.response;
        } else {
            throw new Error(data.response || 'Unknown error');
        }
        
    } catch (error) {
        console.error('Error chatting with Gemini:', error);
        throw error;
    }
}

// Error handling
function showError(message) {
    addBotMessage(`Error: ${message}`);
} 