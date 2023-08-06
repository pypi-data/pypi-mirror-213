# -*- coding: utf-8 -*-
# @Time    : 2023/4/26 10:52:06
# @Author  : Pane Li
# @File    : mqtt.py
"""
mqtt

"""
# 怎样使用python paho mqtt 模拟在线100000个客户端

import pandas as pd
import asyncio
import aiomqtt

# MQTT Broker地址和端口号
broker_address = "localhost"
port = 1883

# 订阅的主题
topic = "test/topic"

# 连接的用户名和密码
username = "user"
password = "password"

# 模拟的客户端数量
client_count = 10000


async def client_loop(auth_one):
    # 创建新的MQTT客户端
    client = aiomqtt.Client(client_id=auth_one[1])
    # 设置用户名和密码
    client.username_pw_set(auth_one[1], auth_one[2])
    # 连接到MQTT broker
    await client.connect(auth_one[3], port=auth_one[4])
    # 订阅主题
    # await client.subscribe(topic)
    # 循环处理MQTT消息
    client.loop_start()


# 创建事件循环
loop = asyncio.get_event_loop()

# 启动CLIENT_COUNT个客户端连接
auths = pd.read_csv('./auth.csv', index_col=False).values.tolist()
for i in auths:
    # 创建协程任务
    task = asyncio.ensure_future(client_loop(i))
    # 添加到事件循环中
    loop.run_until_complete(task)

# 在所有客户端连接完成后，保持事件循环运行
loop.run_forever()
