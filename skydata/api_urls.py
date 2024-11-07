from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkynexusDataViewSet

# Set up the DefaultRouter for the API endpoints
router = DefaultRouter()
router.register(r'skynexusdata', SkynexusDataViewSet, basename='skynexusdata')

# Include all API routes under the `api/` path
urlpatterns = [
    path('', include(router.urls)),
]
