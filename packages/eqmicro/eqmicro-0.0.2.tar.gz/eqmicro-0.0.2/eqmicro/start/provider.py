"""
RPC服务
"""
import time

from eqmicro.client.rpc_disposable import RPDisposable
from eqmicro.client.rpc_service import RPCServer
from eqmicro.components.ext_lib import client_default, not_contain_key, client_time
from eqmicro.provider.provider_mgt import ProviderMGT
from eqmicro.consumer.srvice_call import call_ana
from threading import Thread
from eqmicro.client.rpc_receive import rpc_receive
from eqmicro.provider.provider_register import provider_register_protocol
from eqmicro.provider.provider_health import provider_health_protocol
import os
import uuid


class Provider:
    def __init__(self, configuration):
        """
        服务提供者初始化
        configuration 为传入配置信息
        示例：'register': {'host': '127.0.0.1', 'port': '20888'} 表示注册中心信息，用于服务注册
        示例：{'host': '', 'port': '', 'services': ''} 提供服务的端口和IP、服务列表路径
              {'application': 'demo-provider', 'weight':'200'} 应用信息、权重
        """
        self.client = None
        self.config = configuration.copy()
        self.service_config = client_default('provider', configuration)

        # 未设置应用名称时，赋随机值
        if not_contain_key(self.service_config, 'application') is True:
            self.service_config['application'] = 'provider-' + str(uuid.uuid1())

        # 未设置服务权重，赋随机值
        if not_contain_key(self.service_config, 'weight') is True:
            self.service_config['weight'] = '1'

        # 判断服务信息中是否含有services字段，即服务列表路径。没有的话赋予一个初始值
        if not_contain_key(self.service_config, 'services') is True:
            self.service_config['services'] = os.path.abspath(os.path.join(os.getcwd(), "../services"))
        # 建立服务管理对象（对服务列表进行扫描）
        self.provider_mgt = ProviderMGT(self.service_config['services'])

    def start(self):
        # 启动一个RPC服务，用于受理RPC请求
        self.client = RPCServer(self.service_config).service_init()
        print('[eqmicro] [服务启动] Time', client_time())
        while True:
            # 等待客户端连接信息
            connect, addr = self.client.service.accept()
            # 启动新的线程处理客户端请求
            Thread(target=self.receive, args=(connect,)).start()

    def receive(self, connect):
        # 接收并处理 RPC 接口返回的信息
        protocol = rpc_receive(connect)
        # 请求头的协议部分
        protocol_header_protocol = protocol.protocol_content['header']['protocol']
        print('[eqmicro] [协议信息]', protocol_header_protocol)
        if protocol_header_protocol['type'] == 'consumer':  # consumer发送过来的请求
            if protocol_header_protocol['name'] == 'call':  # 服务调用
                print('[eqmicro] 服务调用', protocol.protocol_content['body']['data'])
                # 执行服务调用，并拿到调用结果
                res = call_ana(protocol.protocol_content['body']['data'], self.provider_mgt.services_class)
                # 设置调用返回信息
                protocol.set_res(res)
        # 响应信息发送
        connect.sendall(protocol.to_binary())
        # 关闭TCP连接
        connect.close()

    def register(self):
        """
        服务注册到注册中心
        """
        # 初始化一个服务注册的协议
        send_data = provider_register_protocol(self.register_info())
        # 启动一个临时rpc连接，用于服务注册
        print('[eqmicro] [注册服务]', send_data.protocol_content['body']['data']['application'])
        example = RPDisposable(self.config['register'])
        print('[eqmicro] [注册请求] 报文长度:', len(send_data.to_binary()), send_data.protocol_content['body']['data'])
        # 向注册中心发送信息
        example.client.sendall(send_data.to_binary())
        # 接收注册中心返回信息
        protocol = rpc_receive(example.client)
        print('[eqmicro] [注册结果]', protocol.to_dict())
        example.client.close()

    def health(self):
        """
        服务健康状态检查
        """
        # 初始化一个服务健康状态同步协议
        send_data = provider_health_protocol(self.register_info())
        # 启动一个rpc连接
        print('[eqmicro] [健康状态同步]', send_data.protocol_content['body']['data']['application'])
        example = RPDisposable(self.config['register'])
        # 向注册中心发送信息
        example.client.sendall(send_data.to_binary())
        # 注册中心响应结果
        protocol = rpc_receive(example.client)
        # 关闭rpc连接
        example.client.close()
        print('[eqmicro] [同步结果]', protocol.get_data())

    def health_loop(self, interval=None):
        """
        定时任务
        """
        while True:
            time.sleep(interval)
            self.health()

    def health_async(self, interval=None):
        """
        健康状态同步，统一处理
        """
        if interval is None or interval == 0:  # 只进行一次健康状态同步
            self.health()
        else:  # 另起一个线程，定时进行健康状态同步
            Thread(target=self.health_loop, args=(interval,)).start()

    def register_info(self):
        """
        注册信息格式化
        """
        data = {
            "application": self.service_config['application'],
            "services": self.provider_mgt.services,
            "host": self.service_config['host'],
            "port": self.service_config['port'],
            "weight": self.service_config['weight']
        }
        return data
