from django.urls import path
from . import views

app_name = 'skydata'
urlpatterns = [
    path('<str:lat>/<str:lon>/', views.sky_view,  name='index'),
    path('', views.save_skydata,  name='save-skydata'),
    path('fetch/', views.fetch_skydata,  name='fetch-skydata'),

]
