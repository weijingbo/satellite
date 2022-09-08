import time

from geojson_utils import draw_circle
from skyfield import api
from skyfield.api import Loader
import math
import json
import geoh

TLE_URL = 'https://celestrak.com/NORAD/elements/starlink.txt'
R_MEAN = 6378.1  # 轨道的平均半径
MIN_TERMINAL_ANGLE_DEG = 35  # 从地面能看到卫星的角度
ANGLE = 25
GEOHASH_LEVEL = 3  # geohash的等级，等级越高，geohash被划分的越精细，计算成本越高


#  加载卫星
def load_sats():
    load = Loader('./tle_cache')
    sats = load.tle_file(url=TLE_URL)
    return sats


# 计算角度
def calcCapAngle(altitude: float, term_angle: float) -> float:
    """Returns the cap angle (lambda_FOV/2) in radians"""
    epsilon = math.radians(term_angle)
    try:
        eta_FOV = math.asin((math.sin(epsilon + math.radians(90))
                             * R_MEAN) / (R_MEAN + altitude))
        lambda_FOV = 2 * (math.pi - (epsilon + math.radians(90) + eta_FOV))
        return lambda_FOV / 2
    except:
        print("this satellite can not calculate")
        return -1


if __name__ == '__main__':
    s_time = time.time()
    jsons = open('mygeojson.json').read()
    geojson = json.loads(jsons)
    geohashes = geoh.geohashes(geojson=geojson, precision=GEOHASH_LEVEL)
    geoset = set(geohashes)
    print(geoset)
    load = Loader('./tle_cache')
    sats = load.tle_file(url=TLE_URL)
    print("共加载了{}颗卫星".format(len(sats)))
    ts = api.load.timescale()
    now = ts.now()
    subpoints = {sat.name: sat.at(now).subpoint() for sat in sats}
    a =0
    for sat_name, sat in subpoints.items():
        sat_location = (sat.latitude.degrees, sat.longitude.degrees,)
        angle = calcCapAngle(sat.elevation.km, ANGLE)
        if angle == -1:
            print(sat_name)
            pass
        rad = R_MEAN * angle * 1000
        try:
            pt_center = json.loads(
                '{"type": "Point", "coordinates":[' + str(sat_location[0]) + ',' + str(sat_location[1]) + ']}')
            circle = draw_circle(rad, pt_center, 15)['coordinates'][0]
            first_point = circle[0]
            circle.append(first_point)
            strlist = '{ "type": "FeatureCollection","features": [{ "type": "Feature","geometry": {"type":"Polygon",' \
                      '"coordinates":[[' + ','.join('%s' % id for id in circle) + ']]}}]} '
            circle_json = json.loads(strlist)
            circlehashes = geoh.geohashes(geojson=circle_json, precision=GEOHASH_LEVEL)
            circleset = set(circlehashes)
            print(circleset)
            geoset = geoset-circleset

            if (len(geoset) == 0):
                print("该区域已被全部覆盖")
                break
        except:
            pass


    endtime = time.time()
    totaltime = endtime - s_time
    print(totaltime)



