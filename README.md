# Weather Dashboard with AI Chatbot Integration

A modern, responsive weather dashboard that displays current weather conditions, 5-day forecasts, and includes an intelligent AI chatbot assistant powered by Google Gemini that can answer natural language questions about weather data.

## 🌟 Features

### Weather Display
- **Current Weather**: Real-time temperature, humidity, wind speed, visibility, and weather conditions
- **5-Day Forecast**: Daily weather predictions with temperature and conditions
- **Weather Statistics**: Temperature ranges, averages, and humidity statistics
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

### AI-Powered Chatbot Assistant
- **Google Gemini Integration**: Advanced AI responses using the Gemini 1.5 Pro model
- **Natural Language Processing**: Understands complex weather queries in plain English
- **Context-Aware Responses**: Provides intelligent answers based on current weather data
- **Fallback System**: Gracefully falls back to rule-based responses if AI is unavailable
- **Typing Indicators**: Shows when the AI is processing your request

## 🤖 AI Chatbot Capabilities

The chatbot can answer questions like:
- "Do I need an umbrella this week?"
- "Summarize the next 5 days' weather."
- "What day is best for outdoor activities?"
- "Give me the average and highest temperatures this week."
- "Based on this week's weather, what should I pack for a trip?"
- "Will it rain more than 3 times this week?"
- "What's the temperature right now?"
- "How humid is it today?"
- "What's the wind speed?"

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- OpenWeather API key (optional - demo mode available)
- Google Gemini API key (optional - fallback available)

### Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure API Keys (Optional):**
   
   Create a `.env` file in the project root:
   ```bash
   # For real weather data
   OPENWEATHER_API_KEY=your_openweather_api_key
   
   # For AI chatbot features
   GEMINI_API_KEY=your_gemini_api_key
   ```
   
   **To get API keys:**
   - OpenWeather: https://openweathermap.org/api (free tier: 1000 calls/day)
   - Google Gemini: https://ai.google.dev/ (free tier available)

4. **Run the application:**
   ```bash
   python3 run.py
   ```

5. **Open your browser:**
   ```
   http://localhost:8080
   ```

## 🎯 Usage

### Weather Dashboard
1. Enter a city name in the search box
2. View current weather conditions and 5-day forecast
3. Check weather statistics and temperature ranges

### AI Chatbot
1. Click the chat icon in the bottom-right corner
2. Ask any weather-related question in natural language
3. Get intelligent, context-aware responses from Google Gemini
4. If AI is unavailable, the system falls back to rule-based responses

## 🏗️ Architecture

### Backend (Python Flask)
- **Weather API Integration**: Fetches data from OpenWeather API
- **Gemini AI Integration**: Processes natural language queries
- **Demo Mode**: Provides sample data when API keys aren't configured
- **Fallback System**: Ensures chatbot always responds

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Updates**: Dynamic weather data display
- **Interactive Chatbot**: Smooth chat experience with typing indicators
- **Weather Summaries**: Converts complex data into readable summaries

## 📁 Project Structure

```
Weather Dashboard/
├── app.py                 # Flask backend with AI integration
├── run.py                 # Application launcher
├── demo_data.py           # Sample weather data for demo mode
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── templates/
│   └── index.html        # Main dashboard interface
├── static/
│   ├── css/styles.css    # Modern responsive styling
│   └── js/script.js      # Frontend logic with AI integration
└── README.md             # This documentation
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Required for real weather data
OPENWEATHER_API_KEY=your_openweather_api_key

# Required for AI chatbot features
GEMINI_API_KEY=your_gemini_api_key
```

### Demo Mode
If no API keys are configured, the application runs in demo mode:
- Uses sample weather data
- Chatbot uses rule-based responses
- All features remain functional

## 🤖 AI Integration Details

### Gemini API Integration
- **Model**: gemini-1.5-pro
- **Context**: Weather data summaries in natural language
- **Response Style**: Conversational, helpful, and actionable
- **Error Handling**: Graceful fallback to rule-based responses

### Weather Data Processing
The system converts complex weather data into readable summaries:
- Current conditions with all relevant metrics
- 5-day forecast with daily breakdowns
- Temperature statistics and trends
- Weather patterns and recommendations

## 🎨 Features

### Weather Dashboard
- **Real-time Data**: Current weather conditions
- **5-Day Forecast**: Detailed daily predictions
- **Weather Statistics**: Temperature ranges and averages
- **Responsive Design**: Works on all devices
- **Beautiful UI**: Modern gradients and animations

### AI Chatbot
- **Natural Language**: Ask questions in plain English
- **Context Awareness**: Understands current weather data
- **Intelligent Responses**: AI-powered recommendations
- **Fallback System**: Always provides helpful responses
- **Typing Indicators**: Shows when processing

## 🚀 Deployment

### Local Development
```bash
python3 run.py
```

### Production Deployment
1. Set up a production WSGI server (Gunicorn, uWSGI)
2. Configure environment variables
3. Set up reverse proxy (Nginx, Apache)
4. Enable HTTPS for security

## 🔍 Troubleshooting

### Common Issues

**"City not found" error:**
- Check city spelling
- Try different city names
- Ensure internet connection

**Chatbot not responding:**
- Check API key configuration
- Verify internet connection
- Check browser console for errors

**Gemini API errors:**
- Verify API key is correct
- Check rate limits and quotas
- System will fallback to rule-based responses

### API Rate Limits
- **OpenWeather**: 1000 calls/day (free tier)
- **Google Gemini**: Varies by plan, check quotas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenWeather API for weather data
- Google Gemini for AI capabilities
- Font Awesome for icons
- Flask for the web framework

---

**Enjoy your AI-powered weather dashboard! 🌤️🤖** 