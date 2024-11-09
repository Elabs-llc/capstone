from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Import the viewset that will handle the API logic for SkynexusData.
from .api import SkynexusDataViewSet

# Initialize the DefaultRouter which will automatically generate the URL patterns 
# for the viewsets (like listing, creating, updating, etc.)
router = DefaultRouter()

# Register the 'skynexusdata' endpoint with the viewset, which will handle 
# the CRUD operations for SkynexusData records.
# The 'basename' argument defines the name of the viewset in the URL.
router.register(r'skynexusdata', SkynexusDataViewSet, basename='skynexusdata')

# URL patterns for the API.
# All API routes related to SkynexusData will be handled under the `/api/` prefix.
urlpatterns = [
    path('', include(router.urls)),  # Include all the generated routes from the router.
]
