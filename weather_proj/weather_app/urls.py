from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('forecast', views.ForecastWeather.as_view()),
    path('current', views.CurrentWeather.as_view()),
]