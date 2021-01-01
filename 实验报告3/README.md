# 实验三《k-means聚类算法》

## 小组信息

- 组员信息：陈天诚（组长）、童邦凡
- 组员分工：陈天诚（数据处理及程序算法实现，文档编写），童邦凡（文档校验）
- 指导老师：彭伟龙

## 作业题目和内容

### **题目**

用C++实现k-means聚类算法，

1. 对实验二中的z-score归一化的成绩数据进行测试，观察聚类为2类，3类，4类，5类的结果，观察得出什么结论？
2. 由老师给出测试数据，进行测试，并画出可视化出散点图，类中心，类半径，并分析聚为几类合适。

样例数据(x,y)数据对：

| 3.45 | 7.08 |
| :--: | :--: |
| 1.76 | 7.24 |
| 4.29 | 9.55 |
| 3.35 | 6.65 |
| 3.17 | 6.41 |
| 3.68 | 5.99 |
| 2.11 | 4.08 |
| 2.58 | 7.10 |
| 3.45 | 7.88 |
| 6.17 | 5.40 |
| 4.20 | 6.46 |
| 5.87 | 3.87 |
| 5.47 | 2.21 |
| 5.97 | 3.62 |
| 6.24 | 3.06 |
| 6.89 | 2.41 |
| 5.38 | 2.32 |
| 5.13 | 2.73 |
| 7.26 | 4.19 |
| 6.32 | 3.62 |

找到聚类中心后，判断(2,6)是属于哪一类？

### 注意

除文件读取外，不能使用C++基础库以外的API和库函数。

## 作业环境

- Windows10
- Anaconda Python3.8.5（IDE为pycharm）
- VS2017

## 文件说明

- 源代码
  - 「Kmeans」K-means实现的源代码
  - 「paint.py」可视化出散点图，类中心，类半径

- 文件夹
  - 「data」存放生成的归一化数据以及生成的结果数据
- 「result」存放结果截图
  

## 函数说明

### 构造函数

```c++
//构造函数
KMeans::KMeans(int dimNum, int clusterNum)
{
	m_dimNum = dimNum;
	m_clusterNum = clusterNum;

	m_means = new double*[m_clusterNum];
	for (int i = 0; i < m_clusterNum; i++)
	{
		m_means[i] = new double[m_dimNum];
		memset(m_means[i], 0, sizeof(double) * m_dimNum);
	}

	m_initMode = InitRandom;
	m_maxIterNum = 100;
	m_endError = 0.001;
}
```

### 析构函数

```c++
//析构函数
KMeans::~KMeans()
{
	for (int i = 0; i < m_clusterNum; i++)
	{
		delete[] m_means[i];
	}
	delete[] m_means;
}
```

### 初始化函数

```c++
//初始化
void KMeans::Init(double *data, int N)
{
	int size = N;

	if (m_initMode == InitRandom)
	{
		int inteval = size / m_clusterNum;
		double* sample = new double[m_dimNum];

		// Seed the random-number generator with current time
		srand((unsigned)time(NULL));

		for (int i = 0; i < m_clusterNum; i++)
		{
			int select = inteval * i + (inteval - 1) * rand() / RAND_MAX;
			for (int j = 0; j < m_dimNum; j++)
				sample[j] = data[select*m_dimNum + j];
			memcpy(m_means[i], sample, sizeof(double) * m_dimNum);
		}

		delete[] sample;
	}
	else if (m_initMode == InitUniform)
	{
		double* sample = new double[m_dimNum];

		for (int i = 0; i < m_clusterNum; i++)
		{
			int select = i * size / m_clusterNum;
			for (int j = 0; j < m_dimNum; j++)
				sample[j] = data[select*m_dimNum + j];
			memcpy(m_means[i], sample, sizeof(double) * m_dimNum);
		}

		delete[] sample;
	}
	else if (m_initMode == InitManual)
	{
		// Do nothing
	}
}
```

### 归类函数

```c++
//N 为特征向量数
void KMeans::Cluster(double *data, int N, int *Label, double *maxDis, double *center)
{
	int size = 0;
	size = N;

	assert(size >= m_clusterNum);

	// Initialize model
	Init(data, N);

	// Recursion
	double* x = new double[m_dimNum];	// Sample data
	int label = -1;		// Class index
	double iterNum = 0;
	double lastCost = 0;
	double currCost = 0;
	int unchanged = 0;
	bool loop = true;
	int* counts = new int[m_clusterNum];
	double** next_means = new double*[m_clusterNum];	// New model for reestimation
	for (int i = 0; i < m_clusterNum; i++)
	{
		next_means[i] = new double[m_dimNum];
	}

	while (loop)
	{
		memset(counts, 0, sizeof(int) * m_clusterNum);
		for (int i = 0; i < m_clusterNum; i++)
		{
			memset(next_means[i], 0, sizeof(double) * m_dimNum);
		}

		lastCost = currCost;
		currCost = 0;

		// Classification
		for (int i = 0; i < size; i++)
		{
			for (int j = 0; j < m_dimNum; j++)
				x[j] = data[i*m_dimNum + j];

			currCost += GetLabel(x, &label);

			counts[label]++;
			for (int d = 0; d < m_dimNum; d++)
			{
				next_means[label][d] += x[d];
			}
		}
		currCost /= size;

		// Reestimation
		for (int i = 0; i < m_clusterNum; i++)
		{
			if (counts[i] > 0)
			{
				for (int d = 0; d < m_dimNum; d++)
				{
					next_means[i][d] /= counts[i];
				}
				memcpy(m_means[i], next_means[i], sizeof(double) * m_dimNum);
			}
		}

		// Terminal conditions
		iterNum++;
		if (fabs(lastCost - currCost) < m_endError * lastCost)
		{
			unchanged++;
		}
		if (iterNum >= m_maxIterNum || unchanged >= 3)
		{
			loop = false;
		}

		//DEBUG
		//cout << "Iter: " << iterNum << ", Average Cost: " << currCost << endl;
	}

	// Output the label file


	for (int i = 0; i < size; i++)
	{
		for (int j = 0; j < m_dimNum; j++)
		{
			x[j] = data[i*m_dimNum + j];
			
		}

		maxDis[i] = GetLabel(x, &label);//点到类中心的距离
		Label[i] = label;//属于哪个类
		center[i*m_dimNum + 0] = m_means[label][0];
		center[i*m_dimNum + 1] = m_means[label][1];
		
	}
	
	delete[] counts;
	delete[] x;
	for (int i = 0; i < m_clusterNum; i++)
	{
		delete[] next_means[i];
	}
	delete[] next_means;
}
```

```python

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
```

## 调用的库函数

```c++
#C++
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <iostream>
#include <assert.h>
```

```python
# python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
```

## 难题与解决

[文件的读取](https://blog.csdn.net/mengdicfm/article/details/82910642)

[numpy的数组](https://www.runoob.com/numpy/numpy-array-manipulation.html)

[C++实现K-均值（K-Means）聚类算法](https://blog.csdn.net/lavorange/article/details/28854929 )

[绘制散点图](https://www.cnblogs.com/Pythonmiss/p/10631709.html  )

## 总结

#### 		本次实验采取两种语言实现，k-means算法采用要求的c++语言实现，数据的可视化采用python实现。题目一需要实验二的归一化数据，最终两题的数据结果存在对应的txt文件里，第二题中根据可视化结果显示，当数据分为 两 类时，效果最为明显。