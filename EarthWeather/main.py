import requests
import datetime as dt

key = "871b164390ed1749a8718267f697cdf5"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city = "London"
url = base_url + "appid=" + key + "&q=" + city
response = requests.get(url).json()

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius* 9/5 +32
    return celsius, fahrenheit




print(response['coord'])

{'coord': {'lon': -0.1257, 'lat': 51.5085},
 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}],
   'base': 'stations', 
   'main': {'temp': 291.77, 'feels_like': 291.2, 'temp_min': 290.13, 'temp_max': 292.97, 'pressure': 1016, 'humidity': 58, 'sea_level': 1016, 'grnd_level': 1012},
     'visibility': 10000, 'wind': {'speed': 3.6, 'deg': 360}, 
     'clouds': {'all': 75}, 'dt': 1720798493,
       'sys': {'type': 2, 'id': 2075535, 'country': 'GB', 'sunrise': 1720756663, 'sunset': 1720815252}, 
       'timezone': 3600, 
       'id': 2643743,
         'name': 'London', 
         'cod': 200}
