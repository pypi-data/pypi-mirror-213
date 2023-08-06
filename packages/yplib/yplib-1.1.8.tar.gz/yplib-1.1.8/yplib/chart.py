from yplib.chart_html import *
from yplib.index import *


# 将 html 中的占位符 替换成数据
# 并且 导出 生成后的 html 文件
def insert_data_to_chart(html_data='',
                         chart_name=None,
                         x_list=None,
                         y_list=None,
                         legend=None,
                         series=None):
    p_list = [
        'chart_name', 'x_list', 'y_list', 'legend', 'series'
    ]
    p_data_list = [
        chart_name, x_list, y_list, legend, series
    ]
    for index in range(len(p_list)):
        one_p = p_list[index]
        one_data = p_data_list[index]
        if one_data is None:
            continue
        one_p = f'-{one_p}-'
        if one_p in html_data:
            html_data = html_data.replace(one_p, str(one_data))
    to_txt(list_data=[html_data],
           file_name=str(chart_name),
           file_path='html',
           fixed_name=False,
           suffix='.html')
    # current_path = os.path.abspath(__file__)
    # html_list = open(current_path[0:current_path.find('__init__')] + 'line-stack-temp.html', 'r', encoding='utf-8').readlines()


# 将数据整理成折线图
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#             {
#                 name: 'Email',
#                 hide: False,
#                 data: [120, 132, 101, 134, 90, 230, 210],
#             },
#             {
#                 name: 'Union Ads',
#                 hide: 0,
#                 data: [220, 182, 191, 234, 290, 330, 310],
#             },
#             {
#                 name: 'Video Ads',
#                 hide: True,
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
def to_chart(x_list, y_list, chart_name='line_stack'):
    # data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
    legend_data = []
    legend_selected = {}
    for y_one in y_list:
        legend_data.append(y_one['name'])
        if 'hide' in y_one:
            legend_selected[y_one['name']] = 0
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

    insert_data_to_chart(html_data=line_stack_html(),
                         chart_name=chart_name,
                         x_list=x_list,
                         legend=legend,
                         series=series)


# 将数据整理成折线图
# 一条折线
# 数据 : data_list = [
#             ['2020-01-01', 132],
#             ['2021-01-01', 181],
#             ['2022-01-01', 147]
#         ]
# x_index : x 轴数据的下标
# y_index : y 轴数据的下标
def to_chart_one(list_data, chart_name='line', is_area=False, x_index=0, y_index=1):
    x_list = []
    y_list = []
    for d_one in list_data:
        x_list.append(d_one[x_index])
        y_list.append(d_one[y_index])
    if is_area:
        insert_data_to_chart(html_data=line_area_html(),
                             chart_name=chart_name,
                             x_list=x_list,
                             y_list=y_list)
    else:
        to_chart(x_list, [{'name': chart_name, 'data': y_list}], chart_name=chart_name)


# legend_data.append(y_one['name'])
#     if 'hide' in y_one:
#         legend_selected[y_one['name']] = 0
# legend = "data : " + str(legend_data) + ", selected : " + str(legend_selected)
# # {
# #     name: 'Email',
# #     type: 'line',
# #     stack: 'Total',
# #     data: [120, 132, 101, 134, 90, 230, 210],
# # }
# series = []
# for y_one in y_list:
#     y_one['type'] = 'line'
#     y_one['stack'] = 'Total'
#     series.append(y_one)
#
# insert_data_to_chart(html_data=line_stack_html(),
#                      chart_name=chart_name,
#                      x_list=x_list,
#                      legend=legend,
#                      series=series)


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
    x_list = []
    if isinstance(data_list[0], list):
        for one in data_list:
            x_list.append({'name': one[0], 'value': one[1]})
    else:
        x_list = data_list
    insert_data_to_chart(html_data=pie_html(),
                         chart_name=chart_name,
                         x_list=x_list)


# 将数据整理成柱状图
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
# 或者
# 数据 : data = [
#        {x: "Search Engine", y: 1048 },
#        {x: "Direct", y: 735 },
#        {x: "Email", y:580 },
#        {x: "Union Ads", y:484 },
#        {x: "Video Ads", y:300 }
#       }]
def to_chart_bar(data_list, chart_name='bar'):
    x_list = []
    y_list = []
    for one in data_list:
        if isinstance(one, list):
            x_list.append(one[0])
            y_list.append(one[1])
        else:
            x_list.append(one['x'])
            y_list.append(one['y'])

    insert_data_to_chart(html_data=bar_html(),
                         chart_name=chart_name,
                         x_list=x_list,
                         y_list=y_list)

# data = []
# # for i in range(10):
# #     data.append([uuid_random(), int(random.uniform(0, 1000))])
# for i in range(10000):
#     one = {}
#     one['x'] = uuid_random()
#     one['y'] = int(random.uniform(0, 1000))
#     data.append(one)
#
# to_chart_bar(data)

#
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

# x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y_list = json.loads(
#     '[{"name":"Email","data":[120,132,101,134,90,230,210]},{"name":"Union Ads","data":[220,182,191,234,290,330,310]},{"name":"Video Ads","data":[150,232,201,154,190,330,410]},{"name":"Direct","data":[320,332,301,334,390,330,320]},{"name":"Search Engine","data":[820,932,901,934,1290,1330,1320]}]')
#

# # # 将 list 转化成 图表的例子
# x_list = []
# y_list = []
# # # x 轴有 100 个
# # # 100 个横坐标
# for i in range(100):
#     x_list.append(i)
# #
# # 有 10 条线
# for i in range(1):  # 0 1 2 3 4 55
#     n = {}
#     n['name'] = str(int(random.uniform(0, 1000)))
#     data = []
#     # 每条线有 100 个纵坐标, 与 x_list 中的对应起来
#     for i in range(100):
#         data.append(int(random.uniform(0, 1000)))
#     n['data'] = data
#     # n['hide'] = '1'
#     y_list.append(n)
# #
# to_chart(x_list, y_list)
#

# data_list = []
# for i in range(100000):
#     data_list.append([i, int(random.uniform(0, 1000))])
#
# to_chart_one(list_data=data_list, is_area=True)

# print('end')
