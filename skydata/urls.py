from django.urls import include, path
from . import views

app_name = 'skydata'

urlpatterns = [
    path('', views.home, name='home'),
    path('weather/details/<int:skydata_id>/', views.weather_info, name='weather-details'),
    path('weather/view/', views.sky_view, name='sky-view'),
    path('weather/save/', views.save_skydata, name='save-skydata'),
    path('weather/fetch/', views.fetch_skydata, name='fetch-skydata'),
    # Include the API routes
    path('api/', include('skydata.api_urls')),
]
