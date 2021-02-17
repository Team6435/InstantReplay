import googlemaps
import polyline
import pickle as pkl
from geopy import distance
import gmaps
import matplotlib
import webbrowser as w

try:
    f = open('api.key','r')
except FileNotFoundError:
    print("Cannot find file api.key with api key for google maps")
    raise RuntimeError

api_key = f.read()
f.close()

gmap = googlemaps.Client(api_key)
gmaps.configure(api_key=api_key)

legoland = "33.12727798626295, -117.31035714300366"
legoland_tuple = (33.12727798626295, -117.31035714300366)

try:
    f = open('map_steps.txt','rb')
except FileNotFoundError:
    print("Run maps_init.py to initialize datastream")
    raise RuntimeError

steps = pkl.load(f)
f.close()

x=input("How much distance walked? (meters): ")
try:
    x=int(x)
except ValueError:
    print("Need Integer value!")
    raise RuntimeError

initLat = steps[0]['start_location']['lat']
initLon = steps[0]['start_location']['lng']
lastDist = 0
while True:
    lastDist =  steps[0]['distance']['value']
    x -= lastDist
    if x < 0:
        x += lastDist
        break
    del steps[0]
    if len(steps) == 0:
        print("You Have Arrived!")
        quit()

locs = polyline.decode(steps[0]['polyline']['points'])
startpos = locs[0]
while x > 0:
    x -= distance.distance(startpos,locs[0]).m
    del locs[0]

endpos = locs[0]

newDirs = gmap.directions(str(endpos[0]) + ', ' + str(endpos[1]),legoland,mode='walking',avoid='ferries')
f2 = open('map_steps.txt','wb')
pkl.dump(newDirs[0]['legs'][0]['steps'],f2)
f2.close()

print(str(newDirs[0]['legs'][0]['distance']['value']) + ' meters remaining!')

#w.open('https://www.google.com/maps/dir/'+str(startpos[0])+',+'+str(startpos[1])+'/33.12727798626295,+-117.31035714300366/&mode=walking')
#w.open('https://www.google.com/maps/dir/?api=1&origin='+str(startpos[0])+',+'+str(startpos[1])+'&destination=33.12727798626295,+-117.31035714300366&travelmode=walking')
w.open('https://www.google.com/maps/dir/?api=1&origin=40.95498914990517,+-72.9446308633918&destination=33.12727798626295,+-117.31035714300366&travelmode=walking&waypoints='+str(startpos[0])+',+'+str(startpos[1]))
