"""
    本文件功能：处理已合成的数据，解决提出的问题
    1.	学生中家乡在Beijing的所有课程的平均成绩。
    2.	学生中家乡在广州，课程1在80分以上，且课程10在9分以上的男同学的数量。
    3.	比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
    4.	学习成绩和体能测试成绩，两者的相关性是多少？
"""
import math

import pandas as pd

df = pd.read_excel('./Processing_source/合并数据源.xlsx', sheet_name='Sheet', header=0)


def getCount(key, value):
    """设置一个条件及关键词，返回满足该条件的关键词的列表"""
    In_City = df[df[key] == value]
    return In_City


# 一.家乡在Beijing的所有人的成绩
print('\n学生中家乡在Beijing的所有课程的平均成绩：')

In_Beijing = getCount('City', 'Beijing')
Beijing_len = In_Beijing['ID'].count()

for i in range(0, Beijing_len):
    sum = 0
    for j in range(5, 14):
        if float(In_Beijing.iloc[i][j]) > 0:
            sum = sum + float(In_Beijing.iloc[i][j])
        else:
            sum += 0
    print('ID:%s\tName:%8s\tGrade_Avg= %0.3f' % (In_Beijing.iloc[i][0], In_Beijing.iloc[i][1], sum / 9))
print("===========================")

# 二. 查找学生中家乡在广州，课程1在80分以上，且课程10在9分以上的男同学
In_Guangzhou = getCount('City', 'Guangzhou')
In_Shanghai = getCount('City', 'Shanghai')

print('\n学生中家乡在广州，课程1在80分以上，且课程10在9分以上的男同学的数量:')
boy = In_Guangzhou[In_Guangzhou['Gender'] == 'boy']  # 1.取性别为男的人
C1_80 = boy[boy['C1'] > 80]  # 2.取C1成绩过80的人
C2_9 = C1_80[C1_80['C9'] > 9]  # 3.取C9成绩过9的人
print("数量：%s" % C2_9['ID'].count())  # 输出满足条件的同学数目
print(C2_9)  # 输出满足条件的同学列表
print("===========================")

# 三. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
Con_GZ = In_Guangzhou['Constitution']
Con_Sh = In_Shanghai['Constitution']


# excellent = 2, good = 1, general = 0, bad =-1.
def score(Con_City):
    sum = 0
    people_sum = Con_City.count();
    for i in Con_City:
        if i == 'excellent':
            sum += 2
        elif i == 'good':
            sum += 1
        elif i == 'general':
            sum += 0
        elif i == 'bad':
            sum += -1
        else:
            people_sum -= 1
    return sum, people_sum


score_GZ, people_GZ = score(Con_GZ)
score_Sh, people_Sh = score(Con_Sh)
print("\ngood:2, general:0, bad:-1")
print("两地平均体能测试成绩：  广州：%0.3f    上海：%0.3f" % (score_GZ / people_GZ, score_Sh / people_Sh))
if score_GZ > score_Sh:
    print("即 广州 平均体能测试成绩更佳")
else:
    print("即 上海 平均体能测试成绩更佳")

print("===========================")


# 四.学习成绩和体能测试成绩，两者的相关性是多少？
def score(key):
    """将体能成绩量化：excellent = 2, good = 1, general = 0, bad =-1."""
    sum = []
    for i in df[key]:
        if i == 'excellent':
            sum.append(2)
        elif i == 'good':
            sum.append(1)
        elif i == 'general':
            sum.append(0)
        elif i == 'bad':
            sum.append(-1)
        else:
            sum.append(0)
    return sum


def Avg(list):
    """计算平均值 avg(a)=（a1+a2+……+an)/n"""
    sum = 0
    nan_num = 0
    for i in list:
        if math.isnan(i):
            nan_num += 1
        else:
            sum += i
    return sum / (len(list) - nan_num)


def Cov(list):
    """计算标准差s
    协方差：s**2 = ((x1-avg(x))**2+(x2-avg(x))**2+……+(xn-avg(xn))**2)/(n-1)
    """
    result = 0
    nan_num = 0
    for i in list:
        if math.isnan(i):
            nan_num += 1
        else:
            result += (i - Avg(list)) ** 2
    return (result / (len(list) + nan_num)) ** 0.5


def course(row):
    """计算A‘ ：计算 a’ = (ak-mean(A))/std(A)"""
    list_a = []
    for col in df[row]:
        if math.isnan(col):
            list_a.append((80 - Avg(df[row])) / Cov(df[row]))
        else:
            list_a.append((col - Avg(df[row])) / Cov(df[row]))
    return list_a


def b():
    """计算B‘ ：计算 b’ = (bk-mean(B))/std(B)"""
    num = score('Constitution')
    sumb = []
    for col in num:
        sumb.append((col - Avg(num)) / Cov(num))
    return sumb


def correlation():
    """计算相关性；correlation(A,B) = A'* B' """
    key = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    list_b = b()

    # 用课程每一列与体能成绩做相关性计算即：n*9矩阵 与 n*1矩阵 相乘
    for i in range(len(key)):
        list_a = course(key[i])
        for e in range(len(list_a)):
            sum = 0  # 计算结果
            # 一维矩阵做相乘
            for col in range(len(list_b)):
                temp = list_a[col] * list_b[col]  # 点积
                if math.isnan(list_a[col]):
                    print("发现nan")
                sum += temp
        print("\n%s 与 Constitution 的相关系数：%s" % (key[i], temp))


correlation()
