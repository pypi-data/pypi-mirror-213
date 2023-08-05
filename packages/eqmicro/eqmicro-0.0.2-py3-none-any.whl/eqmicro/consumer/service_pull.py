"""
consumer 从 register 拉取服务的协议定义
"""
from eqmicro.components.protocol import Protocol


def consumer_pull_protocol(call_data):
    """
    传入接口调用信息
    """
    # 初始化一个服务拉取的协议
    send_data = Protocol('new', 'consumer::pull')
    # 获取应用的服务列表
    send_data.protocol_content['body']['code'] = 'success'
    send_data.protocol_content['body']['message'] = send_data.desc
    send_data.protocol_content['body']['data'] = {}
    send_data.protocol_content['body']['data']['params'] = call_data
    return send_data
