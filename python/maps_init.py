import googlemaps
import polyline
import pickle as pkl

try:
    f = open('api.key','r')
except FileNotFoundError:
    print("Cannot find file api.key with api key for google maps")
    raise RuntimeError

api_key = f.read()
f.close()

gmaps = googlemaps.Client(api_key)


home = "40.95498914990517, -72.9446308633918"
legoland = "33.12727798626295, -117.31035714300366"

dirs = gmaps.directions(home,legoland,mode='walking',avoid='ferries')

steps = dirs[0]['legs'][0]['steps']

f = open('map_steps.txt','wb')
pkl.dump(steps,f)
f.close()
