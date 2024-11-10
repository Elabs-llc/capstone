from django.urls import include, path
from . import views

# The URL configuration for the skydata app. This file maps URL patterns to 
# specific view functions for rendering templates or handling requests.

app_name = 'skydata'

urlpatterns = [
    # Home page that displays the main form and weather data.
    path('', views.home, name='home'),

    # URL for viewing detailed weather information for a specific entry.
    # The 'skydata_id' is passed as an integer parameter to identify the specific weather data.
    path('weather/<int:skydata_id>/info/', views.weather_info, name='weather-details'),

    # URL for rendering the weather information view based on session data.
    path('weather/view/', views.sky_view, name='sky-view'),

    # URL for saving new weather data through a POST request.
    path('weather/save/', views.save_skydata, name='save-skydata'),

    # URL for fetching weather data from the API and displaying it.
    path('weather/fetch/', views.fetch_skydata, name='fetch-skydata'),

    # Include the API routes from the skydata API configuration
    # This will link the API routes under the 'api/' prefix.
    path('api/', include('skydata.api_urls')),
]
