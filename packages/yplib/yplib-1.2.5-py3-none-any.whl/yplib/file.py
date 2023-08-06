from yplib.index import *


# 有关文件的操作
# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
# param list
# return list
def get_file(file_path=None, prefix=None, contain=None, suffix=None):
    if file_path is None:
        file_path = os.path.dirname(os.path.abspath('.'))
    list_data = []
    get_file_all(file_path, list_data, prefix, contain, suffix)
    return list_data


# 是否包含指定的文件
def contain_file(file_path=None, prefix=None, contain=None, suffix=None):
    return len(get_file(file_path, prefix, contain, suffix)) > 0


# 在指定的文件夹中查找包含指定字符串的数据
# file_path : 文件路径
# find_str : 查找的字符串
# from_last : 是否从文件的最后开始查找
def get_file_data_line(file_path=None, find_str='find_str', from_last=True):
    file_list = get_file(file_path)
    for one_file in file_list:
        one_list = to_list(one_file)
        index = 0
        if from_last:
            index = len(one_list) - 1
        while -1 < index < len(one_list):
            one_line = one_list[index]
            if from_last:
                index -= 1
            else:
                index += 1
            if one_line.find(find_str) > -1:
                return one_line
    return None


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_file_all(file_path, list_data, prefix=None, contain=None, suffix=None):
    if os.path.isdir(file_path):
        for root, dir_names, file_names in os.walk(file_path):
            for file_name in file_names:
                if get_file_check(file_name, prefix, contain, suffix):
                    list_data.append(os.path.join(root, file_name))
            for dir_name in dir_names:
                get_file_all(os.path.join(root, dir_name), list_data)
    elif get_file_check(file_path, prefix, contain, suffix):
        list_data.append(file_path)


# 检查文件是否符合要求
def get_file_check(file_name='', prefix=None, contain=None, suffix=None):
    if file_name is None or file_name == '':
        return False
    p = True
    c = True
    s = True
    if prefix is not None:
        if file_name.startswith(prefix):
            p = True
        else:
            p = False
    if contain is not None:
        if file_name.find(contain) > -1:
            c = True
        else:
            c = False
    if suffix is not None:
        if file_name.endswith(suffix):
            s = True
        else:
            s = False
    return p and c and s


# 检查文件内容是否包含指定的字符串
# 慎用,否则, 执行时间可能比较长
def find_file_by_content(file_path='', contain_txt=None, prefix=None, contain=None, suffix=None):
    list_file = get_file(file_path, prefix, contain, suffix)
    if len(list_file) == 0:
        to_log(f'no_matched_file : {file_path} , {contain_txt} , {prefix} , {contain} , {suffix}')
        return False
    if contain_txt is None:
        to_log(list_file)
        return True
    for one_file in list_file:
        try:
            text_file = open(one_file, 'r', encoding='utf-8')
            for line in text_file.readlines():
                if line.find(contain_txt) > -1:
                    if line.endswith('\n'):
                        line = line[0:-1]
                    to_log(one_file, line)
        except Exception as e:
            to_log(one_file, e)
            continue

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
