from django.db import models

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