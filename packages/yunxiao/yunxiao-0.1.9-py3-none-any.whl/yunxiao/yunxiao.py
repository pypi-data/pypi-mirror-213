import datetime
import logging
import requests
import time
from requests import utils
import os


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

    def __init__(self, phone: str, password: str):
        """
        :param phone: 用户手机号
        :param password: 用户密码
        """
        self.user = phone
        self.pwd = password

        if os.environ.get("YUNXIAO_OAUTH_TOKEN"):
            self.token = os.environ.get("YUNXIAO_OAUTH_TOKEN")
        else:
            self.renew_token()
            self.token = os.environ.get("YUNXIAO_OAUTH_TOKEN")

        if os.environ.get("YUNXIAO_OAUTH_COOKIE"):
            self.cookie = os.environ.get("YUNXIAO_OAUTH_COOKIE")
        else:
            self.renew_cookie()
            self.cookie = os.environ.get("YUNXIAO_OAUTH_COOKIE")

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

        os.environ["YUNXIAO_OAUTH_TOKEN"] = token

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

        os.environ["YUNXIAO_OAUTH_COOKIE"] = cookie
        logging.info("成功刷新 YUNXIAO_OAUTH_COOKIE")
