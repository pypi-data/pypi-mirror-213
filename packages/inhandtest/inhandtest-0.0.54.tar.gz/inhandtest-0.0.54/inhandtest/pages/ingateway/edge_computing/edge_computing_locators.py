# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 15:58:25
# @Author  : Pane Li
# @File    : edge_computing_locators.py
"""
edge_computing_locators

"""
from playwright.sync_api import Page


class DockerManagerLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def docker_manager_status_locator(self) -> list:
        return [
            ('docker_manager', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('docker_version',
             {'locator': self.page.locator('//label', has_text=self.locale.docker_version).locator(
                 '../../div[2]/div/span/div/span[1]'),
                 'type': 'text'}),
            ('portainer_manager', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('username',
             {'locator': self.page.locator('//label', has_text=self.locale.user_name).locator('../../div[2]').nth(0),
              'type': 'text'}),
            ('password', {'locator': self.page.locator('#password'), 'type': 'fill'}),
            ('port', {'locator': self.page.locator('#port'), 'type': 'fill'}),
        ]

    @property
    def docker_manager_locator(self) -> list:
        return [
            ('docker_manager', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('docker_upgrade', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('docker_upgrade_confirm',
             {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary').nth(0), 'type': 'button',
              'wait_for': [{'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000},   # 文件大时间就长
                           {'type': 'timeout', 'timeout': 3 * 1000}]}),
            ('docker_upgrade_tip', {'type': 'tip_messages'}),
            ('submit_docker_manager', {'locator': self.page.locator('.ant-btn.ant-btn-primary').nth(1), 'type': 'button'}),
            ('portainer_manager', {'locator': self.page.locator('#enable').nth(1), 'type': 'switch_button'}),
            ('password', {'locator': self.page.locator('#password'), 'type': 'text', }),
            ('port', {'locator': self.page.locator('#port'), 'type': 'text', }),
            ('submit_portainer_manager',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit).nth(1),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]').nth(1),
                       'type': 'button'}),
        ]


class PythonEdgeComputingLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def python_engine_status_locator(self) -> list:
        return [
            ('python_engine', {'locator': self.page.locator('//button').nth(0), 'type': 'switch_button'}),
            ('sdk_version',
             {'locator': self.page.locator('//span', has_text=self.locale.sdk_version).locator('../span[2]').nth(0),
              'type': 'text'}),
            ('python_version',
             {'locator': self.page.locator('//span', has_text=self.locale.python_version).locator('../span[2]').nth(0),
              'type': 'text'}),
            ('username',
             {'locator': self.page.locator('//span', has_text=self.locale.username).locator('../span[2]').nth(0),
              'type': 'text'}),
            ('used_user_storage',
             {'locator': self.page.locator('//span', has_text=self.locale.used_user_storage).locator('../div').nth(0),
              'type': 'text'}),
            ('password', {'locator': self.page.locator('.anticon.anticon-copy'), 'type': 'clipboard'}),
        ]

    @property
    def python_edge_computing_locator(self) -> list:
        return [
            ('python_engine', {'locator': self.page.locator('//button').nth(0), 'type': 'switch_button'}),
            ('sdk_upgrade', {'locator': self.page.locator('//button').nth(1), 'type': 'upload_file',
                             'relation': [('python_engine', 'enable')]}),
            ('sdk_upgrade_confirm',
             {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary').nth(0), 'type': 'button'}),
            ('sdk_upgrade_tip', {'type': 'tip_messages'}),
            ('edit_password', {'locator': self.page.locator('.anticon.anticon-form').nth(0), 'type': 'button',
                               'relation': [('python_engine', 'enable')]}),
            ('password',
             {'locator': self.page.locator('.ant-input'), 'type': 'text', 'relation': [('python_engine', 'enable')]}),
            ('submit_password', {'locator': self.page.locator('.anticon.anticon-check').nth(1), 'type': 'button'}),
            ('start_all_app', {'locator': [self.page.locator('.anticon.anticon-play-circle').nth(0),
                                           self.page.locator('.ant-popover-inner-content').locator(
                                               '.ant-btn.ant-btn-primary.ant-btn-sm').first],
                               'type': 'button', 'relation': [('python_engine', 'enable')]}),
            ('stop_all_app', {'locator': [self.page.locator('.anticon.anticon-pause-circle').nth(0),
                                          self.page.locator('.ant-popover-inner-content').locator(
                                              '.ant-btn.ant-btn-primary.ant-btn-sm').first],
                              'type': 'button', 'relation': [('python_engine', 'enable')]}),
            ('restart_all_app', {'locator': [self.page.locator('.anticon.anticon-undo').nth(0),
                                             self.page.locator('.ant-popover-inner-content').locator(
                                                 '.ant-btn.ant-btn-primary.ant-btn-sm').first],
                                 'type': 'button', 'relation': [('python_engine', 'enable')]}),
            ('app_list',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox').nth(0),
                 'pop_up_locator': self.pop_up,
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                 "columns": [
                     ('app_package',
                      {'locator': self.pop_up.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
                     ('log_file_size', {'locator': self.pop_up.locator('#log_size'), 'type': 'text'}),
                     ('number_of_log', {'locator': self.pop_up.locator('#log_file_num'), 'type': 'text'}),
                     ('start_args', {'locator': self.pop_up.locator('#start_args'), 'type': 'text'}),
                     ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'),
                                 'type': 'button'}),
                     ('save', {'locator': self.pop_up.locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                         'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                     ('errors_text', {'type': 'text_messages'}),
                     ('success_tip', {'type': 'tip_messages'}),
                 ]},
                 'type': 'table_tr', 'relation': [('python_engine', 'enable')]}),
            ('app_status',
             {'locator': {
                 'locator': self.page.locator(
                     '.ant-table.ant-table-default.ant-table-bordered.ant-table-scroll-position-left').nth(0),
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
             },
                 'type': 'table_tr', 'relation': [('python_engine', 'enable')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button'}),
        ]


class EdgeComputingLocators(PythonEdgeComputingLocators, DockerManagerLocators):
    pass
