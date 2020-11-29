# 小组信息

- 组员信息：陈天诚（组长）、童邦凡
- 组员分工：陈天诚（数据库搭建、函数编写、代码实现），童邦凡（功能测试、编写注释、文档补充）
- 指导老师：彭伟龙

# 作业题目和内容

## 题目

广州大学某班有同学100人，现要从两个数据源汇总学生数据。第一个数据源在Excel中，第二个数据源在txt文件中，两个数据源课程存在缺失、冗余和不一致性，请用C/C++/Java/Python程序实现对两个数据源的一致性合并以及每个学生样本的数值量化。

- Excel表：ID (int), 姓名(string), 家乡(string:限定为Beijing / Guangzhou / Shenzhen / Shanghai), 性别（string:boy/girl）、身高（float:单位是cm)）、课程1成绩（float）、课程2成绩（float）、...、课程10成绩(float)、体能测试成绩（string：bad/general/good/excellent）；其中课程1-课程5为百分制，课程6-课程10为十分制。
- txt文件：ID(string：6位学号)，性别（string:male/female）、身高（string:单位是m)）、课程1成绩（string）、课程2成绩（string）、...、课程10成绩(string)、体能测试成绩（string：差/一般/良好/优秀）；其中课程1-课程5为百分制，课程6-课程10为十分制。

## 参考

一.数据源1.xlsx

| ID   | Name  | City     | Gender | Height | C1   | ...  | C10  | Constitution |
| ---- | ----- | -------- | ------ | ------ | ---- | ---- | ---- | ------------ |
| 1    | Marks | Shenzhen | boy    | 166    | 77   |      |      | general      |
| 2    | Wayne | Shenzhen | girl   | 159    | 77   |      |      | good         |
| ...  | ...   | ...      | ...    | ...    | ...  | ...  | ...  | ...          |



一.数据源2-逗号间隔.txt

ID,Name,City,Gender,Height,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,Constitution
202001,Marks,Shenzhen,male,1.66,77,100,84,71,91,6,7,6,8,,general

## 实验内容

两个数据源合并后读入内存，并统计：

1. 学生中家乡在Beijing的所有课程的平均成绩。
2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。(备注：该处做了修正，课程10数据为空，更改为课程9)
3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）

## **提示**

参考数据结构：

Student{

int id;

string id;

vector<float> data;

}


可能用到的公式：

