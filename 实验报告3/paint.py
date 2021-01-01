# 导入所需库
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 用来正常显示中文标签（①）
plt.rcParams['font.sans-serif']=['SimHei']

# 为保证各类颜色相同，定义一个颜色数组
color = ['green', 'yellow', 'red', 'black', 'blue', 'purple']

f = open("./data/k=5.txt") #改文件名称即可

line = "1"
data = []

# 读取文件内容到data[]数组中
while line:
    line = f.readline()
    if line:
        int_data = [float(i) for i in (line.replace("\n","").split(" ", 6))]
        data.append(int_data)

Data = np.array(data)

maxClass = np.max(Data[:,2])             # 类数目k


indexClass = Data[:,2]      # 类索引


x_centerClass = [0.0,0.0,0.0,0.0,0.0]   # 类质心x
y_centerClass = [0.0,0.0,0.0,0.0,0.0]   # 类质心y
for i in range(len(data)):
    ClassNum = int(data[i][2])
    x_centerClass[ClassNum] = float(data[i][4])
    y_centerClass[ClassNum] = float(data[i][5])


maxRadius = [0.0,0.0,0.0,0.0,0.0]       # 定义半径
# 找该类的半径
for i in range(len(data)):
    Class = int(data[i][2])
    distance = float(data[i][3])
    if distance>maxRadius[Class]:
        maxRadius[Class] = distance


# 画图
def plot(maxClass,x_centerClass,y_centerClass):
    # 初始坐标列表
    x = []
    y = []
    for i in range(int(maxClass)+1):
        x.append([])
        y.append([])

    # 填充坐标 并绘制散点图
    for j in range(int(maxClass)+1):
        for i in range(len(indexClass)):
            if int(indexClass[i])== j:
                x[j].append(data[i][0])
                y[j].append(data[i][1])

        plt.scatter(x[j], y[j], c=color[j],marker='o',label=("类别%d" % (j + 1)))

        if(j==(maxClass - 1)):
            plt.scatter(x_centerClass[j], y_centerClass[j], c='red', marker='*', label="中心点")  # 画聚类中心
        else:
            plt.scatter(x_centerClass[j], y_centerClass[j], c='red', marker='*')  # 画聚类中心
    # 画出类半径
    for i in range(int(maxClass)+1):
        # 定义圆心和半径
        x = x_centerClass[i]
        y = y_centerClass[i]
        r = maxRadius[i]
        # 点的横坐标为a
        a = np.arange(x - r, x + r, 0.0001)
        # 点的纵坐标减掉质心的y为b
        b = np.sqrt(abs(pow(r, 2) - pow((a - x), 2)))
        # 绘制上半部分
        plt.plot(a, y + b, color=color[i], linestyle='-')
        # 绘制下半部分
        plt.plot(a, y - b, color=color[i], linestyle='-')
    plt.scatter(2, 6, c='violet', marker='x', label="(2,6)")  # 画（2，6）
    # 设置标题
    plt.title('K-means Scatter Diagram')
    # 给图加上图例
    plt.legend()
    # 设置X轴标签
    plt.xlabel('X')
    # 设置Y轴标签
    plt.ylabel('Y')
    # 显示散点图
    plt.show()

plot(maxClass,x_centerClass,y_centerClass)

f.close()