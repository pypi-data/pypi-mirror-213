"""
rpc服务，数据接收统一处理
"""
from eqmicro.components.protocol import Protocol


def rpc_receive(connect):
    """
    rpc 通讯接收
    """
    # 用于存储客户端上送的所有数据
    recv = bytes("", 'utf-8')
    # 循环接收客户端上送数据，每次接收 1024 字节
    while True:
        data = connect.recv(1024)
        recv = recv + data
        # 长度小于 1024 时认为传输结束
        if len(data) < 1024:
            break
    # 使用协议解析数据
    protocol = Protocol('ana', recv)
    # 读取请求信息为 dict 类型
    protocol.to_dict()

    # 返回接受的数据解析
    return protocol
