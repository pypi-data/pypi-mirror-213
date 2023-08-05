# name = "yplib"

import json
import os
import uuid
from datetime import datetime

import xlrd
import xlwt
# import random
from yplib.line_stack_temp import line_stack_temp_html


# 记录日志, 如果是对象会转化为 json
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


# 将 log 数据, 写入到文件
def log_to_file(a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
                a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    lo = log(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20)
    list_to_txt([lo], datetime.today().strftime('%Y-%m-%d'), 'log', True)


# 是否能用 json
def can_use_json(data):
    if isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set):
        return True
    return False


# 检查文件夹是否存在,不存在,就创建新的
def check_file(file_name):
    if file_name != '' and os.path.exists(file_name) is False:
        os.mkdir(file_name)


# 获得文件名称
def get_file_name(file_name, suffix='.txt'):
    return str(file_name) \
        + '_' + datetime.today().strftime('%Y%m%d_%H%M%S') \
        + '_' + str(uuid.uuid4().hex).replace('-', '')[0:5] \
        + suffix


# 去掉 str 中的 非数字字符, 然后, 再转化为 int
def str_to_int(s):
    if s is None or s == '':
        return 0
    return int(''.join(filter(lambda ch: ch in '0123456789', s)))


# 去掉 str 中的 非数字字符, 然后, 再转化为 float
def str_to_float(s):
    if s is None or s == '':
        return 0.0
    return float(''.join(filter(lambda ch: ch in '0123456789.', s)))


# 将 list 中的数据以 json 或者基本类型的形式写入到文件中
# list_data : 数组数据
# file_name : 文件名
# fixed_name : 是否固定文件名
# file_path : 文件路径
def list_to_txt(list_data, file_name, file_path='data', fixed_name=False, suffix='.txt'):
    file_name = str(file_name)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    file_name = file_name + suffix
    if fixed_name is False:
        file_name = get_file_name(file_name, suffix)
    file_name_path = file_name
    if file_path != '':
        file_name_path = file_path + '/' + file_name
    text_file = open(file_name_path, 'a', encoding='utf-8')
    for one in list_data:
        if can_use_json(one):
            s = json.dumps(one)
        else:
            s = str(one)
        text_file.write(s + '\n')
    text_file.close()
    return file_name_path


# 将 list 中的数据写入到固定的文件中,自己设置文件后缀
def list_to_txt_fixed_file_name(list_data, file_name):
    return list_to_txt(list_data, file_name, '', True)


# 将 txt 文件读取到 list 中, 每一行自动过滤掉行前,行后的空格
def txt_to_list(file_name):
    file = open(file_name, 'r', encoding='utf-8')
    data_all = list()
    for line in file.readlines():
        line = line.strip()
        data_all.append(line)
    return data_all


def list_to_excel(list_data, file_name, file_path='data'):
    file_name = str(file_name)
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


# 将数据整理成折线图
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#             {
#                 name: 'Email',
#                 selected: False,
#                 data: [120, 132, 101, 134, 90, 230, 210],
#             },
#             {
#                 name: 'Union Ads',
#                 selected: 0,
#                 data: [220, 182, 191, 234, 290, 330, 310],
#             },
#             {
#                 name: 'Video Ads',
#                 data: [150, 232, 201, 154, 190, 330, 410],
#             },
#             {
#                 name: 'Direct',
#                 data: [320, 332, 301, 334, 390, 330, 320],
#             },
#             {
#                 name: 'Search Engine',
#                 data: [820, 932, 901, 934, 1290, 1330, 1320],
#             },
#         ]
def to_chart(x_list, y_list, chart_name='stack_line'):
    # current_path = os.path.abspath(__file__)
    # html_list = open(current_path[0:current_path.find('__init__')] + 'line-stack-temp.html', 'r', encoding='utf-8').readlines()
    html_list_one = line_stack_temp_html()
    chart_name_html = '-chart_name-'
    x_list_html = '-x_list-'
    legend_html = '-legend-'
    series_html = '-series-'
    r_list = []
    # data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
    legend_data = []
    legend_selected = {}
    for y_one in y_list:
        legend_data.append(y_one['name'])
        if 'selected' in y_one:
            legend_selected[y_one['name']] = 'false'
    legend = "data : " + str(legend_data) + ", selected : " + str(legend_selected)
    # {
    #                 name: 'Email',
    #                 type: 'line',
    #                 stack: 'Total',
    #                 data: [120, 132, 101, 134, 90, 230, 210],
    #             }
    series = []
    for y_one in y_list:
        y_one['type'] = 'line'
        y_one['stack'] = 'Total'
        series.append(y_one)

    one_line = html_list_one
    if one_line.find(chart_name_html) > -1:
        one_line = one_line.replace(chart_name_html, str(chart_name))
    if one_line.find(x_list_html) > -1:
        # ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        one_line = one_line.replace(x_list_html, str(x_list))
    if one_line.find(legend_html) > -1:
        one_line = one_line.replace(legend_html, str(legend))
    if one_line.find(series_html) > -1:
        one_line = one_line.replace(series_html, str(series))
    r_list.append(one_line)
    list_to_txt(r_list, str(chart_name), 'html', False, '.html')


# list_to_txt([1,2,3], 'p')
# list_to_txt_fixed_file_name([1,2,3], 'p')
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
#
# x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y_list = json.loads(
#     '[{"name":"Email","data":[120,132,101,134,90,230,210]},{"name":"Union Ads","data":[220,182,191,234,290,330,310]},{"name":"Video Ads","data":[150,232,201,154,190,330,410]},{"name":"Direct","data":[320,332,301,334,390,330,320]},{"name":"Search Engine","data":[820,932,901,934,1290,1330,1320]}]')
#
# x_list = []
# y_list = []
#
# # to_chart(x_list, y_list)
#
# # x 轴有 100 个
# # 100 个横坐标
# for i in range(100):
#     x_list.append(i)
#
# # 有 10 条线
# for i in range(10):  # 0 1 2 3 4 55
#     n = {}
#     n['name'] = str(int(random.uniform(0, 1000)))
#     data = []
#     # 每条线有 100 个纵坐标, 与 x_list 中的对应起来
#     for i in range(100):
#         data.append(int(random.uniform(0, 1000)))
#     n['data'] = data
#     y_list.append(n)
#
# to_chart(x_list, y_list)


# log_to_file(1)
# log_to_file(12)
# log_to_file('yangpu')
# print(str_to_int('yan123gpu'))
# print(str_to_float('yan123gpu'))
# print(str_to_float('yan123g.12pu'))
