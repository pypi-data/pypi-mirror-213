"""
consumer 调用 provider 失败时，向 register 推送失效服务信息，协议处理
"""

from eqmicro.components.protocol import Protocol


def consumer_invalid_protocol(invalid_info):
    # 初始化一个服务更新的协议
    send_data = Protocol('new', 'consumer::invalid')
    # 获取应用的服务列表
    send_data.protocol_content['body']['code'] = '1000'
    send_data.protocol_content['body']['message'] = send_data.desc
    send_data.protocol_content['body']['data'] = invalid_info

    return send_data
