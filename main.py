import json, turtle, urllib.request, time
#pip install turtle==0.0.1
screen = turtle.Screen()
screen.setup(1300,600)
screen.setworldcoordinates(-180,-90,180,90)
screen.bgpic("\git\smallprojects\isstracker\map1.gif")

#api call
url = "http://api.open-notify.org/iss-now.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())

#parse the dictionary 
location = result["iss_position"]
lat = float(location['latitude'])
lon = float(location['longitude'])
print(lon,lat)
turtle.penup()
turtle.goto(lon,lat)
turtle.pendown()
 
#loop to move turtle
while True:

    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    location = result["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    print(lon,lat)
    turtle.goto(lon,lat)

    #delay the loop
    time.sleep(5)


