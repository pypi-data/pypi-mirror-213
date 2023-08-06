# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class Auth(object):
    """
    用于鉴权
    """
    def __init__(self, access_key_id='', access_key_secret=''):
        pass

    def sign_request(self, req):
        pass

    def sign_url(self, req):
        return req.url
