# 4. 计算出100x100的相关矩阵，并可视化出混淆矩阵

import pandas as pd
from numpy import *  # 导入numpy的库函数
import numpy as np  # 这个方式使用numpy的函数时，需要以np.开头。
import seaborn as sb  # 混淆矩阵
import matplotlib.pyplot as mat

# 读取数据源并转化为矩阵
data = pd.read_excel('./合并数据源.xlsx', sheet_name='Sheet', header=0)
data = pd.DataFrame({'C1': data['C1'], 'C2': data['C2'], 'C3': data['C3'], 'C4': data['C4'], \
                     'C5': data['C5'], 'C6': data['C6'], 'C7': data['C7'], 'C8': data['C8'], \
                     'C9': data['C9'], 'C10': data['C10'], 'Constitution': data['Constitution']})
df = data.values


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


# 将学生体育成绩量化
for i in range(len(df)):
    if df[i][10] == 'excellent':
        df[i][10] = 2
    elif df[i][10] == 'good':
        df[i][10] = 1
    elif df[i][10] == 'general':
        df[i][10] = 0
    elif df[i][10] == 'bad':
        df[i][10] = -1
    else:
        df[i][10] = -2

# 将第10门空成绩按0处理
for i in range(len(df)):
    df[i][9] = 0


def Cov(list):
    """计算协方差s**2
    协方差：s**2 = ((x1-avg(x))**2+(x2-avg(x))**2+……+(xn-avg(xn))**2)/(n-1)
    """
    result = 0
    nan_num = 0
    for i in list:
        if math.isnan(i):
            nan_num += 1
        else:
            result += (i - Avg(list)) ** 2
    return result / (len(list) + nan_num)


# 将归一化数据保存为txt文件
f = open("./归一化后数据.txt", "w", encoding="utf-8")
# f.write("C1"+"\t"+"C2"+"\t"+"C3"+"\t"+"C4"+"\t"+"C5"+"\t"+"C6"+"\t"+"C7"+"\t"+"C8"+"\t"+"C9"+"\t"+"C10"+"\t"+"Constitution")
# f.write("\r\n")
for i in range(len(df)):
    for j in range(len(df[i])):
        result_temp = ("%.5f" % ((df[i][j] - Avg(df[i])) / Cov(df[i])))
        f.write(str(result_temp) + " ")
    f.write("\r\n")
f.close()


# 计算两个学生的协方差
def Cov(df1, df2):
    result = 0
    for i in range(len(df1)):
        result += (df1[i] - Avg(df1)) * (df2[i] - Avg(df2))
    return result / (len(df1) - 1)


# 计算单个学生成绩的标准差
def Std(df):
    sum = 0
    for i in range(len(df)):
        sum += ((df[i] - Avg(df)) ** 2) / (len(df) - 1)
    return sqrt(sum)


# 相关系数函数
def Coefficient(df1, df2):
    return Cov(df1, df2) / (Std(df1) * Std(df2))


# 相关矩阵函数
def correlation_matrix(df):
    result = np.zeros((len(df), len(df)))
    for i in range(len(df)):
        for j in range(len(df)):
            result[i][j] = Coefficient(df[i], df[j])
    return result


# 计算相关矩阵
goldMale = correlation_matrix(df)
# 保存相关矩阵
np.savetxt(r'.\相关矩阵.txt', goldMale)
# 输出相关矩阵
print("相关矩阵：")
print(goldMale)

# 可视化混淆矩阵
df_goldMale = pd.DataFrame(goldMale)  # 矩阵转DataFrame
sb.heatmap(goldMale)  # 生成混淆矩阵（用热力图方式展示）
# 输出图像
mat.show()
