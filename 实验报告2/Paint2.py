# matplotlib模块绘制直方图
# 读入数据
import pandas as pd
import matplotlib.pyplot as plt

Titanic = pd.read_excel('.\合并数据源.xlsx')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# matplotlib画图中中文显示会有问题，需要这两行设置默认字体

# 检查C1成绩是否有缺失
any(Titanic.C1.isnull())
# 不妨删除含有缺失C1成绩的观察
Titanic.dropna(subset=['C1'], inplace=True)
# 绘制直方图
plt.hist(x = Titanic.C1, # 指定绘图数据
         bins = 20, # 指定直方图中条块的个数
         range = (0,100), #指定直方图的上下界
         color = 'steelblue', # 指定直方图的填充色
         edgecolor = 'black' # 指定直方图的边框色
         )
# 添加x轴和y轴标签
plt.xlabel('分数')
plt.ylabel('人数')
# 添加标题
plt.title('课程1的成绩直方图')

plt.savefig(r'./result/2.png', dpi=300)

# 显示图形
plt.show()
