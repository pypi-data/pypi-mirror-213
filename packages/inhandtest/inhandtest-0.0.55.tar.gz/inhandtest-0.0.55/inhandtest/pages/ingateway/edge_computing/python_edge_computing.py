# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 15:34:20
# @Author  : Pane Li
# @File    : python_edge_computing.py
"""
python_edge_computing

"""
import allure
from inhandtest.tools import loop_inspector

from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class PythonEdgeComputing(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Python Engine状态')
    @loop_inspector('python_engine_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               python_engine: enable,disable ex: python_engine='"${value}"=="enable"'
               sdk_version: 1.4.3 ex: sdk_version='1.4.3'
               python_version: Python3 ex: python_version='Python3'
               username: adm ex: username='adm'
               used_user_storage: 176MB/6GB3% ex: used_user_storage='"${value}".startswith("176MB")'
        """
        self.access_menu('edge computing.python edge computing')
        return self.eval_locator_attribute(kwargs, self.edge_locators.python_engine_status_locator)

    @allure.step('获取Python Engine状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               python_engine, sdk_version, python_version, username, used_user_storage, password
        """
        self.access_menu('edge computing.python edge computing')
        return self.get_text(keys, self.edge_locators.python_engine_status_locator)

    @allure.step('配置Python Edge Computing')
    def config(self, **kwargs):
        """
        :param kwargs:
               python_engine: enable,disable ex: python_engine='enable'
               sdk_upgrade: file_path ex: sdk_upgrade='C:\\Users\\Administrator\\Downloads\\inhand-1.4.3.tar.gz'
               sdk_upgrade_tip: dict sdk_upgrade_tip={'tip_messages': 'install_success', 'timeout': 100}
               password: 123456 ex: password='123456'
               start_all_app: True, False ex: app_all_start=True
               stop_all_app: True, False ex: app_all_stop=True
               restart_all_app: True, False ex: restart_all_app=True
               app: [($action, **kwarg)] ex:
                    [('enable', 'device_supervisor', True)],   # 启用 device_supervisor
                    [('enable', 'device_supervisor', False)]   # 禁用 device_supervisor
                    [('install', {'app_package': 'C:\\Users\\Administrator\\Downloads\\device_supervisor-1.0.0.tar.gz'})] # 添加 device_supervisor
                    [('import_config', 'device_supervisor', 'C:\\Users\\Administrator\\Downloads\\device_supervisor-1.0.0.conf')] # 导入device_supervisor配置
                    [('export_config', 'device_supervisor', {'file_path': 'C:\\Users\\Administrator\\Downloads', 'file_name': "device_supervisor-1.0.0.conf"})] # 导出device_supervisor配置， 文件名可以不传
                    [('uninstall', 'device_supervisor')]   # 卸载 device_supervisor
                    [('edit', 'device_supervisor', {'log_file_size': 1, 'number_of_log': 2, 'start_args': ''})]   # 编辑 device_supervisor
                    [('download_log', 'device_supervisor', {'file_path': 'C:\\Users\\Administrator\\Downloads', 'file_name': "device_supervisor-1.0.0.log"})] # 导出device_supervisor日志， 文件名可以不传
                    [('clear_log', 'device_supervisor')]   # 清除 device_supervisor 日志
                    [('start', 'device_supervisor')]  # 启动 device_supervisor
                    [('stop', 'device_supervisor')]   # 停止 device_supervisor
                    [('restart', 'device_supervisor')]   # 重启 device_supervisor
                    edit parameters:
                        log_file_size: int
                        number_of_log: int
                        start_args: str  启动参数
                        error_text: str or list
                        cancel: True, False
               submit: True,False ex: submit=True  or submit={'tip_messages': 'APP start successful'}
               error_text: str ex: error_text='ip_address_conflict'
               success_tip: ‘APP start successful’
               reset: True, False ex: reset=True
        """
        self.access_menu('edge computing.python edge computing')
        self.page.wait_for_load_state(state='networkidle')
        self.page.wait_for_timeout(1 * 1000)
        if kwargs.get('sdk_upgrade'):
            kwargs.update({'sdk_upgrade_confirm': True})
            if kwargs.get('sdk_upgrade_tip') is None:
                kwargs.update({'sdk_upgrade_tip': {'tip_messages': 'install_success', 'timeout': 100}})
        if kwargs.get('password'):
            kwargs.update({'edit_password': True, 'submit_password': True})
        if kwargs.get('app'):
            app_list_action = []
            app_status_action = []
            for action in kwargs.pop('app'):
                if action[0] in ('enable', 'install', 'import_config', 'export_config', 'uninstall', 'edit'):
                    app_list_action.append(action)
                else:
                    app_status_action.append(action)
            kwargs.update({'app_list': app_list_action, 'app_status': app_status_action})
        self.agg_in(self.edge_locators.python_edge_computing_locator, kwargs)


class DockerManager(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Docker Manager状态')
    @loop_inspector('docker_manager_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               docker_manager: enable,disable ex: docker_manager='"${value}"=="enable"'
               docker_version: 1.4.3 ex: docker_version='1.4.3'
               portainer_manager: enable,disable ex: portainer_manager='"${value}"=="enable"'
               username: adm ex: username='adm'
               password: 123456 ex: password='123456'
               port:  9000 ex: port='9000'
        """
        self.access_menu('edge computing.docker manager')
        return self.eval_locator_attribute(kwargs, self.edge_locators.docker_manager_status_locator)

    @allure.step('获取Docker Manager状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               docker_manager, docker_version, portainer_manager, username, password, port
        """
        self.access_menu('edge computing.docker manager')
        self.page.wait_for_timeout(1000)
        return self.get_text(keys, self.edge_locators.docker_manager_status_locator)

    @allure.step('配置Docker Manager')
    def config(self, **kwargs):
        """
        :param kwargs:
               docker_manager: enable,disable ex: docker_manager='enable'
               docker_upgrade: file_path ex: docker_upgrade='C:\\Users\\Administrator\\Downloads\\inhand-1.4.3.tar.gz'
               docker_upgrade_tip: 'install_failure', 'install_success', ex: docker_upgrade_tip='install_success'
               submit_docker_manager: True, False ex: submit_docker_manager=True or submit_docker_manager={'tip_messages': 'submit_success'}
               portainer_manager: enable,disable ex: portainer_manager='enable'
               password: 123456 ex: password='123456'
               port: 9000 ex: port='9000'
               submit_portainer_manager: True, False ex: submit_portainer_manager=True or submit_portainer_manager={'tip_messages': 'submit_success'}
               error_text: str ex: error_text='ip_address_conflict'
               success_tip: ‘submit_success’
               reset: True, False ex: reset=True
        """
        self.access_menu('edge computing.docker manager')
        self.page.wait_for_load_state(state='networkidle')
        self.page.wait_for_timeout(1 * 1000)
        if kwargs.get('docker_upgrade'):
            kwargs.update({'docker_upgrade_confirm': True})
            if kwargs.get('docker_upgrade_tip') is None:
                kwargs.update({'docker_upgrade_tip': {'tip_messages': 'install_success', 'timeout': 100}})
        self.agg_in(self.edge_locators.docker_manager_locator, kwargs)


class EdgeComputing:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.python_edge: PythonEdgeComputing = PythonEdgeComputing(host, username, password, protocol, port,
                                                                    model, language, page, locale)
        self.docker_manager: DockerManager = DockerManager(host, username, password, protocol, port, model, language,
                                                           page, locale)
