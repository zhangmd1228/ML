import pandas as pd
from timechance import *
from road import *
from pointline import *
import math
import time
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import DBSCAN
from pandas.core.frame import DataFrame
import numpy as np

# 读取csv文件，GPS数据信息
data = pd.read_csv(r'D:\Pycharm\untitled\2151.csv', usecols=[14, 16, 19, 20, 21, 22, 24, 33])
# 读取csv文件，道路的拓扑结构
roaddata = pd.read_csv(r'D:\Pycharm\untitled\2.csv', encoding='UTF-8', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
roaddata = roaddata[roaddata['z_order'] > 0]
# 数据预处理，删去空缺数据的行
data.dropna(axis=0, how='any', inplace=True)          # 删除行中数据有空值的行数据

# 数据预处理，不合理的异常无效数据去掉，保留合理的符合要求的数据
data = data[(120.17 < data['JDZB']) & (data['JDZB'] < 120.21) & (35.95 < data['WDZB']) & (data['WDZB'] < 35.97)]
data = data[data['GPSSD'] < 100]          # GPS速度小于100千米每小时
data = data.drop_duplicates(subset=None, keep='first', inplace=False)   # 去掉重复数据的情况

# 包含某个字符，contains检查开始字符串，endswith检查结束字符串
data = data[data.GPSSJ.str.contains("30-JUL-17 ")]

# 时间提取
sj = data['GPSSJ'].tolist()           # 一列值的获取,[]内为列名
times = timechance(sj)                ### 时间转换，将时间转化为以秒为单位的数据
data['TIME'] = times["sj"]            # 把时间值增加为新的一列数据，作为时间索引

# 数据按照序列号聚类，这里只针对车辆数据.csv   因为做了空间切分，单辆车的序列号也就断了
a = data.index.tolist()             # 数据的索引作为list列表
b = [1 for j in range(len(data))]
X = list(zip(a, b))                 # 组成二维列表用于后面的聚类
# print(X)
y_pred = DBSCAN(eps=10, min_samples=2).fit_predict(X)      # DBSCAN聚类,对序列号进行聚类，按道理来说最好对时间进行聚类
# print(y_pred)
plt.scatter(a[:], b[:], linewidths=0, c=y_pred)            # 对序列号聚类画出结果图，可以看出紫色开始，黄色结束
plt.show()

grouped = roaddata.groupby('osm_id')                 # 按照道路编号分组，不同的道路分成不同组内
ppall = pd.DataFrame(columns=('POINT_X', 'POINT_Y'))
for name, group in grouped:                          # 根据不同的道路分组情况找出节点之间最大距离值
    pp = pd.DataFrame(columns=('POINT_X', 'POINT_Y'))
    pp['POINT_X'] = abs(group['POINT_X'].diff())
    pp['POINT_Y'] = abs(group['POINT_Y'].diff())
    pp.dropna(axis=0, how='all', inplace=True)
    ppall = pd.concat([ppall, pp], ignore_index=True)
uu = max(ppall['POINT_X'])            # x轴的范围的最小值
tt = max(ppall['POINT_Y'])            # y轴的范围的最小值
# print(uu, tt)


# GPS数据点的平移，这个问题还待考虑，为什么一定需要平移？到底问题出在哪里？---坐标系原因，转换坐标系后不需要再平移了
df = pd.DataFrame([], columns=['jdzb', 'wdzb'])
df["fx"] = data.FX                   # 添加一维方向数据，提高匹配准确率
df["time"] = data.TIME
df["jdzb"] = data.JDZB-0.0051
df["wdzb"] = data.WDZB-0.0002         # 为了ArcGis匹配地图自动更改坐标系，相当于平移

# 查找聚类后每一类里面的元素地址
list_address = []
t0 = time.time()
for i in y_pred.tolist():                 # 遍历聚类结果，聚类结果是1到12（或更大）的聚类成每一组的序号，离散点表示为-1
    address_index = [x for x in range(len(y_pred.tolist())) if y_pred.tolist()[x] == i]
    list_address.append([i, address_index])         # i为聚类的后的组号，address_index为聚类的每一组的序号，这里序号已经不是以前的数据序号了
dict_address = dict(list_address)                   # 转化为字典形式，i为索引，address_index为聚类后i包含的序号

for i in range(max(y_pred)):                        # 取最大的组号
    road2()                                         ### 作道路的底图
    yy = dict_address[i]                            # 取组号的序号，为作图准备

    at = df.iloc[yy]['time'].tolist()                       # 数据的时间作为list列表
    bt = [1 for u in range(len(data))]
    Xt = list(zip(at, bt))                                  # 组成二维列表用于后面的聚类
    t_pred = DBSCAN(eps=10, min_samples=1).fit_predict(Xt)  # DBSCAN聚类,对序列号进行聚类，按道理来说最好对时间进行聚类
    # print(t_pred)                                           # 按照时间聚类，由紫色变成黄色表示车辆的行驶方向

    pointall = []
    for k in range(len(yy)):                                # 遍历路线的每一个点，一个点一个点的进行地图匹配
        point = [df.iloc[yy[k]]['jdzb'], df.iloc[yy[k]]['wdzb'], df.iloc[yy[k]]['fx']]           # point待匹配的点
        pointall.append(point)                              # 存放所有待匹配点的数据
        dataa = roaddata[(point[0] - uu < roaddata['POINT_X']) & (roaddata['POINT_X'] < point[0] + uu)
                         & (point[1] - tt < roaddata['POINT_Y']) & (roaddata['POINT_Y'] < point[1] + tt)]
        grouped = dataa.groupby('osm_id')                              # 按照道路编号分组，不同的道路分成不同组内
        plineall = pd.DataFrame()                                      # 提取这段路上的所有点（可省略）
        for name, group in grouped:                                        # 根据不同的道路分组情况进行道路匹配
            zipped = list(zip(group["POINT_X"].tolist(), group["POINT_Y"].tolist()))     # 道路节点
            plinepart = pd.DataFrame()                                 # 存放一条道路每个节点间的匹配数据
            for l in range(len(zipped)-1):                                   # 遍历每个节点
                pline = getDist_P2L(point, zipped[l], zipped[l + 1])         #### 进行道路匹配算法，计算投影点与投影距离
                plinepart = plinepart.append(pline, ignore_index=True)       # 存放一条道路每个节点间的匹配数据
            plineall = plineall.append(plinepart, ignore_index=True)         # 存放所有道路每个节点间的匹配数据
            # 显示所有列
            pd.set_option('display.max_columns', None)
        # print(plineall)
        opline = plineall
        opline['road'] = None  # 添加空列
        opline['angle'] = None      # 添加空列
        opline['weight'] = None  # 添加空列
        for t in range(len(plineall)):
            if (plineall.loc[t]['DIS'] > 50) | (max(dist(plineall.loc[t]['subpoint'], plineall.loc[t]['before']),
                    dist(plineall.loc[t]['subpoint'], plineall.loc[t]['after'])) >
                    dist(plineall.loc[t]['before'], plineall.loc[t]['after'])):  # 当投影点在两节点之外，不符合条件
                opline = opline.drop(t)                                          # 不符合条件的数据应该删除
            else:
                direction = getAngle(plineall.loc[t]['before'], plineall.loc[t]['after'])  ### 进行道路方位角的判断
                angle = direction - plineall.loc[t]['fangx']
                if angle < -180:
                    angle = 360 + angle
                elif angle > 180:
                    angle = 360 - angle
                else:
                    angle = angle
                opline.loc[t, 'angle'] = angle
                opline.loc[t, 'road'] = direction
                # math.cos必须要配合弧度制math.radians()
                opline.loc[t, 'weight'] = 0.3 / opline.loc[t]['DIS'] + 0.7 * math.cos(math.radians(opline.loc[t]['angle']))
        o = opline[opline['weight'] == max(opline['weight'])]
        print(opline)
        plt.plot(o['subpoint'].tolist()[0][0], o['subpoint'].tolist()[0][1], marker=".", c='r')
        # print(angle)
        # print(o.distance)
        # print(o['subpoint'].tolist()[0])
        # print(point)
    # print(pointall)

    plt.scatter(df.iloc[yy]['jdzb'], df.iloc[yy]['wdzb'], linewidths=0, marker=".", c=t_pred)

    plt.xlim(120.173, 120.20)
    plt.ylim(35.95, 35.97)                          # 为了方便观察，观察局部视图
    # plt.xlim(120.174, 120.19)
    # plt.ylim(35.95, 35.96)                          # 为了方便观察，观察局部视图
    pl.show()
t = time.time()-t0
print(t)


