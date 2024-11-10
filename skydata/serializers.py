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
from rest_framework import serializers
from .models import SkynexusData

class SkynexusDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SkynexusData model.
    
    This serializer translates SkynexusData model instances into JSON format 
    for API responses and also validates and saves data from JSON inputs 
    to model instances for API requests. Using ModelSerializer, it 
    automatically maps model fields to serializer fields.
    
    Attributes:
        model (SkynexusData): The model class being serialized.
        fields (list of str): Specifies the fields to include in serialization.
        read_only_fields (tuple of str): Fields that are read-only, 
            meaning they cannot be modified through the API.
    """

    class Meta:
        model = SkynexusData
        fields = [
            'id', 'city', 'country', 'temperature', 'feels_like', 
            'weather_description', 'wind_speed', 'humidity', 'created_at',
        ]
        # read_only_fields = ('id', 'created_at')
