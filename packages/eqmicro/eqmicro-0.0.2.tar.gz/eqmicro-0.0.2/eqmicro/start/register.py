"""
注册中心服务器
"""
from eqmicro.client.rpc_service import RPCServer
from eqmicro.components.ext_lib import client_default, client_time, not_contain_key
from threading import Thread
from eqmicro.register.service_mgt import ServiceMGT
from eqmicro.provider.provider_mgt import ProviderMGT
from eqmicro.consumer.srvice_call import call_ana
from eqmicro.client.rpc_receive import rpc_receive
import os
import uuid


class Register:
    def __init__(self, configuration):
        """
        注册中心启动器，初始化
        configuration: 配置信息
        示例：{'host': '0.0.0.0', 'backlog': '5', 'port': '9700', 'save': '本地之持久化存储路径'}
        补充：{'services': '自身provider服务路径'}
        补充：{'service_type': '1'} 注册中心操作开启方式 1-仅RPC服务，2-仅HTTP服务，3-全部开启
        补充：{'application': 'register-center'} 应用名称
        """
        # 检查配置信息是否正确输入。若配置信息未输入，根据启动器类型赋予默认值
        self.configuration = client_default('register', configuration)

        # 存储客户端服务信息
        self.client = None

        # 如果未传入本地持久化路径，则自动生生一个；如果传入了，则使用传入值
        if not_contain_key(configuration, 'save') is True:
            configuration['save'] = os.path.abspath(os.path.join(os.getcwd(), "../static/service.json"))
        self.service_mgt = ServiceMGT(configuration['save'])

        # 如果未传入自身服务路径，赋一个默认值
        if not_contain_key(configuration, 'services') is True:
            configuration['services'] = os.path.abspath(os.path.join(os.getcwd(), "../services"))
        self.provider_mgt = ProviderMGT(configuration['services'])

        # 未设置应用名称时，赋随机值
        if not_contain_key(self.configuration, 'application') is True:
            self.configuration['application'] = 'register-' + str(uuid.uuid1())
            print('[eqmicro] [应用信息]', self.configuration['application'])

        # 注册中心操作开启方式与RPC服务权重
        if not_contain_key(configuration, 'service_type') is True:
            self.configuration['service_type'] = 1

        # 当为1或3时，开启RPC调用方式
        if self.configuration['service_type'] == 1 or self.configuration['service_type'] == 3:
            register_info = {
                "application": self.configuration['application'],
                "services": self.provider_mgt.services,
                "host": self.configuration['host'],
                "port": self.configuration['port'],
                "weight": "100"
            }
            self.service_mgt.service_register(register_info)

    def start(self):
        # 启动一个RPC服务，用于受理RPC请求
        self.client = RPCServer(self.configuration).service_init()
        print('[eqmicro] [服务启动] Time', client_time())
        while True:
            # 等待客户端连接信息
            connect, addr = self.client.service.accept()
            # 启动新的线程处理客户端请求
            Thread(target=self.receive, args=(connect,)).start()

    def receive(self, connect):
        """
        注册中信接收内容后处理
        """
        # 用于存储客户端上送的所有数据
        protocol = rpc_receive(connect)

        # 请求头的协议部分
        protocol_header_protocol = protocol.protocol_content['header']['protocol']
        print('[eqmicro] [协议信息]', protocol_header_protocol)
        if protocol_header_protocol['type'] == 'provider':  # provider发送过来的
            if protocol_header_protocol['name'] == 'register':  # 服务注册
                # provider 发来的服务注册
                print('[eqmicro] [收到注册请求]', protocol.to_dict())
                # 加入已有服务列表
                print('[eqmicro] [原始服务列表]', self.service_mgt.get_list())
                new_server_list = self.service_mgt.service_register(protocol.protocol_content['body']['data'])
                print('[eqmicro] [最新服务列表]', new_server_list)
                # 设置响应信息
                protocol.set_res('服务注册成功')
            if protocol_header_protocol['name'] == 'health':
                # provider 发送过来的健康状态同步服务
                print('[eqmicro] [服务状态同步]', protocol.to_dict())
                # 根据健康状态进行处理
                res = self.service_mgt.service_health(protocol.get_data())
                protocol.set_res(res)

        elif protocol_header_protocol['type'] == 'consumer':  # consumer发送过来的请求
            if protocol_header_protocol['name'] == 'pull':  # 服务拉取
                # consumer 发来的服务拉取
                print('[eqmicro] 获取有效的服务')
                res = self.service_mgt.services_valid
                protocol.set_res(res)
            elif protocol_header_protocol['name'] == 'call':  # 服务调用
                # consumer 发来的服务调用
                print('[eqmicro] 服务调用', protocol.protocol_content['body']['data'])
                # 执行服务调用，并拿到调用结果
                res = call_ana(protocol.protocol_content['body']['data'], self.provider_mgt.services_class)
                # 设置调用返回信息
                protocol.set_res(res)
            elif protocol_header_protocol['name'] == 'invalid':  # 失效服务处理
                # consumer 发送过来的失效服务信息
                print('[eqmicro] 失效服务处理', protocol.protocol_content['body']['data'])
                res = self.service_mgt.set_invalid(protocol.protocol_content['body']['data'])
                protocol.set_res(res)

        # 响应信息发送
        connect.sendall(protocol.to_binary())
        # 关闭TCP连接
        connect.close()
