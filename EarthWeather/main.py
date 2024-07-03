import requests
import datetime as dt

key = "871b164390ed1749a8718267f697cdf5"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city = "London"
url = base_url + "appid=" + key + "&q=" + city
response = requests.get(url).json()

def kelvin_to_celsius_fahrenheit(kelkin):
    celsius = kelvin - 273.15
    fahrenheit = celsius* 9/5 +32
    return celsius, fahrenheit




print(response)

