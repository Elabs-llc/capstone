from django.http import Http404
from django.shortcuts import get_object_or_404, render
import requests

from skydata.models import SkynexusData



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
    except ValueError as json_error:
        print(f"JSON decoding error occurred: {json_error}")
        raise Http404("Data Error: Unable to parse weather data")


# Save  Weather Information
def save_skydata(request):
    """ Save  Weather Information"""
    if request.method == 'POST':
        weather_data = {
            'city': request.POST.get('city', 'NA'),
            'country': request.POST.get('country', 'Unknown'),
            'temperature': request.POST.get('temperature', 0.0),
            'feels_like': request.POST.get('feels_like', 0.0),
            'weather_description': request.POST.get('weather_description', 'NA'),
            'wind_speed': request.POST.get('wind_speed', 0.0),
            'humidity': request.POST.get('humidity', 0),
        }
        # Database logic  to save the weather data
        SkynexusData.objects.create(**weather_data)

        return render(request, 'index.html', {'message': 'Weather data saved successfully'})
    else:
        return render(request, 'index.html', {'error': 'Unable to save weather data'})
    

# Fetch Weather Information from the database
def fetch_skydata(request):
    """ Fetch Weather Information from the database"""
    #weather_data = get_object_or_404(SkynexusData, pk=1)
    weather_data = SkynexusData.objects.all().order_by('-created_at')
    return render(request, 'weather-data.html', {'weather_data': weather_data})
   