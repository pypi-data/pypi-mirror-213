"""
consumer 调用 provider 协议处理
"""
from eqmicro.components.protocol import Protocol


# 协议处理
def consumer_call_protocol(call_data):
    """
    初始化一个服务注册的协议
    """
    send_data = Protocol('new', 'consumer::call')
    # 获取应用的服务列表
    send_data.protocol_content['body']['code'] = 'success'
    send_data.protocol_content['body']['message'] = send_data.desc
    send_data.protocol_content['body']['data'] = {}
    send_data.protocol_content['body']['data']['params'] = call_data
    return send_data


# 调用解析
def call_ana(req, services):
    """
    provider 使用，根据请求体执行调用的方法
    """
    path_list = req['func'].split('/')
    call_service = services.copy()
    for i in range(0, len(path_list) - 1):
        call_service = call_service[path_list[i]]
    method = getattr(call_service['func'], path_list[len(path_list) - 1])
    return method(*tuple(req['params']))


def res_ana(res):
    """
    调用响应信息
    """
    if res['body']['code'] == 'success':
        return res['body']['data']
