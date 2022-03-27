"""
    21/7/26 12:20
    Coding By Danyhug
    7/26 16:05 可用
    连接校园网主程序
"""

import requests
import json
import time
import os
import sys

import secure   # 自用将这个删除
import conf     # 配置文件

# 会话状态保持
# session = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/98.0.4758.80'}

# 访问校园网地址获得对应数据
needStr = requests.get(conf.URL).text
try:
    queryString = needStr.split("index.jsp?")[1].split("'<")[0]
except IndexError:
    print('校园网可能已登录')
    sys.exit(1)
# 是否登录成功
isLogin = False

# 将所有信息读取
"""
读取信息格式1(根据账号格式选择取消哪个的注释)
格式要求 JSON格式
[
    {"uname": "test1", "passwd": "test1"},
    {"uname": "test2", "passwd": "test2"}
]
"""
def readFile() -> list:
    userInfo = list()
    with open('data.json', 'r') as f:
        d = f.readline()
        userInfo = json.loads(d)
    print('>> 文件读取完毕')
    return userInfo


"""
读取信息格式2
格式要求 用户名(空格)密码
    用户名1 用户名1
    用户名2 用户名2
"""
# def readFile() -> list:
#     userInfo = list()
#     with open('ccl.txt', 'r') as f:
#         d = f.readlines()
#         for item in d:
#             temp = item.split(' ')
#             userInfo.append({
#                 'uname': temp[0],
#                 'passwd': temp[1].split('\n')[0]
#             })
#     print(userInfo)
#     return userInfo

# 获取该用户的运营商，返回该用户的所有运营商
def GetService(uname) -> list:
    url = f"{conf.URL}/eportal/userV2.do?method=getServices"
    data = {
        'username': uname,
        'search': '?' + queryString
    }
    res = requests.post(url=url, data=data, headers=headers)
    serviceDetail = res.text
    # 证明无数据，账号有误或其他
    if serviceDetail == '':
        return []

    webList = serviceDetail.split('@')
    return webList


# 尝试登录
def Login(user):
    global service

    # 状态，尝试一次吧
    state = True
    print('>> 用户名', user['uname'], '尝试登录')

    # 证明有用户在线或其他问题，不可使用该账户登录
    """
        自用将这个判断删除
    """
    if not secure.Login(user['uname'], user['passwd']):
        state = False

    if user['service'] == '电信专线':
        service = '%E7%94%B5%E4%BF%A1%E4%B8%93%E7%BA%BF'
    elif user['service'] == '移动pppoe':
        service = '%E7%A7%BB%E5%8A%A8pppoe'
    elif user['service'] == '联通专线':
        service = '%E8%81%94%E9%80%9A%E4%B8%93%E7%BA%BF'
    url = f"{conf.URL}/eportal/InterFace.do?method=login"
    data = {
        'userId': user['uname'],
        'password': user['passwd'],
        'service': service,
        'queryString': queryString,
        'validcode': '',
        'operatorUserId': '',
        'operatorPwd': ''
    }

    while state:
        global isLogin
        res = requests.post(url=url, data=data, headers=headers)
        # 将内容转为Unicode码后编码为utf8的字符串
        resContent = json.loads(res.text.encode('ISO-8859-1').decode('utf8'))
        time.sleep(1)
        msg = ['用户不允许使用本服务!', '验证码错误.', '您的账户已欠费，为了不影响您正常使用网络，请尽快缴费!']
        for err in msg:
            if resContent['message'] == err:
                print('登录校园网失败，原因：', err)
                # 如果是验证码问题，重新再试一次
                if err == '验证码错误.':
                    pass
                    # data['validcode'] = GetValidcode()
                else:
                    state = False
            elif resContent['message'] == '':
                isLogin = True
                print('>>> 登录成功！！！')
                print('======================================')
                #print(f"账号是{data['userId']} ---- 密码是{data['password']} ---- {user['service']}")
                return
            else:
                print('>>> 其他错误')
                state = False


if isLogin:
    os.system('pause')

# 读取数据
userInfo = readFile()
# 需要跳过的账号
for info in userInfo:
    if isLogin:
        #os.system('pause')
        break

    for service in GetService(info['uname']):
        if service == '校园网':
            continue
        user = {
            'uname': info['uname'],
            'passwd': info['passwd'],
            'service': service,
            'time': []
        }
        Login(user)
        print('\n')

        time.sleep(1)
