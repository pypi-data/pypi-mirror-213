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


# 查询指定文件夹下面的所有的文件信息, 也可以是指定的文件
def get_file_all(file_path, list_data, prefix=None, contain=None, suffix=None):
    if os.path.isdir(file_path):
        for root, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                if get_file_check(filename, prefix, contain, suffix):
                    list_data.append(os.path.join(root, filename))
            for dirname in dirnames:
                get_file_all(os.path.join(root, dirname), list_data)
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
def get_file_by_content(file_path='', contain_txt=None, prefix=None, contain=None, suffix=None):
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


# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))
