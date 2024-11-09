from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from skydata.weather_service import fetch_weather_data, get_lat_lon
from .models import SkynexusData
from .serializers import SkynexusDataSerializer

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
    Provides standard CRUD operations and additional custom actions 
    for fetching and saving weather data. Utilizes the SkynexusData 
    model with a serializer for data representation.
    """
    queryset = SkynexusData.objects.all().order_by('-created_at')
    serializer_class = SkynexusDataSerializer

    @action(detail=False, methods=['post'], url_path='save-weather')
    def save_weather(self, request):
        """
        Custom action to save new weather data to the database.
        Accepts POST data to create a new SkynexusData entry. If 
        validation is successful, the data is saved, otherwise an 
        error response is returned.

        Args:
            request: HTTP POST request with weather data.

        Returns:
            HTTP 201 response with success message on valid data,
            HTTP 400 response with validation errors otherwise.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Weather data saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='fetch-weather')
    def fetch_weather(self, request):
        """
        Custom action to retrieve all weather data entries from the database.
        Returns a list of all SkynexusData entries ordered by creation date.

        Args:
            request: HTTP GET request.

        Returns:
            HTTP 200 response with serialized data of all weather entries.
        """
        weather_data = SkynexusData.objects.all().order_by('-created_at')
        serializer = self.get_serializer(weather_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='weather')
    def weather_details(self, request, pk=None):
        """
        Custom action to retrieve specific weather data by its ID.
        Fetches detailed data of a specific SkynexusData entry using 
        the provided primary key.

        Args:
            request: HTTP GET request.
            pk: Primary key of the SkynexusData entry to retrieve.

        Returns:
            HTTP 200 response with serialized weather data if found,
            HTTP 404 response if the entry does not exist.
        """
        try:
            weather_data = SkynexusData.objects.get(id=pk)
            serializer = self.get_serializer(weather_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SkynexusData.DoesNotExist:
            return Response({"error": "Weather data not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='search')
    def fetch_current_weather(self, request):
        """
        Custom action to fetch real-time weather data for a specific city.
        Takes a city name as a query parameter, retrieves its latitude and 
        longitude, and uses these coordinates to obtain live weather data 
        from an external source.

        Args:
            request: HTTP GET request with 'city' query parameter.

        Returns:
            HTTP 200 response with current weather data if found,
            HTTP 404 response if the city is not recognized,
            HTTP 500 response if an internal error occurs.
        """
        try:
            city = request.query_params.get('city')
            coordinates = get_lat_lon(city)
            lat, lon = coordinates
            if coordinates:
                weather_data = fetch_weather_data(lat=lat, lon=lon)
                return Response(weather_data, status=status.HTTP_200_OK)
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
