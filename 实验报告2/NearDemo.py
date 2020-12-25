# 5. 根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）输出到txt文件中，以\t,\n间隔。

import pandas as pd
import numpy as np

#读取存放ID数据的数据源
data = pd.read_excel('./合并数据源.xlsx', sheet_name='Sheet', header=0)
data = data.values

#读取相关矩阵
correlationMatrix = np.loadtxt('相关矩阵.txt', dtype=np.float32)

#构造结果矩阵
result = np.zeros((len(data),3))

#寻找距离每个样本最近的三个样本
for i in range(len(correlationMatrix)):
    value_temp = [-1, -1, -1]   #存放已挑出来的学生序号
    ID_temp = [-1, -1, -1]      #存放结果ID
    #对于每个样本进行三次循环，每次求得一个最大相关系数
    for t in range(3):
        temp = 0    #临时存放最大值
        ID = -1     #临时存放最大值的学生序号
        for j in range(len(correlationMatrix[i])):
            #对每一个参与比较的值进行筛选，跳过自己、跳过已挑选的最大值
            if(((correlationMatrix[i][j]) != 1)and(j!=value_temp[0])and(j!=value_temp[1])and(j!=value_temp[2])):
                if(correlationMatrix[i][j])>temp:
                    temp = correlationMatrix[i][j]
                    ID = j
        value_temp[t] = correlationMatrix[i].tolist().index(temp)   #保存每一轮挑选的最大值学生序号
        ID_temp[t] = data[ID][0]                                    #保存每一轮挑选的最大值学生ID
    #将结果写入结果矩阵
    result[i] = ID_temp

#将结果矩阵写入txt
np.savetxt(r'.\最近矩阵.txt',result, fmt='%s',delimiter='\t')
print(result)

