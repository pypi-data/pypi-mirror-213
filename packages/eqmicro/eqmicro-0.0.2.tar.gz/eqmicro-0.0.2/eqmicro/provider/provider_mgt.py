"""
服务提供管理
"""
from eqmicro.components.scan_services import ScanServices


class ProviderMGT:
    def __init__(self, path):
        """
        扫描本地服务。用于 provider 或者 http server 启动时加载
        """
        self.provider_service = ScanServices(path)
        # 服务名称列表
        self.services = self.provider_service.get_services()
        # 服务对象列表
        self.services_class = self.provider_service.get_services_class()
