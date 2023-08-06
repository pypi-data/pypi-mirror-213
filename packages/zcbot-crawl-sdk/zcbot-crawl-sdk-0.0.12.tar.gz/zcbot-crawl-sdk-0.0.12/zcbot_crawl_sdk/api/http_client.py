# -*- coding: utf-8 -*-

"""
http
~~~~~~~~
这个模块包含了HTTP Adapters。尽管OSS Python SDK内部使用requests库进行HTTP通信，但是对使用者是透明的。
该模块中的 `Session` 、 `Request` 、`Response` 对requests的对应的类做了简单的封装。
"""
import logging
import requests
from requests.structures import CaseInsensitiveDict
from . import exceptions

USER_AGENT = 'zcbot-crawl-sdk'
logger = logging.getLogger(__name__)


class Session(object):

    def send_request(self, req, timeout):
        try:
            return Response(
                requests.request(
                    req.method,
                    req.url,
                    data=req.data,
                    params=req.params,
                    headers=req.headers,
                    stream=True,
                    timeout=timeout,
                    proxies=req.proxies
                )
            )
        except requests.RequestException as e:
            raise exceptions.RequestError(e)


class Request(object):
    def __init__(self, method, url, data=None, params=None, headers=None, app_name='', proxies=None):
        self.method = method
        self.url = url
        self.data = data
        self.params = params or {}
        self.proxies = proxies

        if not isinstance(headers, CaseInsensitiveDict):
            self.headers = CaseInsensitiveDict(headers)
        else:
            self.headers = headers

        if 'Accept-Encoding' not in self.headers:
            self.headers['Accept-Encoding'] = None

        if 'User-Agent' not in self.headers:
            if app_name:
                self.headers['User-Agent'] = USER_AGENT + '/' + app_name
            else:
                self.headers['User-Agent'] = USER_AGENT


class Response(object):
    def __init__(self, response):
        self.response = response
        self.status = response.status_code
        self.headers = response.headers
        self.request_id = response.headers.get('x-zcbot-request-id', '')
        self.response_text = response.text