| 均值公式                 |                             img1                             |
| :----------------------- | :----------------------------------------------------------: |
| **协方差公式**           | **[img2](https://github.com/TCchen-CS/MachineLearningExperiment/raw/master/实验报告一/Screenshots/2.png)** |
| **z-score规范化**        |                           **img3**                           |
| **数组A和数组B的相关性** |                           **img4**                           |

注意：计算部分不能调用库函数；画图/可视化显示可以用可视化API或工具实现。

# 作业环境

+ Windows10

+ Anaconda Python3.8.5（IDE为pycharm）

## 文件说明

+ 源代码
  - 「AddData.py」功能：将<一.数据源1.xlsx>表格导入到MySQL数据库
  - 「LoadSqlData.py」功能：从数据库中将数据源1读取为<一.数据源1_NEW.xlsx>
  - 「txtToExcel.py」功能：将文本<一.数据源2-逗号间隔.txt>文件转换为Excel表格的<一.数据源2_NEW.xlsx>文件
  - 「MergeList.py」功能：将之前生成的<一.数据源1_NEW.xlsx>与<一.数据源2_NEW.xlsx>合并为一张表<合并数据源.xlsx>
  - 「DealData.py」功能：处理已合成的数据，解决提出的问题
+ 文件夹「resources」存放数据源文件
  - 「一.数据源1.xlsx」：数据源1
  - 「一.数据源2-逗号间隔.txt」：数据源2
+ 文件夹「Processing_source」存放数据源的处理结果
  - 「一.数据源1_NEW.xlsx」：新数据源1
  - 「一.数据源2_NEW.xlsx」：新数据源2
  - 「合并数据源.xlsx」：最终合并数据结果
+ 文件夹「result」存放运行结果截图
  + 输出合并后数据源
  + 输出学生中家乡在Beijing的所有课程的**平均成绩**
  + 输出学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的**数量**
  + 输出比较广州和上海两地女生的平均体能测试成绩并判断哪个地区的更强些
  + 输出学习成绩和体能测试成绩两者的**相关性**

## 函数说明

### 定义一个写excel表的方法

```python
    def write(self, data_path, sheetname, value):
        index = len(value)
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = sheetname
        for i in range(0, index):
            for j in range(0, len(value[i])):
                sheet.cell(row=i + 1, column=j + 1, value=str(value[i][j]))
        workbook.save(data_path)
        print("xlsx格式表格写入数据成功！")

        workbook.close()
```

将写入结果保留到data_path路径当中

### 定义一个读数据库的方法

```python
    def read(self, table):
        try:
            sql = "select * from " + table
            self.cursor.execute(sql)#执行sql语句查表
            self.connect.commit()#向MySQL服务器提交当前事务
            description = self.cursor.description#获取每个字段的属性域名
            title = []

            # 取表的各表头
            for data in description:
                title.append(data[0])

            datas = [] #存表内容

            # 取表的内容
            for row in self.cursor.fetchall():#fetchall函数返回多个元组
                sheelData = {}
                for col in range(len(row)):
                    sheelData[title[col]] = row[col]
                datas.append(sheelData)
            return datas
        except Exception as e:
            print(str(e))
            print("数据读取错误")
```



### getCount

```python
def getCount(key, value):
    """设置一个条件及关键词，返回满足该条件的关键词的列表"""
    In_City = df[df[key] == value]
    return In_City
```



### score

```
def score(Con_City):
    sum = 0
    people_sum = Con_City.count();
    for i in Con_City:
        if i == 'good':
            sum += 2
        elif i == 'general':
            sum += 0
        elif i == 'bad':
            sum += -1
        else:
            people_sum -= 1
    return sum, people_sum
```



### 体能成绩量化函数

```
def score(key):
    """将体能成绩量化：good=2, general=0, bad=-1"""
    sum = []
    for i in df[key]:
        if i == 'good':
            sum.append(2)
        elif i == 'general':
            sum.append(0)
        elif i == 'bad':
            sum.append(-1)
        else:
            sum.append(0)
    return sum
```



### 计算平均值函数

```
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
```



### 标准差函数

```
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
    return (result / (len(list)+nan_num)) ** 0.5
```



### 计算A'函数

```
def course(row):
    """计算A‘ ：计算 a’ = (ak-mean(A))/std(A)"""
    list_a = []
    for col in df[row]:
        if math.isnan(col):
            list_a.append((80 - Avg(df[row])) / Cov(df[row]))
        else:
            list_a.append((col - Avg(df[row])) / Cov(df[row]))
    return list_a
```



### 计算B'函数

```
def b():
    """计算B‘ ：计算 b’ = (bk-mean(B))/std(B)"""
    num = score('Constitution')
    sumb = []
    for col in num:
        sumb.append((col - Avg(num)) / Cov(num))
    return sumb

```



### 相关性函数

```
def correlation():
    """计算相关性；correlation(A,B) = A'* B' """
    key = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    list_b = b()

    # 用课程每一列与体能成绩做相关性计算即：n*9矩阵 与 n*1矩阵 相乘
    for i in range(len(key)):
        list_a = course(key[i])
        for e in range(len(list_a)):
            sum = 0 # 计算结果
            # 一维矩阵做相乘
            for col in range(len(list_b)):
                temp = list_a[col] * list_b[col] # 点积
                if math.isnan(list_a[col]):
                    print("发现nan")
                sum += temp
        print("\n%s 与 Constitution 的相关系数：%s" % (key[i], temp))
```



## 调用的函数库以及涉及哪些技术

### 函数库

+ ```python
  import xlrd
  ```

+ ```python
  import MySQLdb
  ```

+ ```python
  import openpyxl
  ```

+ ```python
  import pymysql
  ```

+ ```python
  from openpyxl import Workbook
  ```

- ```python
  import pandas as pd
  ```

- ```python
  import os
  ```

- ```python
  import math
  ```

### 涉及的技术

| 调用的函数        | 函数说明 |
| ----------------- | -------- |
| open_workbook     |          |
| sheet_by_name     |          |
| MySQLdb.connect   |          |
| cursor            |          |
| cursor.execute    |          |
| cursor.close      |          |
| database.commit   |          |
| database.close    |          |
| openpyxl.Workbook |          |
| openpyxl.active   |          |
| openpyxl.save     |          |
|                   |          |
|                   |          |
|                   |          |

# 难题与解决

前言：非常惭愧做本次实验基本是从0开始，除了理解实验要求不是难题，其余一切代码实现几乎都是难题，无论是简单的导入还是复杂的清洗、合并、查询，都花费了大量的时间和精力用于各种百度上，也从中收集了一些个人认为很不错的文章，同时也在源代码中做好了标记，下面会根据标记处所遇到的问题以及解决办法罗列在下方，今后一定洗心革面好好学习天天向上

## *1

### [\# Numpy的基础知识](https://mp.weixin.qq.com/s?__biz=MjM5MDEzNDAyNQ==&mid=402378855&idx=1&sn=77ed3c403aa00977e66a6d712b565f44&scene=21#wechat_redirect)

### [# Panda的基础知识](https://mp.weixin.qq.com/s?__biz=MjM5MDEzNDAyNQ==&mid=402568021&idx=1&sn=66d5234a31f2de640baa71439f856a33&scene=21#wechat_redirect)

## *2

### [\# 数据导入](https://mp.weixin.qq.com/s?__biz=MjM5MDEzNDAyNQ==&mid=402829681&idx=1&sn=3042132921889b2b5414fff28513b05b&scene=21#wechat_redirect)

### [\# .drop_duplicates 用法说明](https://www.cnblogs.com/yaos/p/9837448.html)

### [\# SettingwithCopyWarning（不加.copy()会报警告的原因）](https://blog.csdn.net/xiaofeixia666888/article/details/106807181)

## *3

### [\# Pandas中把数据格式（df,array）的相互转换](https://blog.csdn.net/weixin_43708040/article/details/87275815)

### [\# numpy对象折叠成一维的数组1](https://blog.csdn.net/likeyou1314918273/article/details/89735607)

### [\# numpy对象折叠成一维的数组2](https://www.pythonheidong.com/blog/article/430164/3f1749c78e817b2d3ec0/)

### [\# 替换异常值](https://mp.weixin.qq.com/s?__biz=MjM5MDEzNDAyNQ==&mid=2650313425&idx=1&sn=72ebfbe60eb592e5b36aa0fd71c508d5&scene=21#wechat_redirect)

## *4

### [\# 去除空格](https://mp.weixin.qq.com/s?__biz=MjM5MDEzNDAyNQ==&mid=2650313491&idx=1&sn=08d3dcaf1bace4265691fa7541c05727&scene=21#wechat_redirect)

## *5

### [\# 如何在Python中从dataframe列的字符串中删除非字母数字字符？](https://www.cnpython.com/qa/61821)

## *6

### [# 数据合并](https://mp.weixin.qq.com/s?__biz=MjM5MDEzNDAyNQ==&mid=2650313362&idx=1&sn=3d8b068493098a942241fbe8662a81b9&scene=21#wechat_redirect)

## *7

### [\# 用一个数据源的数据填充另一个数据源的缺失值](https://www.cnblogs.com/yuxiangyang/p/11286394.html)

## *8

### [\# 有缺失值默认给float类型](https://www.cnblogs.com/everfight/p/10855654.html)

## *9

### [\# Pandas 查询选择数据](https://www.gairuo.com/p/pandas-selecting-data)	

## *10

### [pandas--将字符串属性转换为int型](https://blog.csdn.net/weixin_43486780/article/details/105601526)

## *额外

### [\# git语法](https://www.liaoxuefeng.com/wiki/896043488029600)

# 总结

本次实验所要求的内容并不复杂，难就难在代码实现上，由于没有什么基础可言，90%的时间都拿去搜索各种文档恶补相关知识去了，可谓是受益匪浅，了解到了Python中的Numpy库以及Pandas库，也在不断捣鼓的过程中摸索出了一些相通的方法，第一次将项目推到GitHub上，也开始意识到要对自己写出的代码负责，这份沉甸甸的责任感使我不断优化自身代码，虽然学习Git语法也花费了我不少时间，整个实验花费了远多于以往实验的精力和时间，但结果总归是好的，相信接下来的实验会更加有的放矢更加得心应手，期间非常感谢彭老师的悉心指导