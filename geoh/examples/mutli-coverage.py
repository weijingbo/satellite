from geojson_utils import draw_circle
from skyfield import api
from skyfield.api import Loader
import h3
import json
import time
import math
import threading

TLE_URL = 'https://celestrak.com/NORAD/elements/starlink.txt'
R_MEAN = 6378.1  # 轨道的平均半径
MIN_TERMINAL_ANGLE_DEG = 35  # 从地面能看到卫星的角度
ANGLE = 25
GEOHASH_LEVEL = 3  # geohash的等级，等级越高，geohash被划分的越精细，计算成本越高
H3_LEVEL = 4
maxthread = 10


class CacSatellite(threading.Thread):
    def __init__(self, satName, sat, threadID):
        threading.Thread.__init__(self)
        self.name = satName
        self.sat = sat
        self.threadID = threadID

    def run(self):
        sat_location = (self.sat.latitude.degrees, self.sat.longitude.degrees,)
        angle = calcCapAngle(self.sat.elevation.km, ANGLE)
        if angle == -1:
            # print(self.name)
            pass
        rad = R_MEAN * angle * 1000
        try:
            pt_center = json.loads(
                '{"type": "Point", "coordinates":[' + str(sat_location[0]) + ',' + str(sat_location[1]) + ']}')
            circle = draw_circle(rad, pt_center, 15)['coordinates'][0]
            first_point = circle[0]
            circle.append(first_point)
            strlist = '{"type":"Polygon","coordinates":[[' + ','.join('%s' % id for id in circle) + ']]} '
            circlejson = json.loads(strlist)
            circleset = h3.polyfill(circlejson, H3_LEVEL, geo_json_conformant=False)
            # print(circleset)
        except:
            pass


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
        # print("this satellite can not calculate")
        return -1


if __name__ == '__main__':
    s_time = time.time()
    geojson = {
        'type': 'Polygon',
        'coordinates': [[[0.0, 0.0], [180, 0.0], [180.0, 30.0], [0.0, 30.0], [0.0, 0.0]]]}
    geoset = h3.polyfill(geojson, H3_LEVEL, geo_json_conformant=False)
    # print("geoset:", geoset)

    load = Loader('./tle_cache')
    sats = load.tle_file(url=TLE_URL)
    print("共加载了{}颗卫星".format(len(sats)))
    ts = api.load.timescale()
    now = ts.now()
    subpoints = {sat.name: sat.at(now).subpoint() for sat in sats}
    thread_list = []

    threading.BoundedSemaphore(maxthread)
    a = 0
    for sat_name, sat in subpoints.items():
        t = CacSatellite(sat_name, sat, "1")
        thread_list.append(t)
        a=a+1
        if(a==100):
            break
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()
    end_time = time.time() - s_time
    print(end_time)