from django.urls import path
from . import views

urlpatterns = [
    path('<str:lat>/<str:lon>/', views.sky_view,  name='index'),

]
