import hashlib
import uuid

import requests
import random
from yplib import *

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



# print(get_file_data_line(r'D:\notepad_file\202306\fasdfsadfaf.txt', 'a'))

# get_file_data_line(r'D:\notepad_file\202306', 'a')
# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))


# print('end')