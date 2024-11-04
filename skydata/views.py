from django.http import Http404
from django.shortcuts import render
import requests



def sky_view(request, lat,lon):
    # openweathermap api key
    api_key = "7e2a82a043dd7fa93fe729456e6dbe56"
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}")

        if response.status_code == 200:
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
            return render(request, 'index.html', {'weather_info': weather_info})
        else:
            return render(request, 'index.html', {'error': 'Unable to retrieve weather data'})
    except:
        raise Http404("Error : Unable to retrieve weather data")


# Save  Weather Information
# def save_skydata():
#     """ Save  Weather Information"""
   