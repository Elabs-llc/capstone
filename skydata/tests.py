from django.shortcuts import render
from django.test import TestCase
import requests

from skydata.views import API_BASE_URL

# Create your tests here.
class Test(TestCase):
    def test_fetch_skydata(self):
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
        # print(weather_data)
        self.assertIn('weather_data', locals())
        
    def weather_info(self):
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
        skydata_id = 12
        try:
            response = requests.get(f"{API_BASE_URL}{skydata_id}/weather/")
            response.raise_for_status()
            weather_data = response.json()
            print(weather_data)
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            weather_data = {"error": f"Unable to fetch weather data for the given ID. Error:[{e}]"}
        print(weather_data)
        self.assertIn('weather_data', locals())
        
