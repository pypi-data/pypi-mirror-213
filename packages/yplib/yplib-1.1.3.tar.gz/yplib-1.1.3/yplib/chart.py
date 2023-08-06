from yplib.chart_html import *
from yplib.index import *


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
    html_list_one = line_stack_html()
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
    #     name: 'Email',
    #     type: 'line',
    #     stack: 'Total',
    #     data: [120, 132, 101, 134, 90, 230, 210],
    # }
    series = []
    for y_one in y_list:
        y_one['type'] = 'line'
        y_one['stack'] = 'Total'
        series.append(y_one)

    one_line = html_list_one
    if chart_name_html in one_line:
        one_line = one_line.replace(chart_name_html, str(chart_name))
    if x_list_html in one_line:
        # ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        one_line = one_line.replace(x_list_html, str(x_list))
    if legend_html in one_line:
        one_line = one_line.replace(legend_html, str(legend))
    if series_html in one_line:
        one_line = one_line.replace(series_html, str(series))
    r_list.append(one_line)
    to_txt(r_list, str(chart_name), 'html', False, '.html')


# 将数据整理成饼状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
def to_chart_pie(data_list, chart_name='pie'):
    html_list_one = pie_html()
    data_html = '-data-'
    data_html_list = []
    if isinstance(data_list[0], list):
        for one in data_list:
            if isinstance(one, list):
                data_html_list.append({'name': one[0], 'value': one[1]})
    else:
        data_html_list = data_list

    if data_html in html_list_one:
        html_list_one = html_list_one.replace(data_html, str(data_html_list))
    to_txt([html_list_one], str(chart_name), 'html', False, '.html')


# 将数据整理成柱状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
def to_chart_bar(data_list, chart_name='bar'):
    html_list_one = pie_html()
    data_html = '-data-'
    data_html_list = []
    if isinstance(data_list[0], list):
        for one in data_list:
            if isinstance(one, list):
                data_html_list.append({'name': one[0], 'value': one[1]})
    else:
        data_html_list = data_list

    if data_html in html_list_one:
        html_list_one = html_list_one.replace(data_html, str(data_html_list))
    to_txt([html_list_one], str(chart_name), 'html', False, '.html')

#
# data = []
# # for i in range(10):
# #     data.append([uuid_random(), int(random.uniform(0, 1000))])
# for i in range(10):
#     one = {}
#     one['name'] = uuid_random()
#     one['value'] = int(random.uniform(0, 1000))
#     data.append(one)
#
# to_chart_pie(data)


# print('start')
# to_txt([1,2,3], 'p')
# to_txt_file_name([1,2,3], 'p')
#
#
# li = to_list('D:\code\python3\packaging_tutorial\yplib\data\p_20230612_095450_34779.txt')
#
# to_log()
#
# to_log()
# to_log(1)
# to_log(1, 2)
# to_log(1, 2, [1, 2])
# to_log_file(1, 2, [{'a': 2}])
# to_log_txt('1.txt', 1, 2, [{'a': 2}])
# to_txt([{'a': 2}])
# to_txt_data('yangpu', 1)
# to_txt_data('yangpu1', 1)
# to_txt_data('yangpu12', 1)
#
# x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y_list = json.loads(
#     '[{"name":"Email","data":[120,132,101,134,90,230,210]},{"name":"Union Ads","data":[220,182,191,234,290,330,310]},{"name":"Video Ads","data":[150,232,201,154,190,330,410]},{"name":"Direct","data":[320,332,301,334,390,330,320]},{"name":"Search Engine","data":[820,932,901,934,1290,1330,1320]}]')
#

# # 将 list 转化成 图表的例子
# x_list = []
# y_list = []
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
# #
# to_chart(x_list, y_list)
#
# to_txt_data(x_list, 'operate')
# to_txt_data(y_list, 'operate')

# to_log_file(1)
# log_to_file(12)
# log_to_file('yangpu')
# print(str_to_int('yan123gpu'))
# print(str_to_float('yan123gpu'))
# print(str_to_float('yan123g.12pu'))

#
# print(to_hump('user_id'))
# print(to_hump('USER_ID'))
# print(to_hump('userId'))
# print(to_hump('user'))
# print(to_hump(''))

# print(to_hump_more('userId'))

# print(to_underline('userId'))


# print(uuid_random(5))
# print(uuid_random(10))
# print(uuid_random())
# print(uuid_random(32))
# print(uuid_random(64))
# print(uuid_random(128))
# print(uuid_random(127))
# print(uuid_random(129))


# print(to_int('a'))
# print(to_int(2))
# print(to_int(2.2))
# print(to_int(2.2))

# print(to_float('a'))
# print(to_float(2))
# print(to_float(2.2))
# print(to_float(2.24))

# print(to_date('2019-09'))
# print(to_date('2019-09-08'))
# print(to_date('2019-09-08 12'))
# print(to_date('2019-09-08 12:13'))
# print(to_datetime('2019-09-08 12:13:14'))
# print(to_datetime('2019-09-08 12:13:14.789'))
# print(to_datetime(1686537485))
# print(to_datetime(1686537484467))
# print(to_datetime(datetime.today()))
#
# print(do_md5())
# print(do_md5())
# print(do_md5('yangpu'))
# print(do_md5('yangpu12'))
#
# log_msg = ''
# headers = {'Content-Type': 'application/json;charset=utf-8'}
# data = {}
# data['merchantId'] = "merchantId"
# data['currency'] = "IDR"
# data['accType'] = "payout"
# data['version'] = "1.0"
# sign = sort_by_json_key(data)
# print(sign)
# hash = hashlib.sha256()
# hash.update(sign.encode('utf-8'))
# data['sign'] = hash.hexdigest()
#
# print(data)


# print(get_file_data_line(r'D:\notepad_file\202306\fasdfsadfaf.txt', 'payout', from_last=False))

# get_file_data_line(r'D:\notepad_file\202306', 'a')
# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))


# print('end')
