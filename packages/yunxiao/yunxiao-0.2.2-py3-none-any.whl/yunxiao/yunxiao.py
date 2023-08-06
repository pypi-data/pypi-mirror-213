import configparser
import datetime
import logging

import requests
import time
from requests import utils
import os

config = configparser.ConfigParser()


class UsedTime:
    stamp = int(time.time() * 1000)
    now = datetime.datetime.now().date()
    today = now.__str__()
    weekstrat = (now - datetime.timedelta(days=now.weekday())).__str__()
    weekend = (now + datetime.timedelta(days=6 - now.weekday())).__str__()
    yymm = time.strftime('%Y-%m', time.localtime())
    yymm01 = time.strftime('%Y-%m-01', time.localtime())
    todaybeformonth = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * 30))
    tomorrow = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))


class YunXiao:

    def __init__(self, configfile: str = "yunxiao_config.ini"):

        self.configfile = configfile

        # 如果没有初始化配置文件，抛出异常并终止程序
        if not os.path.exists(self.configfile):
            config['AUTH'] = {
                'phone': 'your_phone',
                'password': 'your_password',
                'token': '',
                'cookie': ''
            }
            with open(configfile, 'w') as f:
                config.write(f)
            logging.error(f"请访问 {configfile} 配置你的用户名和密码。")
            raise Exception("未初始化配置文件。请访问 {configfile} 配置你的用户名和密码。")

        # 读取配置文件
        config.read(self.configfile)
        self.token = config['AUTH']['token']
        self.cookie = config['AUTH']['cookie']
        self.user = config['AUTH']['phone']
        self.pwd = config['AUTH']['password']

        # 未填写配置时
        if self.user == "your_phone" or self.pwd == "your_password":
            logging.error(f"请访问 {configfile} 配置你的用户名和密码。")
            raise Exception("未初始化配置文件。请访问 {configfile} 配置你的用户名和密码。")

        # 初始化 token：为空则刷新一次。
        if not self.token:
            self.renew_token()

        # 初始化 cooke：为空则刷新一次。
        if not self.cookie:
            self.renew_cookie()

    def renew_token(self):
        """
        刷新 token.tmp 配置中存储的 token
        """
        mid_token = requests.post(
            url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/loginByPhonePwd",
            json={
                "_t_": UsedTime.stamp,
                "password": self.pwd,
                "phone": self.user,
                "userType": 1
            }
        ).json()["data"]["token"]

        token = requests.get(
            url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/businessLogin",
            headers={"x3-authentication": mid_token},
            params={"_t_": UsedTime.stamp}
        ).json()["data"]["token"]

        config.read(self.configfile)
        config['AUTH']['token'] = token
        self.token = token
        with open(self.configfile, 'w') as f:
            config.write(f)

        logging.info("成功刷新 YUNXIAO_OAUTH_TOKEN")

    def renew_cookie(self):
        """
        刷新 cookie.tmp 配置中存储的 cookie
        """
        # logging.debug("开始刷新 Cookie")
        res = requests.post(
            url="https://yunxiao.xiaogj.com/api/ua/login/password",
            params={
                "productCode": 1,
                "terminalType": 2,
                "userType": 1,
                "channel": "undefined"
            },
            json={
                "_t_": UsedTime.stamp,
                "clientId": "x3_prd",
                "password": self.pwd,
                "username": self.user,
                "redirectUri": "https://yunxiao.xiaogj.com/web/teacher/#/home/0",
                "errUri": "https://yunxiao.xiaogj.com/web/simple/#/login-error"
            },
            allow_redirects=False
        )
        res1 = requests.Session().get(
            url=res.json()["data"],
            cookies=res.cookies,
            allow_redirects=False
        )

        cookie1 = "UASESSIONID=" + requests.utils.dict_from_cookiejar(res.cookies)["UASESSIONID"]
        cookie2 = "SCSESSIONID=" + requests.utils.dict_from_cookiejar(res1.cookies)["SCSESSIONID"]
        headers = {"cookie": cookie1 + "; " + cookie2}

        res2 = requests.Session().get(
            url=res1.headers["location"],
            headers=headers,
            allow_redirects=False
        )

        res3 = requests.Session().get(
            url=res2.headers["location"],
            headers=headers,
            allow_redirects=False
        )

        cookie3 = "SCSESSIONID=" + requests.utils.dict_from_cookiejar(res3.cookies)["SCSESSIONID"]

        cookie = cookie1 + "; " + cookie3

        config.read(self.configfile)
        config['AUTH']['cookie'] = cookie
        self.cookie = cookie
        with open(self.configfile, 'w') as f:
            config.write(f)

        logging.info("成功刷新 YUNXIAO_OAUTH_COOKIE")
