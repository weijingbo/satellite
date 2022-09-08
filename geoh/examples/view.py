# -*- coding: utf-8 -*-
import geopandas
from shapely import geometry
import matplotlib.pyplot as plt

#保存在本地的geoJson数据
data = geopandas.read_file('mygeojson.json')#修改一下路径

cq = geopandas.GeoSeries([geometry.Point([116.0, 39.0])],crs='EPSG:4326')#默认wgs1984坐标系
#生成图表
fig, ax = plt.subplots()
data.to_crs(crs='EPSG:4524').plot(ax=ax, color="#4C92C3",alpha=0.8)
cq.to_crs(crs='EPSG:4524').plot(ax=ax, color='orange', markersize=100, marker='*')
plt.xticks(rotation=20)
plt.savefig("MapDisplayAndprojection.png")#修改一下路径
plt.show()
