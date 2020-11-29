"""
功能：
将之前生成的<一.数据源1_NEW.xlsx>与<一.数据源2_NEW.xlsx>合并为一张表<合并数据源.xlsx>
"""

import pandas as pd
import xlrd
import os

writer = pd.ExcelWriter('./Processing_source/合并数据源.xlsx')#创建一个writer对象，参数为写入路径

os.chdir('./')#在当前文件目录下寻找合并文件源

#获取两个数据源表的文件路径
path1 = './Processing_source/一.数据源1_NEW.xlsx'
path2 = './Processing_source/一.数据源2_NEW.xlsx'

#将数据源1读出为s1
workbook1 = xlrd.open_workbook(path1)
s1 = pd.read_excel(path1, sheet_name='Sheet')
#将数据源2读出为s2
workbook2 = xlrd.open_workbook(path2)
s2 = pd.read_excel(path2, sheet_name='Sheet')

#合并s1和s2
S11=(s1.combine_first(s2))#使用s2表的数据补全s1空缺内容并临时存放在S11当中
S = pd.merge(S11,s2,"outer")#将S11与s2进行外连接，将s1原本缺少的学生添加进来
#去重， keep="first" ： 保留重复的第一个值， sort_values参数：1）以‘ID’做排序  2）True为升序
S.drop_duplicates(subset=['ID'], keep='first').sort_values(['ID'],ascending=True).to_excel(writer,'Sheet',index=False)

#保存合并表
writer.save()