import requests
from django.http import Http404

def get_lat_lon(city_name):
    """Fetch latitude and longitude from a city name using the OpenCage API."""
    geocode_api_key = "d92a7df738bc434582c7f7fd2b96f868"  # Replace with your geocoding API key
    try:
        geocode_response = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={geocode_api_key}")
        
        geocode_response.raise_for_status()
        
        data = geocode_response.json()
        
        if data['results']:
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return lat, lon
        else:
            raise ValueError("No results found for the specified city.")
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise Http404("Unable to connect to the geocoding service.")
    except ValueError as json_error:
        print(f"JSON decoding error occurred: {json_error}")
        raise Http404("Data Error: Unable to retrieve latitude and longitude.")

def fetch_weather_data(lat, lon):
    """Fetch weather data from OpenWeatherMap using latitude and longitude."""
    api_key = "7e2a82a043dd7fa93fe729456e6dbe56"  
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}")

        response.raise_for_status()

        data = response.json()
        weather_info = {
            "city": data['name'],
            "country": data['sys']['country'],
            "temperature": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "weather_description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon'],
            "wind_speed": data['wind']['speed'],
            "humidity": data['main']['humidity'],
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise Http404("Unable to connect to the weather service.")
    except ValueError as json_error:
        print(f"JSON decoding error occurred: {json_error}")
        raise Http404("Data Error: Unable to retrieve weather data.")
