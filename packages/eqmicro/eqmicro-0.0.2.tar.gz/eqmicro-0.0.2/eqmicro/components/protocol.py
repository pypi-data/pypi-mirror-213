"""
交互协议定义
"""

import json
import traceback
from eqmicro.components.protocol_info import *
from datetime import date as dt_date, datetime as dt_datetime


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt_datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, dt_date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class Protocol:
    def __init__(self, option='new', data=None):
        """
        初始化协议类型
        option: new-新建协议，ana-解析
        """
        self.protocol_binary = None
        self.desc = None
        if option == 'new':
            # 此时 data 应传入协议编号，根据协议编号新建协议模板
            self.protocol_content, self.desc = get_protocol(data)
        else:
            # 此时传入的内容为待解析的协议
            self.protocol_binary = data

    def to_binary(self):
        # 协议内容转换为比特类型
        dtb = json.dumps(self.protocol_content, cls=ComplexEncoder) if type(
            self.protocol_content) != str else self.protocol_content
        self.protocol_binary = dtb.encode("utf-8")
        return self.protocol_binary

    def to_dict(self):
        # 协议内容转换为字典类型
        bs = self.protocol_binary.decode("utf-8")
        try:  # 尝试协议类型转换为dict
            bs = json.loads(bs)
        except Exception as e:
            print('[eqmicro] [protocol] 协议类型转换异常', e)
            print(traceback.format_exc())
        # 协议内容格式化之后写入对象
        self.protocol_content = bs
        return self.protocol_content

    def set_res(self, data=None):
        self.protocol_content['header']['protocol']['option'] = 'res'
        self.protocol_content['body']['data'] = data

    def get_data(self):
        return self.protocol_content['body']['data']


def get_protocol(protocol_str):
    """
    根据协议路径，进行初始化
    """
    # 获取协议类型，举例：provider::register 表示提供者的服务注册协议
    protocol_list = protocol_str.split('::')
    protocol = init_protocol()
    protocol['header']['protocol']['type'] = protocol_list[0]
    protocol['header']['protocol']['name'] = protocol_list[1]
    desc = protocol_number_list[protocol_list[0]][protocol_list[1]]
    return protocol, desc


if __name__ == '__main__':
    p = Protocol('100')
    b = p.to_binary()
    s = p.to_dict()
    print(s['name'])
