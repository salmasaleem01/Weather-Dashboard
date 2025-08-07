#!/usr/bin/env python3
"""
Weather Dashboard Runner
"""

import os
import sys
from app import app

def main():
    """Start the weather dashboard application"""
    print("🌤️ Weather Dashboard with Python Chatbot")
    print("=" * 50)
    
    # Check if API key is configured
    api_key = os.getenv('OPENWEATHER_API_KEY', 'YOUR_OPENWEATHER_API_KEY')
    
    if api_key == 'YOUR_OPENWEATHER_API_KEY':
        print("⚠️  Demo Mode: Using sample weather data")
        print("📝 To use real weather data:")
        print("   1. Get API key from: https://openweathermap.org/api")
        print("   2. Run: export OPENWEATHER_API_KEY='your_api_key'")
        print("   3. Restart the application")
    else:
        print("✅ Real weather data mode enabled")
    
    print("\n🚀 Starting Flask application...")
    print("📱 Open your browser to: http://localhost:8080")
    print("💬 Chatbot is ready to answer weather questions!")
    print("\n" + "=" * 50)
    
    # Start the Flask app
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )

if __name__ == '__main__':
    main() 