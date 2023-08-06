# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 16:38:15
# @Author  : Pane Li
# @File    : register_v1.py
"""
register_v1

"""
import logging
import requests
import pandas as pd
from inhandtest.tools import file_hash
from inhandtest.inmongodb import Mongodb
from bson.objectid import ObjectId

address = 'http://beta.elms.inhand.design'
mongo_address = '10.5.17.50'
mqtt_broker = 'ap.beta.elms.inhand.design'
mqtt_port = 31883


def register_v1(sn: str or list, username: str, model: str = 'IR300', to_csv='./auth.csv'):
    """
    注册
    :param sn: 设备sn
    :param username: 用户名
    :param model: 设备型号
    :param to_csv: 保存到csv文件
    :return:
    """
    sn = [sn] if isinstance(sn, str) else sn
    data = {"sn": [], "id": [], 'key': [], 'server': [], 'port': []}
    for i in sn:
        sign = file_hash(str(i) + username + '64391099@inhand')  # 对sign进行加密
        param = {"sn": i, "auth": username, "sign": sign, "model": model}
        response = requests.get(f'{address}/dapi/register', params=param)
        if response.status_code == 200:
            logging.info(f'设备 {i} 注册成功')
        data.get('sn').append(i)
        data.get('id').append(response.json().get('result').get('deviceId'))
        data.get('key').append(response.json().get('result').get('key'))
        data.get('server').append(response.json().get('result').get('server').get('host'))
        data.get('port').append(response.json().get('result').get('server').get('port'))
    if to_csv:
        pf = pd.DataFrame(data)
        pf.to_csv(to_csv, index=False)


# 获取mqtt 客户端认证信息
def get_auth(sn: str or list, to_csv='./auth.csv'):
    """
    获取mqtt 客户端认证信息
    :param sn: 设备sn
    :param to_csv: 保存到csv文件
    :return:
    """
    mo = Mongodb(mongo_address, 27017, 'admin', 'admin')
    sn = [sn] if isinstance(sn, str) else sn
    data = {"sn": [], "id": [], 'key': [], 'server': [], 'port': []}
    for i in sn:
        _id = mo.find('dn_pp', 'devices', {'serialNumber': i})[0].get('_id')
        device_auth = mo.find('ABCED_db', 'device.key', {'deviceId': ObjectId(_id)})[0]
        key = device_auth.get('key')
        data.get('sn').append(i)
        data.get('id').append(_id)
        data.get('key').append(key)
        data.get('server').append(mqtt_broker)
        data.get('port').append(mqtt_port)
        logging.info(f'已获取{i}设备认证信')
    if to_csv:
        pf = pd.DataFrame(data)
        pf.to_csv(to_csv, index=False)


if __name__ == '__main__':
    # 设置输出日志到控制台
    import concurrent.futures

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    all_sn = [f"RL302000100{str(i).rjust(4, '0')}" for i in range(0, 10000)]
    get_auth(all_sn, to_csv='./auth.csv')
    # register_v1(all_sn, '8888@inhand.com.cn', 'http://beta.elms.inhand.design')
    # register_v1('RL3020924001591', 'liwei@inhand.com.cn', 'http://beta.elms.inhand.design')
    # 创建多个进程，每个进程创建一部分客户端
    # auths = pd.read_csv('./auth.csv', index_col=False).values.tolist()
    # for auth in auths:
    #     create_client(auth)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
    #     for i in auths[:300]:
    #         executor.submit(create_client, i)

    # 等待一段时间，让所有客户端连接到服务器
    # time.sleep(1 * 60)
