from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response

from skydata.weather_service import fetch_weather_data, get_lat_lon
from .models import SkynexusData
from .serializers import SkynexusDataSerializer
from rest_framework.decorators import action

from django.conf import settings
from django.shortcuts import redirect, render
import requests

# ViewSets combine the logic for a set of related views
# ModelViewSet provides CRUD operations automatically:
# LIST (GET /api/weather/)
# CREATE (POST /api/weather/)
# RETRIEVE (GET /api/weather/{id}/)
# UPDATE (PUT /api/weather/{id}/)
# DELETE (DELETE /api/weather/{id}/)
# queryset defines which records are available through the API
# serializer_class specifies which serializer to use
class SkynexusDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows weather data to be viewed or edited.
    """
    queryset = SkynexusData.objects.all().order_by('-created_at')
    serializer_class = SkynexusDataSerializer

    # Action to save weather data via  POST request
    @action(detail=False,methods=['post'], url_path='save-weather')
    def save_weather(self,  request):
        """Handles custom POST requests to save weather data."""
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Weather data saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # Action to retrieve weather data from the database via GET request
    @action(detail=False, methods=['get'], url_path='fetch-weather')
    def fetch_weather(self,  request):
        """Fetch all weather records, ordered by latest created."""
        weather_data = SkynexusData.objects.all().order_by('-created_at')
        serializer = self.get_serializer(weather_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # Action to get weather details for a specific entry
    @action(detail=True, methods=['get'], url_path='weather-details')
    def weather_details(self, request, pk=None):
        """Fetch weather details for a specific entry."""
        try:
            weather_data = SkynexusData.objects.get(id=pk)
            serializer = self.get_serializer(weather_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SkynexusData.DoesNotExist:
            return Response({"error": "Weather data not found"}, status=status.HTTP_404_NOT_FOUND)
        

    # Action to fetches real-time weather data for a given city
    @action(detail=False, methods=['get'], url_path='search')
    def fetch_current_weather(self, request):
        """Fetches real-time weather data for a given city."""
        try:
            city = request.query_params.get('city')
            coordinates = get_lat_lon(city)
            print(coordinates)
            lat, lon = coordinates
            if coordinates:
                weather_data = fetch_weather_data(lat=lat, lon=lon)
                return  Response(weather_data, status=status.HTTP_200_OK)
            
            #  If city is not found, return a 404 error
            return  Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            #  If any error occurs during fetching weather data, return a 500 error
            return  Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# views.py 
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

def weather_details(request, skydata_id):
    """ Fetch details of a specific weather entry and render in the template. """
    try:
        full_url = f"{API_BASE_URL}weather-details/{skydata_id}/"
        print(f"Fetching weather data from URL: {full_url}")
        response = requests.get(f"{API_BASE_URL}weather-details/{skydata_id}/")
        response.raise_for_status()
        weather = response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        weather = {"error": f"Unable to fetch weather data for the given ID. Error:[{e}]"}

    return render(request, 'weather-details.html', {'weather': weather})


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
        return render(request, 'index.html', {'weather_info': weather_info})
    else:
        return render(request, 'index.html', {'error': 'Unable to retrieve weather data'})


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
            return render(request, 'index.html', {'message': 'Weather data saved successfully'})
        else:
            # If the API call fails, render an error message
            return render(request, 'index.html', {'error': 'Failed to save weather data'})
    else:
        return render(request, 'index.html', {'error': 'No data provided'})