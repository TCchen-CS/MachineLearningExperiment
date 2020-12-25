# 实验二《数据统计和可视化》

## 小组信息

- 组员信息：陈天诚（组长）、童邦凡
- 组员分工：陈天诚（绘制散点图、直方图、数据量化归一化），童邦凡（计算相关矩阵、可视化混淆矩阵、临近矩阵）
- 指导老师：彭伟龙

## 作业题目和内容

### **题目**

基于**实验一**中清洗后的数据练习统计和视化操作，100个同学（样本），每个同学有11门课程的成绩（11维的向量）；那么构成了一个100x11的数据矩阵。以你擅长的语言C/C++/Java/Python/Matlab，编程计算：

1. 请以课程1成绩为x轴，体能成绩为y轴，画出散点图。
2. 以5分为间隔，画出课程1的成绩直方图。
3. 对每门成绩进行z-score归一化，得到归一化的数据矩阵。
4. 计算出100x100的相关矩阵，并可视化出混淆矩阵。（为避免歧义，这里“协相关矩阵”进一步细化更正为100x100的相关矩阵，100为学生样本数目，视实际情况而定）
5. 根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）输出到txt文件中，以\t,\n间隔。

### 提示

计算部分不能调用库函数；画图/可视化显示可可视化工具或API实现。

## 作业环境

- Windows10
- Anaconda Python3.8.5（IDE为pycharm）

## 文件说明

- 源代码
  - 「Paint1.py」功能：绘制散点图
  - 「Paint2.py」功能：绘制直方图
  - 「DealData.py」功能：对实验一清洗后的数据进行量化、归一化以及相关的计算公式
  - 「CorralationMatrix.py」功能：对成绩量化、保存，计算相关矩阵，并可视化出混淆矩阵
  - 「NearDemo.py」功能：根据相关矩阵找到距离每个样本最近的三个样本，得到100*3的矩阵

- 文件夹
  - 「result」存放散点图和直方图

- 文档

  - 「合并数据源.xlsx」即实验一的合并数据结果

  - 「归一化数据.txt」存放量化后且归一化的数据
  - 「相关矩阵.txt」存放第四题结果相关矩阵
  - 「最近矩阵.txt」存放第五题结果矩阵

## 函数说明

### 协方差函数

```python
# 计算两个学生的协方差
def Cov(df1, df2):
    result = 0
    for i in range(len(df1)):
        result += (df1[i]-Avg(df1))*(df2[i]-Avg(df2))
    return result/(len(df1)-1)
```

### 标准差函数

```python
# 计算单个学生成绩的标准差
def Std(df):
    sum = 0
    for i in range(len(df)):
        sum += ((df[i] - Avg(df))**2)/(len(df)-1)
    return sqrt(sum)
```

### 相关系数函数

```python
# 相关系数函数
def Coefficient(df1,df2):
    return Cov(df1,df2)/(Std(df1)*Std(df2))
```

### 相关矩阵函数

```python
# 相关矩阵函数
def correlation_matrix(df):
        result = np.zeros((len(df),len(df)))
        for i in range(len(df)):
            for j in range(len(df)):
                result[i][j] = Coefficient(df[i],df[j])
        return resultPython
```

## 调用的库函数

- ```python
  import math
  ```

- ```Python
  import pandas as pd
  ```

- ```python
  import numpy as np
  ```

- ```python
  import matplotlib.pyplot as plt
  ```

- ```python
  import pandas as pd
  ```

- ```python
  from numpy import *
  ```

- ```python
  import seaborn as sb
  ```

- ```python
  import matplotlib.pyplot as mat
  ```

## 难题与解决

### 数据处理

将数据源里的数据读取出来

还要将其转化称为可计算的矩阵

将体育成绩量化，原本的体育成绩是以’excellent‘、’good‘等字符，量化前无法参与计算

### 100*100的相关矩阵

之前不了解题目的目的

是需要求每一位同学的每一科成绩之间的相关性？

还是要求同学与同学之间的相关性？

参考了里面关于计算相关系数的部分代码

https://github.com/Chi2B/Data-Mining

***感谢陈泽彬同学的悉心解惑***

## 总结

矩阵计算之前需要将成绩量化成可计算的值，否则计算无从谈起。

通过计算相关矩阵，可以罗列出每位同学之间的相关系数，进而可以通过可视化工具将其形象展示出来。

自己与自己的相关系数永远是1。