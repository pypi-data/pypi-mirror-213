"""
服务注册协议处理
"""
from eqmicro.components.protocol import Protocol


def provider_register_protocol(register_info):
    # 初始化一个服务注册的协议
    send_data = Protocol('new', 'provider::register')
    # 获取应用的服务列表
    send_data.protocol_content['body']['code'] = '1000'
    send_data.protocol_content['body']['message'] = send_data.desc
    send_data.protocol_content['body']['data'] = register_info

    return send_data
