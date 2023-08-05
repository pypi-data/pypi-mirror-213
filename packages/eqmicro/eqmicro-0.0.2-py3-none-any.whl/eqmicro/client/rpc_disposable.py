"""
一个临时rpc连接对象，用于向 server 发送数据
"""

import socket
from eqmicro.components.ext_lib import client_time
from eqmicro.client.rpc_receive import rpc_receive


class RPDisposable:
    def __init__(self, configuration):
        """
        初始化rpc连接信息
        """
        self.client = socket.socket()
        print('[eqmicro] [临时RPC调用]', configuration)
        self.client.connect((configuration['host'], int(configuration['port'])))
        print('[eqmicro] [临时RPC连接] Time', client_time())

    def data_trans(self, data):
        """
        data: 要向rpc服务发送的数据
        return: rpc服务返回的数据（进行了协议解析）
        """
        # 向远程地址发送请求
        self.client.sendall(data)
        # 接收远程服务响应结果
        recv_data = rpc_receive(self.client)
        # 关闭RPC连接
        self.client.close()
        return recv_data
