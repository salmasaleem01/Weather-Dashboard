#!/usr/bin/env python3
"""
Setup script for Weather Dashboard with Python Chatbot
"""

import os
import sys

def setup_api_key():
    """Interactive setup for OpenWeather API key"""
    print("🌤️ Weather Dashboard Setup")
    print("=" * 40)
    
    # Check if API key is already set
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if api_key and api_key != 'YOUR_OPENWEATHER_API_KEY':
        print(f"✅ OpenWeather API Key is already set")
        return True
    
    print("\n📋 To use this weather dashboard, you need an OpenWeather API key:")
    print("1. Visit: https://openweathermap.org/api")
    print("2. Sign up for a free account")
    print("3. Get your API key from your account dashboard")
    print("4. The free tier allows 1000 calls per day")
    
    print("\n🔑 Enter your OpenWeather API key (or press Enter to skip):")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("\n⚠️  No API key provided. The application will show an error when searching for cities.")
        print("You can set the API key later by:")
        print("1. Setting the OPENWEATHER_API_KEY environment variable")
        print("2. Editing the OPENWEATHER_API_KEY variable in app.py")
        return False
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f'OPENWEATHER_API_KEY={api_key}\n')
    
    print(f"\n✅ API key saved to .env file")
    print("🚀 You can now run the application with: python3 app.py")
    return True

def main():
    """Main setup function"""
    try:
        setup_api_key()
        print("\n🎉 Setup complete! Run 'python3 app.py' to start the server.")
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 