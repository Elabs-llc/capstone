from datetime import timezone
import datetime
from django.db import models
from django.contrib import admin

# Create your models here.
class SkynexusData(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100, default="NA")
    country = models.CharField(max_length=100, default='Unknown')
    temperature = models.FloatField(default=0.0)
    feels_like = models.FloatField(default=0.1)
    weather_description = models.CharField(max_length=255, default="NA")
    wind_speed = models.FloatField(default=0.0)
    humidity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}, {self.country} - {self.temperature}°C"
    

    # To enable the was_created_recently method to be displayed in the admin interface,
    # we need to use the admin.display decorator.
    @admin.display(
        boolean=True,
        ordering='created_at',
        description='Created recently?',
    )
    def was_created_recently(self):
        """
        Check if the current instance of SkynexusData was created within the last 24 hours.

        Parameters:
        self (SkynexusData): The instance of SkynexusData to check.

        Returns:
        bool: True if the instance was created within the last 24 hours, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now