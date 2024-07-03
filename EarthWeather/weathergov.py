#https://www.weather.gov/documentation/services-web-api#/
import requests


wfo = "SEW"
x = 136
y = 48


url = f'https://api.weather.gov/gridpoints/{wfo}/{x},{y}/forecast'


response = requests.get(url).json()

print(response)

