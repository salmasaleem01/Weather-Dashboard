"""
Demo weather data for testing the application without API key
"""

import json
from datetime import datetime, timedelta

def get_demo_current_weather(city):
    """Return demo current weather data"""
    return {
        "coord": {"lon": -0.13, "lat": 51.51},
        "weather": [
            {
                "id": 800,
                "main": "Clear",
                "description": "clear sky",
                "icon": "01d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 22.5,
            "feels_like": 21.8,
            "temp_min": 18.2,
            "temp_max": 26.1,
            "pressure": 1013,
            "humidity": 65
        },
        "visibility": 10000,
        "wind": {
            "speed": 3.6,
            "deg": 280
        },
        "clouds": {"all": 0},
        "dt": int(datetime.now().timestamp()),
        "sys": {
            "type": 2,
            "id": 2075535,
            "country": "GB",
            "sunrise": int((datetime.now() - timedelta(hours=6)).timestamp()),
            "sunset": int((datetime.now() + timedelta(hours=6)).timestamp())
        },
        "timezone": 0,
        "id": 2643743,
        "name": city,
        "cod": 200
    }

def get_demo_forecast(city):
    """Return demo 5-day forecast data"""
    forecast_list = []
    base_time = datetime.now()
    
    for i in range(40):  # 5 days * 8 intervals per day
        time = base_time + timedelta(hours=3*i)
        temp = 20 + (i % 10) - 5  # Varying temperature
        
        forecast_list.append({
            "dt": int(time.timestamp()),
            "main": {
                "temp": temp,
                "feels_like": temp - 1,
                "temp_min": temp - 3,
                "temp_max": temp + 3,
                "pressure": 1013,
                "sea_level": 1013,
                "grnd_level": 1010,
                "humidity": 60 + (i % 20),
                "temp_kf": 0
            },
            "weather": [
                {
                    "id": 800 if i % 3 == 0 else 300,
                    "main": "Clear" if i % 3 == 0 else "Drizzle",
                    "description": "clear sky" if i % 3 == 0 else "light intensity drizzle",
                    "icon": "01d" if i % 3 == 0 else "09d"
                }
            ],
            "clouds": {"all": 0 if i % 3 == 0 else 40},
            "wind": {
                "speed": 2.5 + (i % 3),
                "deg": 280 + (i % 40)
            },
            "visibility": 10000,
            "pop": 0.1 if i % 3 != 0 else 0,
            "sys": {"pod": "d" if 6 <= time.hour <= 18 else "n"},
            "dt_txt": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return {
        "cod": "200",
        "message": 0,
        "cnt": 40,
        "list": forecast_list,
        "city": {
            "id": 2643743,
            "name": city,
            "coord": {"lat": 51.51, "lon": -0.13},
            "country": "GB",
            "population": 1000000,
            "timezone": 0,
            "sunrise": int((base_time - timedelta(hours=6)).timestamp()),
            "sunset": int((base_time + timedelta(hours=6)).timestamp())
        }
    }

def get_demo_weather_data(city):
    """Return complete demo weather data for a city"""
    return {
        'current': get_demo_current_weather(city),
        'forecast': get_demo_forecast(city)
    } 