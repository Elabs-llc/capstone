from django.urls import path
from . import views

app_name = 'skydata'

urlpatterns = [
    path('', views.home, name='home'),
    path('weather/details/<int:skydata_id>/', views.weather_details, name='weather-details'),
    path('weather/view/<str:lat>/<str:lon>/', views.sky_view, name='sky-view'),
    path('weather/save/', views.save_skydata, name='save-skydata'),
    path('weather/fetch/', views.fetch_skydata, name='fetch-skydata'),
]
