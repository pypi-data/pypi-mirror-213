"""
扩展工具
"""
import json
from socket import gethostbyname, gethostname
import random
import time


def not_contain_key(source_dict, target_key):
    """
    判断 dict 不包含元素
    source_dict 不包含 target_key, 返回 True
    """
    try:
        if source_dict.__contains__(target_key) is True:
            if source_dict[target_key] is not None:
                if source_dict[target_key] != '':
                    return False
    except Exception as e:
        print('[eqmicro] [Error] [ext_lib]', '字典元素检查', str(e))
    return True


def json_file_read(file_path):
    """
    file_path:JSON文件路径，读取文件内容（文件内容需要为 json 格式）
    """
    try:
        with open(file_path, encoding='utf-8') as json_file:
            fie_data = json.load(json_file)
            return fie_data
    except Exception as e:
        print('[eqmicro] [Warning] JSON 文件读取失败：', str(e), file_path)
        return {}


def client_default(client_type, configuration):
    """
    客户端工具配置默认值
    """
    if not_contain_key(configuration, 'host') is True:  # 指定默认端口好
        configuration['host'] = gethostbyname(gethostname())
    if not_contain_key(configuration, 'backlog') is True:  # 拒绝连接前，指定可以挂起的连接数
        configuration['backlog'] = '5'

    # 设置端口默认值
    if client_type == 'register':  # 注册中心配置端口
        if not_contain_key(configuration, 'port') is True:
            configuration['port'] = '20888'
    elif client_type == 'provider':  # provider 配置端口
        if not_contain_key(configuration, 'port') is True:
            configuration['port'] = random_number('2', 4)
    else:  # consumer 配置端口
        if not_contain_key(configuration, 'port') is True:
            configuration['port'] = random_number('2', 4)

    return configuration


def random_number(left, length):
    """
    生产随机数字
    """
    number = left
    for i in range(length):
        number = number + str(random.randint(1, 9))
    return number


def client_time():
    """
    客户端时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def file_save(path, data):
    """
    文件覆盖写入
    """
    if type(data) == dict or type(data) == list:
        data = json.dumps(data)

    with open(path, 'w') as f:
        f.write(data)
