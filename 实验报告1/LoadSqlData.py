"""
从数据库中将数据源1读取为<一.数据源1_NEW.xlsx>
"""

#excel操作
import openpyxl

class ExcelData():

    # 定义一个写excel表的方法
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


#数据库操作
import pymysql


class DB():
    #初始化构造函数
    def __init__(self,User,Password,database):
        #链接数据库
        self.connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user=User,
            passwd=Password,
            db=database,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    #定义一个读数据库的方法
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

# user_name= input("用户名:")
# password = input("密码:")
# database = input("数据库名：")
# tablename = input("表名:")
user_name= 'root'
password = 'root'
database = 'testdb'
tablename = 'stu'


#将数据库导出为excel
db = DB(user_name,password,database) #定义一个数据库对象
excel = ExcelData() #定义一个excel数据对象

values = db.read(tablename)#读取数据库中学生表stu数据保存至values

title = []#存放表头
tmp = values[0]
for key in tmp:
    title.append(key)

toValue = []#存放学生数据表
toValue.append(title)

#按行取每位学生的数据，存进toValue
for value in values:
    tmp = []
    for key in value:
        if key == "ID":
            value[key] += 202000
        tmp.append(value[key])
    toValue.append(tmp)

#将toValue数据写入excel表
excel.write("./Processing_source/一.数据源1_NEW.xlsx", "Sheet", toValue)
