# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from DealData import score

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# matplotlib画图中中文显示会有问题，需要这两行设置默认字体

plt.xlabel('C1')
plt.ylabel('Constitution')
plt.xlim(xmax=100, xmin=0)
plt.ylim(ymax=2.5, ymin=-2.5)
# 画两条（0-9）的坐标轴并设置轴标签x，y
import pandas as pd

df = pd.read_excel('.\合并数据源.xlsx', sheet_name='Sheet', header=0)

x = df['C1'].values

y = score('Constitution')

colors1 = '#00CED1'  # 点的颜色


area = np.pi * 3 ** 2  # 点面积
# 画散点图
plt.scatter(x, y, s=area, c=colors1, alpha=0.4,label = 'score')

plt.plot([0, 15], [15, 0], linewidth='0.5', color='#000000')
plt.legend()
plt.savefig(r'./result/1.png', dpi=300)
plt.show()