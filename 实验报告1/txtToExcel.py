"""
功能：将文本<一.数据源2-逗号间隔.txt>文件转换为Excel表格的<一.数据源2_NEW.xlsx>文件
"""

from openpyxl import Workbook
#导入openpyxl包
wb = Workbook()#创建一个excel
sheet = wb.active#获取当前excel的sheet
datas = None#定义一个空值,接收score.txt的参数

with open("./resources/一.数据源2-逗号间隔.txt","r") as fr :#读取上面txt的数据,这里我的txt文本命名为score.txt
    datas = fr.readlines()#readlines函数返回一个字符串列表，每个元素为fr的一行内容

ID_late = ''
i = 0#行数，初始值为0

#遍历datas的长度,100行
for x in range(len(datas)):
    #对每一行的data数据按“,”切分，获取到每一个学生的信息
    ID,Name,City,Gender,Height,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,Constitution = datas[x].split(",")
    if ID_late == ID:
        continue
    else:
        ID_late = ID

    #按行输入学生信息
    row = str(i + 1)
    sheet["A" + row] = ID
    sheet["B" + row] = Name
    sheet["C" + row] = City

    # 将性别更改为统一格式
    if Gender == 'male':
        sheet["D" + row] = 'boy'
    elif Gender == 'female':
        sheet["D" + row] = 'girl'
    else:
        sheet["D" + row] = Gender

    #将身高更改为统一格式
    if Height == 'Height':
        sheet["E" + row] = Height
    elif float(Height) >= 100:
        sheet["E" + row] = float(Height)
    elif float(Height) <= 10:
        sheet["E" + row] = float(Height) * 100

    #按行输入学生成绩
    sheet["F" + row] = C1
    sheet["G" + row] = C2
    sheet["H" + row] = C3
    sheet["I" + row] = C4
    sheet["J" + row] = C5
    sheet["K" + row] = C6
    sheet["L" + row] = C7
    sheet["M" + row] = C8
    sheet["N" + row] = C9
    sheet["O" + row] = C10
    sheet["P" + row] = Constitution.strip()#使用strip（）去掉末尾的换行符\n

    #每录完一个学生，行数加一
    i += 1

#保存excel名字随意,后缀要注意
wb.save("./Processing_source/一.数据源2_NEW.xlsx")

