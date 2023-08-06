# -*- coding: utf-8 -*-
"""
zcbot_sdk.exceptions
~~~~~~~~~~~~~~
异常类。
"""
OSS_REQUEST_ID = "x-zcbot-request-id"


class BizException(Exception):
    def __init__(self, resp, msg=''):
        #: HTTP 状态码
        self.status = resp.status
        #: 请求ID，用于跟踪一个请求
        self.request_id = resp.headers.get(OSS_REQUEST_ID, '')
        #: HTTP响应体（部分）
        self.body = resp.response_text
        self.msg = msg

    def __str__(self):
        error = {
            'msg': self.msg,
            'status': self.status,
            OSS_REQUEST_ID: self.request_id,
            'body': self.body,
        }
        return str(error)


class RequestError(Exception):
    def __init__(self, e):
        #: HTTP 状态码
        self.status = -1
        #: 请求ID，用于跟踪一个请求
        self.request_id = ''
        #: HTTP响应体（部分）
        self.body = 'RequestError: ' + str(e)
        #: 原始异常信息对象
        self.exception = e

    def __str__(self):
        error = {
            'status': self.status,
            OSS_REQUEST_ID: self.request_id,
            'body': self.body
        }
        return str(error)
