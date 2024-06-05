# -*- coding: utf8 -*-
import json
import random
import socket
from collections import OrderedDict
from time import sleep
import requests
import traceback
from random_user_agent import set_user_agent
import brotli


class HTTPClient(object):
    def __init__(self) -> None:
        """
        :param method:
        :param headers: Must be a dict. Such as headers={'Content_Type':'text/html'}
        """
        self._s = requests.Session()
        self._ua = set_user_agent()
        self.token = ''
        self.memberId = ''
        self.cookie = ''

    def initS(self):
        return self
    
    def rand_ua(self):
        self._ua = set_user_agent()

    def set_cookies(self, kwargs):
        """
        设置cookies
        :param kwargs:
        :return:
        """
        for kwarg in kwargs:
            for k, v in kwarg.items():
                self._s.cookies.set(k, v)

    def get_cookies(self):
        """
        获取cookies
        :return:
        """
        return self._s.cookies#.values()

    def del_cookies(self):
        """
        删除所有的key
        :return:
        """
        self._s.cookies.clear()

    def del_cookies_by_key(self, key):
        """
        删除指定key的session
        :return:
        """
        self._s.cookies.set(key, None)

    def setHeaders(self, headers):
        if 'token' in headers:
            headers['token'] = self.token
        if 'memberId' in headers:
            headers['memberId'] = self.memberId
        if 'User-Agent' in headers and headers['User-Agent'] == '':
            headers['User-Agent'] = self._ua
        if  self.cookie:
            headers['cookie'] = self.cookie
        self._s.headers.update(headers)
        #print(self._s.headers)
        return self
    def resetHeaders(self):
        self._s.headers.clear()

    def getHeadersHost(self):
        return self._s.headers["Host"]

    def setHeadersHost(self, host):
        self._s.headers.update({"Host": host})
        return self

    def setHeadersUserAgent(self):
        self._s.headers.update({"User-Agent": self._ua})

    def getHeadersUserAgent(self):
        return self._s.headers["User-Agent"]

    def getHeadersReferer(self):
        return self._s.headers["Referer"]

    def setHeadersReferer(self, referer):
        self._s.headers.update({"Referer": referer})

    def send(self, urls, data=None, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        error_data = {"code": 99999, "message": u"重试次数达到上限"}
        allow_redirects = False
        req_url = urls.get("req_url", "")
        method = urls.get("req_type", "")
        re_try = urls.get("re_try", 0)
        s_time = urls.get("s_time", 0)
        header = urls.get("header", {})
        self.resetHeaders()
        self.setHeaders(header)

        for i in range(re_try):
            try:
                sleep(s_time)
                try:
                    requests.packages.urllib3.disable_warnings()
                except:
                    pass
                response = self._s.request(method=method,
                                           timeout=5,
                                           url=req_url,
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           verify=False,
                                           **kwargs)
                if response.status_code == 200 or response.status_code == 302:
                    if urls.get("not_decode", False):
                        return response.content
                    if response.content:
                        if urls["is_json"]:
                            print(response.json(),req_url)
                            return json.loads(
                                response.content.decode() if isinstance(response.content, bytes) else response.content)
                        else:
                            return response.content.decode("utf8", "ignore") if isinstance(response.content,
                                                                                           bytes) else response.content
                    else:
                        print(
                            f"url: {urls['req_url']}返回参数为空, 接口状态码: {response.status_code}")
                        continue
                else:
                    print(f"url: {urls['req_url']}访问错误, 接口状态码: {response.status_code}")
                    sleep(urls["re_time"])
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
                # traceback.print_exc()
            except socket.error:
                pass
                # traceback.print_exc()
        return error_data
