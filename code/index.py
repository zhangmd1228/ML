import pandas as pd
from timechance import timechance


def get_data():
    data = pd.read_csv("data/0901.csv")
    # 数据预处理，删去空缺数据的行
    data.dropna(axis=0, how='any', inplace=True)          # 删除行中数据有空值的行数据

    # 数据预处理，不合理的异常无效数据去掉，保留合理的符合要求的数据
    data = data[(120.17 < data['JDZB']) & (data['JDZB'] < 120.21) & (35.95 < data['WDZB']) & (data['WDZB'] < 35.97)]
    data = data[data['GPSSD'] < 100]          # GPS速度小于100千米每小时
    data = data.drop_duplicates(subset=None, keep='first', inplace=False)   # 去掉重复数据的情况
    # 时间提取
    sj = data['GPSSJ'].tolist()           # 一列值的获取,[]内为列名
    times = timechance(sj)                ### 时间转换，将时间转化为以秒为单位的数据
    data['TIME'] = times["sj"]            # 把时间值增加为新的一列数据，作为时间索引
    print(data)
    return data
