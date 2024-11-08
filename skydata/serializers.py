from rest_framework import serializers
from .models import SkynexusData

# Serializers convert complex data types (like Django models) to 
# Python primitives that can be rendered into JSON
# ModelSerializer automatically creates a set of fields based on 
# your model
# fields list specifies which model fields to include in the 
# serialization
# read_only_fields indicates fields that can't be modified 
# through the API
class SkynexusDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkynexusData
        fields = '__all__'
        #['id', 'city', 'country', 'temperature', 'feels_like', 
                 #'weather_description', 'wind_speed', 'humidity', 'created_at']
        #read_only_fields = ('id', 'created_at')