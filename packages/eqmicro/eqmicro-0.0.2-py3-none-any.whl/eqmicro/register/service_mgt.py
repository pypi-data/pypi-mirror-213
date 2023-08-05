"""
注册中心服务管理
"""
from eqmicro.components.read_conf import ReadConf
from eqmicro.components.ext_lib import not_contain_key, file_save
import json


class ServiceMGT:
    def __init__(self, save_path):
        """
        管理对象初始化
        """
        # 本地服务存储文件路径（json文件）
        self.save_path = save_path
        # 初始化一个配置文件读取对象
        self.service_save = ReadConf(save_path)
        self.service_save.__file_load__()
        # 判断本地服务存储文件读取结果
        if bool(self.service_save.configuration) is False:
            # 本地存储文件读取化失败，进行初始化
            file_save(save_path, content_int())
        # 有效服务列表
        self.services_valid = {}
        # 全部服务列表
        self.services_all = {}

    def get_list(self):
        """
        本地存储的所有信息
        """
        return self.service_save.configuration

    def service_register(self, data):
        """
        provider 注册服务时的处理
        """
        # 读取本地保存的服务列表
        server_list = self.service_save.__read__('server_list')
        # 判断服务列表中 是否存在要注册的服务
        server_name = data['application']
        if not_contain_key(server_list, server_name) is True:
            # 如果当前服务在列表中不存在，需要先添加服务元素
            server_list[server_name] = {}
            # 提供的服务信息
            server_list[server_name]['services'] = data['services']
            # 提供服务的调用信息 (服务地址, 端口, 权重，上线状态，运行状态)
            server_list[server_name]['call'] = [[data['host'], data['port'], data['weight'], "1", "1", "1"]]
        else:
            # 服务调用信息检查，注册的服务信息是否已登记在注册中心
            # 应用IP:PORT注册标识，为False时，不需要进行call列表更新
            need_update = True
            for item in server_list[server_name]['call']:
                # 已在列表中，强制每次更新权重信息
                if item[0] == data['host'] and item[1] == data['port']:
                    item[2] = data['weight']
                    need_update = False
            if need_update is True:
                # 向服务列表中添加服务注册 (服务地址, 端口, 权重，上线状态，运行状态)
                server_list[server_name]['call'].append([data['host'], data['port'], data['weight'], "1", "1", "1"])
        print('[eqmicro] [服务更新] 内容写入本地文件', json.dumps(self.service_save.configuration))
        # 每次调用强制更新注册中心服务列表
        file_save(self.save_path, self.service_save.configuration)
        self.services_all = server_list
        self.get_valid()
        # 返回已经注册的服务列表
        return server_list

    def service_health(self, data):
        """
        服务健康状态管理
        data包含ip和port
        """
        result = {
            'state': 'success',
            'message': '服务状态已同步'
        }
        server_list = self.service_save.__read__('server_list')
        server_name = data['application']
        # print(server_list[server_name]['call'])
        # print(data)
        if not_contain_key(server_list, server_name) is True:
            print('[eqmicro] [health] 应用服务未注册', server_name)
            result['state'] = 'error'
            result['message'] = '服务未注册'
        else:
            # 服务调用信息检查
            for item in server_list[server_name]['call']:
                # [['11.11.0.127', 28501, '1', '1', 1, 1], ['11.11.0.127', '28502', '1', '1', 1, 1]]
                # ip, port, weight, 1:上线/0:下线, 1:有效/0:失效, 备用状态:1-正常
                if item[0] == data['host'] and item[1] == data['port']:
                    # 失效状态的服务，将被置为有效状态
                    if item[4] == '0':
                        item[4] = '1'
                        # 更新注册中心登记的服务状态
                        file_save(self.save_path, self.service_save.configuration)
                        self.services_all = server_list
                        self.get_valid()
        return result

    def get_valid(self):
        """
        获取有效服务列表
        """
        # 服务列表审拷贝，防止修改覆盖
        services_all = json.loads(json.dumps(self.services_all))
        for item in services_all:
            call_list = services_all[item]['call'].copy()
            for inter in call_list:
                # [['11.11.0.127', 28501, '1', '1', 1, 1], ['11.11.0.127', '28502', '1', '1', 1, 1]]
                # ip, port, weight, 1:上线/0:下线, 1:有效/0:失效, 备用状态:1-正常
                if str(inter[3]) == '1' and str(inter[4]) == '1' and str(inter[5]) == '1':
                    pass
                else:
                    call_list.remove(inter)
            services_all[item]['call'] = call_list
        self.services_valid = services_all
        print('[eqmicro] [有效服务列表]', self.services_valid)
        return services_all

    def set_invalid(self, service_info):
        """
        有效的将服务将被置为失效状态
        """
        # 读取服务列表
        server_list = self.service_save.__read__('server_list')
        call_info = server_list[service_info['appname']]['call']
        for item in call_info:
            if item[0] == service_info['host'] and str(item[1]) == str(service_info['port']):
                item[4] = '0'
                break
        print('[eqmicro] [服务状态更新] 内容写入本地文件', json.dumps(self.service_save.configuration))
        file_save(self.save_path, self.service_save.configuration)
        self.services_all = server_list
        valid_services = self.get_valid()
        return valid_services

    def set_offline(self, appname, host, port, op_type='off'):
        """
        设置服务下线、上线状态
        off 服务下线
        on  服务上线
        """
        # 读取服务列表
        server_list = self.service_save.__read__('server_list')
        call_info = server_list[appname]['call']
        for item in call_info:
            if item[0] == host and str(item[1]) == str(port):
                if op_type == 'off':
                    item[3] = '0'
                elif op_type == 'on':
                    item[3] = '1'
                else:
                    break
                print('[eqmicro] [服务状态更新] 内容写入本地文件', json.dumps(self.service_save.configuration))
                file_save(self.save_path, self.service_save.configuration)
                self.services_all = server_list
                # 更新当前有效的服务
                self.get_valid()
                return True
        return False


def content_int():
    """
    注册中心本地存储文件初始化
    """
    content = {
        'type': 'save',
        'server_list': {}
    }
    return content
