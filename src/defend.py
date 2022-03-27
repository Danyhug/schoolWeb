"""
    2022年3月27日13:03:13
    该文件是守护程序，每20秒访问一次baidu，访问正常则网络正常
    访问不正常，则说明网络断了，需要连接
    ====================================================
    我的做法是把校园网的连接程序编译为exe文件，访问不正常的时候自动打开该程序
    根据你的需求自行更改
"""
import os
import time
import requests

# 状态 1为正常
status = 1
# 等待次数
count = 0
while True:
    # http状态码
    try:
        code = requests.request('GET', 'https://www.baidu.com/favicon.ico').status_code
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 网络正常')
        status = 1
        count = 0
    except:
        count += 1
        # 说明网络不正常，执行程序
        if status or count > 10:
            count = 0
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 网络出错，已重连')
            # 不正常
            status = 0
            #os.system('start P:\\Code\\Python\\school2\\dist\\main.exe')
            os.system('python main.py')

    time.sleep(20)
