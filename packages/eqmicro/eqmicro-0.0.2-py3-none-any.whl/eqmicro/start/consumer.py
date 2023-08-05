"""
服务提供者
"""
import math
import random
import time
from threading import Thread
from eqmicro.client.rpc_disposable import RPDisposable
from eqmicro.consumer.srvice_call import consumer_call_protocol, res_ana
from eqmicro.consumer.service_pull import consumer_pull_protocol
from eqmicro.consumer.service_invalid import consumer_invalid_protocol


class ServerList:
    def __init__(self):
        self.server_list = {}

    def __get__(self):
        return self.server_list

    def __set__(self, data):
        self.server_list = data


server_list = ServerList()


class Consumer:
    def __init__(self, configuration):
        # 配置内容信息
        self.config = configuration
        # 服务提供者列表
        self.provider = None

    def call(self, service_name, call_data=None):
        """
        调用provider提供的远程服务
        """
        print('[eqmicro] 执行远程服务调用', self.config)
        return call_provider(service_name, call_data, self.config['register'])

    def pull(self, call_data=None):
        """
        从注册中心拉取可用服务
        """
        pull_provider(self.config['register'], call_data)

    def pull_loop(self, interval):
        """
        循环拉取服务
        """
        Thread(target=timing_pull, args=(interval, self.config['register'], None)).start()


def timing_pull(interval, config, call_data):
    """
    定时任务拉取服务
    """
    while True:
        pull_provider(config, call_data)
        time.sleep(interval)


def pull_provider(register_config, call_data=None):
    # 初始化一个服务拉取的协议
    send_data = consumer_pull_protocol(call_data)
    # 启动一个临时rpc连接，用于服务调用
    example = RPDisposable(register_config)
    # 向注册中心发送服务拉取请求
    recv_data = example.data_trans(send_data.to_binary())
    server_list.__set__(recv_data.get_data())
    print('[eqmicro] [服务拉取数据]', server_list.__get__())


def call_provider(service_name, call_data=None, register_conf=None):
    # 初始化一个远程调用的协议
    send_data = consumer_call_protocol(call_data)
    # 根据权重，计算调用ip
    # 0 - 应用名称，1 - 服务、方法路径
    service_call_info = service_name.split('::')
    send_data.protocol_content['body']['data']['func'] = service_call_info[1]
    while True:
        # 根据权重计算要调用的provider
        provider_server = weight_calculation(server_list.__get__(), service_call_info[0])
        if bool(provider_server) is False:
            response = '无可用服务！'
            break
        try:
            # 启动一个临时rpc连接，用于服务调用
            print('[eqmicro] [远程调用]', len(send_data.to_binary()), send_data.protocol_content)
            example = RPDisposable(provider_server)
            # 向注provider发送信息
            recv_data = example.data_trans(send_data.to_binary())
            # 调用成功
            print('[eqmicro] [响应结果]', recv_data.get_data())
            response = res_ana(recv_data.protocol_content)
            break
        except Exception as e:
            print(e)
            if 'WinError 10061' in str(e):  # 此时认为provider已经停止服务
                # 失效服务同步给注册中心
                sync_data = consumer_invalid_protocol(provider_server)
                sync_example = RPDisposable(register_conf)
                # 注册中心移除失效服务后，返回有效服务列表
                sync_recv_data = sync_example.data_trans(sync_data.to_binary())
                # 更新consumer本地存储的服务列表
                server_list.__set__(sync_recv_data.get_data())
            else:
                # 其他情况不进行处理，直接返回失败
                response = str(e)
                break
    return response


def weight_calculation(server_list_info, appname):
    """
    加权调用计算
    """
    # 可被调用的服务列表
    try:
        provider_server = server_list_info[appname]['call']
    except Exception as e:
        print('[eqmicro]', e)
        return False

    weight_check = []
    # 用于远程服务遍历的计数器
    count_w = 0
    # 权值和
    count_c = 0

    # 计算提供服务的应用数量、权重列表、所有应用的权重之和
    for item in provider_server:
        weight_check.append(int(item[2]))
        count_w = count_w + 1
        count_c = int(item[2]) + count_c

    # 无可用服务时，直接返回
    if count_c == 0:
        return False

    # 权重因子
    weight_factor = math.ceil(100 / count_c)
    # 权重计数累计值
    weight_m = 0
    # 生成0到100的随机数
    call_random = random.randint(0, 100)
    # 加权计算后，被调用的远程服务
    call_weight = 0
    print('[eqmicro] 远程服务加权调用，服务权重:', weight_check)

    # 顺序计算随机数命中了权重列表的哪个值
    for item in range(0, len(weight_check)):
        c_weight = int(weight_check[item]) * weight_factor
        weight_check[item] = [weight_m, weight_m + c_weight]
        if weight_m <= call_random <= weight_m + c_weight:
            call_weight = int(item)
            break
        weight_m = weight_m + c_weight
    print('[eqmicro] [加权调用]', call_weight, call_random)

    # 针对 host == 0.0.0.0 的调用，进行特殊处理
    if provider_server[call_weight][0] == '0.0.0.0':
        remote_host = '127.0.0.1'
    else:
        remote_host = provider_server[call_weight][0]

    # 返回根据权重计算的可调用服务的结果
    return {
        "appname": appname,
        "host": remote_host,
        "port": provider_server[call_weight][1]
    }
