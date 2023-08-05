name = "yplib"

import json
import os
import uuid
from datetime import datetime

import xlrd
import xlwt


def log(a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
        a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    l = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,
         a11, a12, a13, a14, a15, a16, a17, a18, a19, a20]
    d = ''
    for one in l:
        if can_use_json(one):
            o = json.dumps(one)
        else:
            o = str(one)
        if o != '':
            d = d + ' ' + o
    lo = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + d
    print(lo)
    return lo


# 是否能用 json
def can_use_json(data):
    if isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set):
        return True
    return False


# 检查文件夹是否存在,不存在,就创建新的
def check_file(file_name):
    if os.path.exists(file_name) is False:
        os.mkdir(file_name)


# 获得文件名称
def get_file_name(file_name, suffix='.txt'):
    return str(file_name) \
        + '_' + datetime.today().strftime('%Y%m%d_%H%M%S') \
        + '_' + str(uuid.uuid4().hex).replace('-', '')[0:5] \
        + suffix


# 将 list 中的数据以 json 或者基本类型的形式写入到文件中
# list_data : 数组数据
# file_name : 文件名
# fixed_name : 是否固定文件名
# file_path : 文件路径
def list_to_txt(list_data, file_name, file_path='data', fixed_name=False):
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    if fixed_name is False:
        file_name = get_file_name(file_name)
    text_file = open(file_path + '/' + file_name, 'a', encoding='utf-8')
    for one in list_data:
        if can_use_json(one):
            s = json.dumps(one)
        else:
            s = str(one)
        text_file.write(s + '\n')
    text_file.close()


# 将 txt 文件读取到 list 中, 每一行自动过滤掉行前,行后的空格
def txt_to_list(file_name):
    file = open(file_name, 'r', encoding='utf-8')
    data_all = list()
    for line in file.readlines():
        line = line.strip()
        data_all.append(line)
    return data_all


def list_to_excel(list_data, file_name, file_path='data'):
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 2. 创建Excel工作薄
    myWorkbook = xlwt.Workbook()
    # 3. 添加Excel工作表
    mySheet = myWorkbook.add_sheet(str(file_name))
    # 4. 写入数据
    # myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')  # 数据格式
    m = 0
    for one_data in list_data:
        n = 0
        if isinstance(one_data, list):
            for one in one_data:
                # mySheet.write(n, m, one)  # 写入A3，数值等于1
                if isinstance(one, dict) or isinstance(one, list):
                    s = json.dumps(one)
                else:
                    s = str(one)
                mySheet.write(m, n, s)  # 写入A3，数值等于1
                n += 1
        else:
            if can_use_json(one_data):
                s = json.dumps(one_data)
            else:
                s = str(one_data)
            mySheet.write(m, n, s)  # 写入A3，数值等于1
        m += 1
    # 5. 保存
    # myWorkbook.save('5002200.xls')
    myWorkbook.save(file_path + '/' + get_file_name(file_name, '.xls'))


# 将 excel 文件读取到 list 中, 单元格中的空格自动过滤掉了
def excel_to_list(file_name, sheet_index=0):
    book = xlrd.open_workbook(file_name)  # 打开一个excel
    sheet = book.sheet_by_index(sheet_index)  # 根据顺序获取sheet
    data_list = list()
    for i in range(sheet.nrows):  # 0 1 2 3 4 5
        rows = sheet.row_values(i)
        row_data = []
        for j in range(len(rows)):
            row_data.append(str(rows[j]).strip())
        data_list.append(row_data)
    return data_list


# list_to_txt([1,2,3], 'p')
#
#
# li = txt_to_list('D:\code\python3\packaging_tutorial\yplib\data\p_20230609_081711_78ff6.txt')
#
# print(log())
#
# log()
# log(1)
# log(1, 2)
# log(1, 2, [1, 2])
# log(1, 2, [{'a': 2}])
