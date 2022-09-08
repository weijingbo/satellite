import os, json
import geoh

GEOHASH_LEVEL = 4
jsons = open('geojson-sf.json').read()
geojson = json.loads(jsons)
geohashes = geoh.geohashes(geojson=geojson, precision=GEOHASH_LEVEL)
print(geohashes)
# print(geojson['features'][0]['geometry'])
