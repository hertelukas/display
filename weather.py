import requests
from requests.models import Response

class Weather:
    def __init__(self, max, min, icon):
        self.max = max
        self.min = min
        self.icon = icon


def get_forecast(lat, lon, days, openAPI):
    apiResponse = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=%3.2f&lon=%3.2f&exclude=minutely&appid=%s&units=metric' %(lat, lon, openAPI))
    response = apiResponse.json()

    forecast = response['daily']

    result = []
    for i in range(days):
        result.append(Weather(forecast[i]['temp']['max'], forecast[i]['temp']['min'], forecast[i]['weather'][0]['id']))
        
    return result