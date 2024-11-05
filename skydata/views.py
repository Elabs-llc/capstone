from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
import requests

from skydata.models import SkynexusData
from skydata.weather_service import fetch_weather_data, get_lat_lon

def home(request):
    if request.method == 'POST':
        city_name = request.POST.get('city')
        if city_name:
            data = get_lat_lon(city_name)
            if data:  # Check if data is not None

                # Unpack latitude and longitude from the returned tuple
                lat, lon = data  

                # Redirect to sky_view to process data
                return redirect('skydata:sky-view', lat=lat, lon=lon)
            
            else:
                return render(request, 'home.html', {'error': 'Latitude and longitude not found'})
                    
        else:
            return render(request, 'home.html', {'error': 'City not found'})
    
    
    return render(request, 'home.html')


def sky_view(request, lat,lon):
    # openweathermap api key
    if lat and lon:
        # Fetch weather data
        weather_info = fetch_weather_data(lat, lon)
            
        return render(request, 'index.html', {'weather_info': weather_info})
    else:
        return render(request, 'index.html', {'error': 'Unable to retrieve weather data'})


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
        return render(request, 'index.html', {'error': 'No latitiude and longitude provided'})
    

# Fetch Weather Information from the database
def fetch_skydata(request):
    """ Fetch Weather Information from the database"""
    #weather_data = get_object_or_404(SkynexusData, pk=1)
    weather_data = SkynexusData.objects.all().order_by('-created_at')
    return render(request, 'weather-data.html', {'weather_data': weather_data})
   

# Details of Weather Information
def weather_details(request, skydata_id):
    """ Details of Weather Information"""
    weather_data = get_object_or_404(SkynexusData, pk=skydata_id)
    return render(request, 'weather-details.html', {'weather_data': weather_data})