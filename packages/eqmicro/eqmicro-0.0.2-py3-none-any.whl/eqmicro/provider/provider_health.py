"""
健康状态推送协议处理
"""
from eqmicro.components.protocol import Protocol


def provider_health_protocol(health_info):
    # 初始化一个服务健康状态的协议
    send_data = Protocol('new', 'provider::health')
    # 获取应用的服务列表
    send_data.protocol_content['body']['code'] = '1000'
    send_data.protocol_content['body']['message'] = send_data.desc
    send_data.protocol_content['body']['data'] = health_info

    return send_data
