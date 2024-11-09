from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status

# This views are for testing the API's above

API_BASE_URL = 'http://127.0.0.1:8000/skydata/api/skynexusdata/'

def fetch_skydata(request):
    """ Fetch weather data from the API and render it in the template. """
    try:
        response = requests.get(f"{API_BASE_URL}fetch-weather/")
        response.raise_for_status()  # Check for HTTP errors
        weather_data = response.json()  # Parse the JSON data from API response
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        weather_data = []  # Fallback if there's an error

    return render(request, 'weather-data.html', {'weather_data': weather_data})

def weather_info(request, skydata_id):
    """ Fetch details of a specific weather entry and render in the template. """
    try:
        response = requests.get(f"{API_BASE_URL}{skydata_id}/weather/")
        response.raise_for_status()
        weather_data = response.json()
        print(weather_data)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        weather_data = {"error": f"Unable to fetch weather data for the given ID. Error:[{e}]"}

    return render(request, 'weather-details.html', {'weather': weather_data})

def home(request):
    if request.method == 'POST':
        city_name = request.POST.get('city')
        if city_name:
            try:
                # Make an API call to fetch weather data for the city
                response = requests.get(f"{API_BASE_URL}search/?city={city_name}")
                response.raise_for_status()  # Raise an exception for HTTP errors

                if response.status_code == status.HTTP_200_OK:
                    # Extract weather data from the response
                    weather_info = response.json()

                    # Check if weather data exists
                    if weather_info:
                        # Redirect to sky-view and pass the entire weather data
                        #return redirect('skydata:sky-view', weather_info=weather_info)
                        print(weather_info)
                        # Store weather_info in session to retrieve in sky_view
                        request.session['weather_info'] = weather_info
                        return HttpResponseRedirect(reverse('skydata:sky-view'))
                    else:
                        return render(request, 'home.html', {'error': 'Weather data not found.'})

                elif response.status_code == status.HTTP_404_NOT_FOUND:
                    return render(request, 'home.html', {'error': f'City [{city_name}] not found'})
                else:
                    return render(request, 'home.html', {'error': 'Error fetching weather data'})

            except requests.RequestException as e:
                return render(request, 'home.html', {'error': f'Error fetching weather data: {e}'})
    
    return render(request, 'home.html')

def sky_view(request):
    weather_info = request.session.pop('weather_info', None)  # Retrieve and remove from session
    if weather_info:
        return render(request, 'results.html', {'weather_info': weather_info})
    else:
        return render(request, 'results.html', {'error': 'Unable to retrieve weather data'})


def save_skydata(request):
    """Save Weather Information by calling the save_weather API"""
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
        
        # Make a POST request to the save_weather API
        api_url = f'{API_BASE_URL}save-weather/' 
        response = requests.post(api_url, data=weather_data)
        
        if response.status_code == 201:
            # If API call is successful, render success message
            return render(request, 'results.html', {'message': 'Weather data saved successfully'})
        else:
            # If the API call fails, render an error message
            return render(request, 'results.html', {'error': 'Failed to save weather data'})
    else:
        return render(request, 'results.html', {'error': 'No data provided'})