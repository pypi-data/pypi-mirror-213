"""
一个rpc服务器对象
"""

import socket


class RPCServer:
    def __init__(self, configuration):
        """
        初始化一个 RPC 服务
        """
        self.config = configuration
        self.service = None

    def service_init(self):
        """
        RPC 服务连接信息
        """
        self.service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.service.bind((self.config['host'], int(self.config['port'])))
        self.service.listen(int(self.config['backlog']))
        print('[eqmicro] [服务信息]', self.config['host'], self.config['port'])
        return self
