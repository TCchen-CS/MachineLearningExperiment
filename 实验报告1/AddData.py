"""
功能：将<一.数据源1.xlsx>表格导入到MySQL数据库
"""

import xlrd
import MySQLdb

# Open the workbook and define the worksheet
book = xlrd.open_workbook("./resources/一.数据源1.xlsx")
sheet = book.sheet_by_name("Sheet1")

# 建立一个MySQL连接
database = MySQLdb.connect(host="localhost", user="root", passwd="root", db="testdb")

# 获得游标对象, 用于逐行遍历数据库数据
cursor = database.cursor()

# 创建插入SQL语句
# (ID,Name,City,Gender,Height,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,Constitution)
query = "INSERT INTO stu VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题
for r in range(1, sheet.nrows):
    ID = sheet.cell(r, 0).value
    Name = sheet.cell(r, 1).value
    City = sheet.cell(r, 2).value

# Gender获取学生性别，同时整理性别的不一致性，统一用“boy”或“girl”表示
    Gender = sheet.cell(r, 3).value
    if Gender =='male':
        Gender = 'boy'
    elif Gender == 'female':
        Gender = 'girl'

# Height获取学生身高，整理身高单位的不一致性，统一用“cm”表示
    Height = sheet.cell(r, 4).value
    if Height != '' and float(Height) <= 100:
        Height = str(int(float(Height)*100))

#获取学生成绩
    C1 = sheet.cell(r, 5).value
    C2 = sheet.cell(r, 6).value
    C3 = sheet.cell(r, 7).value
    C4 = sheet.cell(r, 8).value
    C5 = sheet.cell(r, 9).value
    C6 = sheet.cell(r, 10).value
    C7 = sheet.cell(r, 11).value
    C8 = sheet.cell(r, 12).value
    C9 = sheet.cell(r,13).value
    C10 = sheet.cell(r,14).value
    Constitution = sheet.cell(r,15).value

#将获取的学生数据values导入数据库
    values = (ID,Name,City,Gender,Height,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,Constitution)
    try:
        # 执行sql语句
        cursor.execute(query, values)
    except MySQLdb._exceptions.IntegrityError:
        # 为空则抛出异常，
        print("Error: 插入失败")
    else:
        print("插入第%d数据成功！",r)


# 关闭游标
cursor.close()

# 提交
database.commit()

# 关闭数据库连接
database.close()

# 打印结果
print("成功导入！")
