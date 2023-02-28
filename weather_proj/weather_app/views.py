from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from json import *
import json
from django.http import HttpResponse, JsonResponse
import configparser
from django.conf import settings

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг



class ForecastWeather(APIView):
    """Получение погоды по дате и времени"""

    def get(self, request):
        city = request.GET.get('city')
        dt = request.GET.get('dt')
        api_url = settings.URL_API_WEATHER
        api_url = api_url.format(city)
        response_api = requests.get(api_url).json()
        if len(dt.split("_")) == 2:
            dt = dt.replace("_", " ")
            for date in response_api["forecast"]["forecastday"]:
                for dtime in date["hour"]:
                    if dtime["time"] == dt:
                        resp_date = str(dtime["temp_c"])
        elif len(dt.split("_")) == 1:
            for date in response_api["forecast"]["forecastday"]:
                if date["date"] == dt:
                    print(date["hour"][1])
                    resp_date = str(date["day"]["avgtemp_c"])

        resp = {"city":response_api["location"]["name"], "unit":"celsius", "temperature":resp_date}

        return JsonResponse(resp)


class CurrentWeather (APIView):
    """Получение погоды текущей даты и времени"""

    def get(self, request):
        city = request.GET.get('city')
        api_url = "http://api.weatherapi.com/v1/forecast.json?key=92b2b54828074632897211731232702&q={}"
        api_url = api_url.format(city)
        response_api = requests.get(api_url).json()
        resp = {"city":response_api["location"]["name"], "unit":"celsius", "temperature":response_api["current"]["temp_c"]}

        return JsonResponse(resp)