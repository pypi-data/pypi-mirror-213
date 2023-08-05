"""
应用配置文件加载器
"""
import sys
import os
from eqmicro.components.ext_lib import not_contain_key
from eqmicro.components.read_conf import ReadConf


class LoadConfApp:
    def __init__(self, app_conf_path=None):
        """
        app_conf_path: application 配置文件路径
        params_start: 应用启动参数
        """
        # 如果未传入配置文件路径，取一个默认路径
        if app_conf_path is None:
            app_conf_path = os.path.abspath(os.path.join(os.getcwd(), "../configuration/profiles/app.json"))
        # 加载应用启动时的传入参数
        params_start = get_run_params(sys.argv[1:])
        # 补充的环境配置信息
        self.configuration_env = {}
        # 读取主配置文件信息
        self.configuration = ReadConf(app_conf_path)
        self.configuration.__file_load__()
        # 判断是否有补充的环境配置信息
        if not_contain_key(params_start, 'env') is False:
            # 启动参数传入运行环境信息时，额外加载环境配置文件
            self.load_env(app_conf_path[:-5] + '-' + params_start['env'] + app_conf_path[-5:])
            print('[eqmicro] [强制指定] 运行配置文件', params_start['env'])
            self.configuration.configuration['env'] = params_start['env']
        else:
            # 启动参数未传入运行环境信息，判断主配置文件是否指定环境信息
            if not_contain_key(self.configuration.configuration, 'env') is False:
                self.load_env(app_conf_path[:-5] + '-' + self.get_conf()['env'] + app_conf_path[-5:])
        if 'port' in params_start:
            # 支持启动参数强制指定端口
            self.configuration.configuration['port'] = int(params_start['port'])

    def load_env(self, path):
        """
        加载附加环境配置文件信息
        :param path: 附加环境路径
        """
        # 读取补充环境配置文件信息
        self.configuration_env = ReadConf(path)
        self.configuration_env.__file_load__()
        # 补充配置信息写入主配置信息
        self.configuration.configuration.update(self.configuration_env.configuration)

    def get_conf(self):
        # 配置信息读取
        return self.configuration.configuration


def get_run_params(input_params):
    """
    启动参数处理
    :param input_params: 应用启动参数 ['env=dev', 'port=7877']
    :return: 启动参数格式化 {'env':'dev', 'port':'7877'}
    """
    run_params = {}
    for item in input_params:
        try:
            info = item.split('=')
            run_params[info[0]] = info[1]
        except Exception as e:
            print('[eqmicro] 仅解析 a=b 格式的启动参数，其他跳过，', e)
    return run_params
