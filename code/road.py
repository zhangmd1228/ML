import pandas as pd
# from timechance import *
# from DBSCAN import *
# from sklearn.cluster import DBSCAN
# import matplotlib.pyplot as plt
import numpy as np

def road():
    # 读取csv文件，道路的拓扑结构
    # data = pd.read_csv(r'D:\Pycharm\untitled\2.csv', encoding='UTF-8', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    # data = data[data['z_order'] > 0]
    data = pd.read_csv(r'D:\Pycharm\untitled\test\ROAD.csv', encoding='UTF-8')
    data = data[data['POINT_X'] > 100]  # 过滤掉经纬度不合理的道路
    grouped = data.groupby('osm_id')    # 按照道路编号分组，不同的道路分成不同组内
    # print(len(grouped))
    for name, group in grouped:       # 根据不同的道路分组情况画出各自的道路图
        plt.plot(group["POINT_X"], group["POINT_Y"], 'k', linewidth=0.2)
    # plt.xlim(120.173, 120.20)
    # plt.ylim(35.95, 35.97)
    # pl.show()

def road2():
    # 读取csv文件，道路的拓扑结构
    data = pd.read_csv(r'D:\Pycharm\untitled\2.csv', encoding='UTF-8', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    data = data[data['z_order'] > 0]
    grouped = data.groupby('osm_id')    # 按照道路编号分组，不同的道路分成不同组内
    # print(len(grouped))
    for name, group in grouped:       # 根据不同的道路分组情况画出各自的道路图
        plt.plot(group["POINT_X"], group["POINT_Y"], 'k', linewidth=0.2)
    # plt.xlim(120.173, 120.20)
    # plt.ylim(35.95, 35.97)
    # pl.show()

def GetCrossAngle(l1, l2):
    arr_0 = np.array([(l1.p2.x - l1.p1.x), (l1.p2.y - l1.p1.y)])
    arr_1 = np.array([(l2.p2.x - l2.p1.x), (l2.p2.y - l2.p1.y)])
    cos_value = (float(arr_0.dot(arr_1)) / (np.sqrt(arr_0.dot(arr_0)) * np.sqrt(arr_1.dot(arr_1))))   # 注意转成浮点数运算
    return np.arccos(cos_value) * (180/np.pi)

# data = pd.read_csv('2.csv', encoding='UTF-8', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
# building = pd.read_csv('building.csv', encoding='UTF-8', usecols=[2, 11, 12])    # 建筑物名称，经纬度坐标
# building.dropna(axis=0, how='any', inplace=True)          # 删除行中数据有空值的行数据
# print(building)
#
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
# for h in range(len(building)):
#     plt.scatter(building.iloc[h]['POINT_X'], building.iloc[h]['POINT_Y'], linewidths=0, marker=".", c='k')
#     a = building.iloc[h]['POINT_X']
#     b = building.iloc[h]['POINT_Y']
#     # 前两个参数是x，y轴坐标,第三个参数是要显式的内容,alpha透明度
#     plt.text(a, b + 0.0001, "%s" % (building.iloc[h]['name']), ha='center', va='bottom', fontsize=6, alpha=0.6)
#
# data = data[data['z_order'] > 0]
# grouped = data.groupby('osm_id')  # 按照道路编号分组，不同的道路分成不同组内
# # print(len(grouped))
# for name, group in grouped:       # 根据不同的道路分组情况画出各自的道路图
#     plt.plot(group["POINT_X"], group["POINT_Y"], 'k', linewidth=0.2)
# plt.xlim(120.173, 120.20)
# plt.ylim(35.95, 35.97)
# pl.show()
