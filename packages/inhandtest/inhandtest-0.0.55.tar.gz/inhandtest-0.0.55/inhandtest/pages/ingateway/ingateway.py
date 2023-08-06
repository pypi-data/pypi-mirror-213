# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 16:09:27
# @Author  : Pane Li
# @File    : ingateway.py
"""
ingateway

"""
import logging

from playwright.sync_api import Page
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.edge_computing.python_edge_computing import EdgeComputing
from inhandtest.pages.ingateway.network.network import Network
from inhandtest.pages.ingateway.overview.overview import Overview
from inhandtest.pages.ingateway.system.system import System
from inhandtest.telnet import Telnet
import dynaconf
import os


class InGateway(BasePage):

    def __init__(self, host: str, super_user: str, super_password: str, page: Page = None, model='IG902',
                 language='en', protocol='https', port=443, username='adm', password='123456', telnet=True,
                 locale_yaml_path=None):
        """

        :param host:   设备主机地址
        :param super_user:  超级用户
        :param super_password: 超级用户密码
        :param page:  playwright page
        :param model:  设备型号  IG902 IG502
        :param language: 语言 en cn
        :param protocol: 协议  http https
        :param port:    端口
        :param username: 用户名
        :param password: 密码
        :param telnet: 是否开启telnet
        :param locale_yaml_path: 语言文件 默认为None
        """

        if locale_yaml_path:
            in_setting = dynaconf.Dynaconf(
                settings_files=[os.path.join(os.path.dirname(__file__), 'locale.yml'), locale_yaml_path])
        else:
            in_setting = dynaconf.Dynaconf(
                settings_files=[os.path.join(os.path.dirname(__file__), 'locale.yml')])
        super().__init__(host, username, password, protocol, port, model, language, page, locale=in_setting)
        if telnet:
            self.telnet = Telnet(model, host, super_user, super_password)
        else:
            self.telnet = None
        if self.language == 'en':
            self.telnet.send_cli(command='language English', type_='user')
        else:
            self.telnet.send_cli(command='language Chinese', type_='user')
        self.login()
        self.overview = Overview(host, username, password, protocol, port, model, language, self.page, self.locale)
        self.network: Network = Network(host, username, password, protocol, port, model, language, self.page,
                                        self.locale)
        self.edge = EdgeComputing(host, username, password, protocol, port, model, language, self.page, self.locale)
        self.system = System(host, username, password, protocol, port, model, language, self.page, self.locale)


if __name__ == '__main__':
    from inhandtest.tools import enable_log

    enable_log('./log.log', console_level=logging.INFO)
    with InGateway('10.5.24.96') as device:
        device.network.cellular.config(cellular_enable=False,
                                       submit={'tip_messages': 'cellular_configuration_changed_successful'})

        # device.page.wait_for_timeout(3 * 1000)
