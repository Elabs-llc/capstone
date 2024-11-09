from datetime import timezone
import datetime
from django.db import models
from django.contrib import admin

# Define the SkynexusData model which will store weather-related data.
class SkynexusData(models.Model):
    # Auto-incrementing primary key for each entry
    id = models.AutoField(primary_key=True)

    # Store the city name (default is 'NA' if not provided)
    city = models.CharField(max_length=100, default="NA")

    # Store the country name (default is 'Unknown' if not provided)
    country = models.CharField(max_length=100, default='Unknown')

    # Store the current temperature in Celsius (default is 0.0)
    temperature = models.FloatField(default=0.0)

    # Store the "feels like" temperature (default is 0.1)
    feels_like = models.FloatField(default=0.1)

    # Store a brief description of the weather (default is 'NA')
    weather_description = models.CharField(max_length=255, default="NA")

    # Store the wind speed in meters per second (default is 0.0)
    wind_speed = models.FloatField(default=0.0)

    # Store the humidity as a percentage (default is 0)
    humidity = models.IntegerField(default=0)

    # Automatically sets the current time when a new record is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the SkynexusData instance, formatted as:
        "City, Country - Temperature°C"

        Returns:
        str: A human-readable string for displaying SkynexusData.
        """
        return f"{self.city}, {self.country} - {self.temperature}°C"

    # The method to check if the record was created recently, within the last 24 hours.
    @admin.display(
        boolean=True,  # Display as a boolean value (True/False) in admin interface
        ordering='created_at',  # Allow sorting by created_at field
        description='Created recently?'  # Custom column name in admin interface
    )
    def was_created_recently(self):
        """
        Check if the current instance of SkynexusData was created within the last 24 hours.

        This method is used in the admin interface to display whether the record 
        was created recently. It compares the 'created_at' field with the current time.

        Parameters:
        self (SkynexusData): The instance of SkynexusData to check.

        Returns:
        bool: True if the instance was created within the last 24 hours, False otherwise.
        """
        now = timezone.now()  # Get the current time in UTC
        return now - datetime.timedelta(days=1) <= self.created_at <= now  # Check if within the last 24 hours
