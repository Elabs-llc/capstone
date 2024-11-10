from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status

# Base URL for the API endpoints
API_BASE_URL = 'http://127.0.0.1:8000/skydata/api/skynexusdata/'


def home(request):
    """
    Handles the main page and search functionality for fetching weather data by city.
    Accepts a POST request with a city name, fetches the weather data using the API,
    and stores the results in the session for later retrieval in `sky_view`.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered template for the home page or a redirect to the `sky_view` page if data is found.
    """
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
    """
    Retrieve and display stored weather data from the session.
    Retrieves the weather data from the session (set in `home`) and
    displays it on the results page. If no data is available, displays an error.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered template displaying weather data or an error message if unavailable.
    """
    weather_info = request.session.pop('weather_info', None)  # Retrieve and remove from session
    if weather_info:
        return render(request, 'results.html', {'weather_info': weather_info})
    else:
        return render(request, 'results.html', {'error': 'Unable to retrieve weather data'})


def save_skydata(request):
    """
    Save weather information by making a POST request to the save_weather API.
    Accepts weather data via POST request, sends it to the save_weather API endpoint,
    and renders a success or error message based on the API response.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        A rendered template showing either a success message if data is saved successfully
        or an error message if saving fails.
    """
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

def fetch_skydata(request):
    """
    Fetch weather data from the API and render it in the template.
    Sends a GET request to fetch all weather data entries and renders the
    data in the 'weather-data.html' template. If an error occurs while fetching,
    an empty list is passed as fallback.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        A rendered template displaying weather data.
    """
    try:
        response = requests.get(f"{API_BASE_URL}fetch-weather/")
        response.raise_for_status()  # Check for HTTP errors
        weather_data = response.json()  # Parse the JSON data from API response
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        weather_data = []  # Fallback if there's an error

    return render(request, 'weather-data.html', {'weather_data': weather_data})


def weather_info(request, skydata_id):
    """
    Fetch details of a specific weather entry by ID and render it in the template.
    Sends a GET request to fetch data for a specific weather entry, using the
    entry's ID as a parameter. If an error occurs, an error message is displayed.
    
    Args:
        request: The HTTP request object.
        skydata_id: The ID of the weather data entry to fetch.
        
    Returns:
        A rendered template with details of the specified weather entry.
    """
    try:
        response = requests.get(f"{API_BASE_URL}{skydata_id}/weather/")
        response.raise_for_status()
        weather_data = response.json()
        print(weather_data)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        weather_data = {"error": f"Unable to fetch weather data for the given ID. Error:[{e}]"}

    return render(request, 'weather-details.html', {'weather': weather_data})
