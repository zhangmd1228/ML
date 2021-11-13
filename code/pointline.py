import numpy as np
from road import *
from geopy.distance import geodesic
import math
from decimal import *

def pointline(point, point1, point2):
    result = pd.DataFrame(columns=('subpoint', 'distance'))

    array_longi = np.array(point2) - np.array(point1)  # 表示一条向量
    array_trans = np.array(point) - np.array(point1)  # point1为两个向量点的起始点

    # 用向量计算点到直线距离
    array_temp = (float(array_trans.dot(array_longi)) / array_longi.dot(array_longi))  # 注意转成浮点数运算 dot表示矩阵相乘
    array_temp = array_longi.dot(array_temp)
    subpoint = np.array(point1) + np.array(array_temp)  # 投影点的坐标
    distance = np.sqrt((array_trans - array_temp).dot(array_trans - array_temp))
    result = result.append(pd.DataFrame({'subpoint': [subpoint], 'distance': [distance], 'before': [point1],
                                        'after': [point2]}), sort=False, ignore_index=True)
    return result

def getDist_P2L(point, point1, point2):
    global DIS1
    result = pd.DataFrame(columns=('subpoint', 'distance'))
    A = point1[1] - point2[1]
    B = point2[0] - point1[0]
    C = point1[0]*point2[1] - point1[1]*point2[0]
    if B == 0:
        distance = abs(point[0] - point1[0])
        subpoint = [point1[0], point[1]]
    else:
        m = -A / B
        b = -C / B
        # 计算点在直线上投影点
        x1 = (float(m * point[1] + point[0] - m * b) / float(m ** 2 + 1))
        y1 = (float(m ** 2 * point[1] + m * point[0] + b) / float(m ** 2 + 1))
        distance = (float(abs(A * point[0] + B * point[1] + C))) / (float((A * A + B * B) ** 0.5))
        subpoint = [x1, y1]
        DIS1 = geodesic((point[1], point[0]), (y1, x1)).m
    result = result.append(pd.DataFrame({'subpoint': [subpoint], 'distance': [distance], 'before': [point1],
                                         'after': [point2], 'DIS': [DIS1], 'fangx': [point[2]*2]}), sort=False, ignore_index=True)
    return result

def getAngle(point1, point2):
    radLatA = math.radians(point1[1])          # radians() 方法将角度转换为弧度
    radLonA = math.radians(point1[0])
    radLatB = math.radians(point2[1])
    radLonB = math.radians(point2[0])
    dLon = radLonB - radLonA
    y = math.sin(dLon) * math.cos(radLatB)
    x = math.cos(radLatA) * math.sin(radLatB) - math.sin(radLatA) * math.cos(radLatB) * math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))      # degrees()将弧度转换为角度
    brng = (brng + 360) % 360
    return brng

