import h3
import json

H3_LEVEL = 5
if __name__ == '__main__':
    geojson = {
        'type': 'Polygon',
        'coordinates': [[[0.0, 0.0], [180, 0.0], [180.0, 90.0], [0.0, 90.0], [0.0, 0.0]]]}

    res = h3.polyfill(geojson, H3_LEVEL, geo_json_conformant=False)
    # print(res)
    jsons = open('mygeojson.json').read()
    geojson = json.loads(jsons)
    res = h3.polyfill_geojson(geojson, H3_LEVEL)
