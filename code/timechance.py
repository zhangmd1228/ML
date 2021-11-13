def timechance(m):
    ri = [];yue = [];nian = [];shi = [];fen = [];miao = [];apm = [];sj = []
    for i in range(len(m)):
        ri.append(int(m[i][0:2]))     # 日
        yue.append(m[i][3:6])         # 月
        nian.append(int(m[i][7:9]))   # 年
        shi.append(int(m[i][10:12]))  # 时
        fen.append(int(m[i][13:15]))  # 分
        miao.append(float(m[i][16:22]))  # 秒
        apm.append(m[i][23:25])          # 上午下午
        if apm[i] == 'PM' and shi[i] != 12:
            shi[i] = shi[i] + 12
        if apm[i] == 'AM' and shi[i] == 12:          # 12AM凌晨,12PM中午要区分好
            shi[i] = shi[i] - 12
        sj.append(shi[i] * 60 * 60 + fen[i] * 60 + miao[i])  # 时间，以秒为单位
    return {"ri": ri, "yue": yue, "nian": nian, "shi": shi, "fen": fen, "miao": miao, "sj": sj, "apm": apm}

def bustime(m):
    ri = [];yue = [];nian = [];shi = [];fen = [];miao = [];sj = []
    for i in range(len(m)):
        ri.append(m[i] / 1000000 % 100)     # 日
        yue.append(m[i] / 100000000 % 100)     # 月
        nian.append(int(m[i] / 10000000000))   # 年
        shi.append(int(m[i] / 10000 % 100))  # 时
        fen.append(int(m[i] / 100 % 100))  # 分
        miao.append(float(m[i] % 100))  # 秒
        sj.append(shi[i] * 60 * 60 + fen[i] * 60 + miao[i])  # 时间，以秒为单位
    return {"ri": ri, "yue": yue, "nian": nian, "shi": shi, "fen": fen, "miao": miao, "sj": sj}
