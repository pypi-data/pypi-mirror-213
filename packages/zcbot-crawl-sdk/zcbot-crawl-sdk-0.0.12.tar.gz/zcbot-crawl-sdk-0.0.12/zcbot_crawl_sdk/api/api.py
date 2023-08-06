# -*- coding: utf-8 -*-
import json
import logging
import demjson
from typing import List, Union
from .model import ApiData, StreamApiData, TaskItem
from . import http_client
from . import exceptions

LOGGER = logging.getLogger(__name__)


class _Base(object):
    def __init__(self, auth, endpoint, session=None, app_name='', timeout=60):
        self.auth = auth
        self.session = session or http_client.Session()
        self.endpoint = endpoint.strip().strip('/')
        self.timeout = timeout
        self.app_name = app_name

    def _send_request(self, method, url, **kwargs):
        req = http_client.Request(method, url, app_name=self.app_name, **kwargs)
        # 加入鉴权参数
        self.auth.sign_request(req)
        resp = self.session.send_request(req, timeout=self.timeout)
        if resp.status != 200:
            raise exceptions.BizException(resp)

        return resp

    def _get(self, url, **kwargs):
        return self._send_request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._send_request('POST', url, **kwargs)

    @staticmethod
    def _parse_result(rs):
        if not rs or not rs.response_text:
            raise exceptions.BizException(rs, '响应内容为空')
        js = json.loads(rs.response_text)
        if not js or not js.get('success', False) or js.get('code', -1) < 0:
            raise exceptions.BizException(rs, '业务操作失败')

        return js.get('data', {})


class ZcbotApi(_Base):
    # 简易分拣接口
    def simple_classify(self, task_items: List[Union[TaskItem, dict]]):
        rs = self._post(
            url=f'{self.endpoint}/api/materiel/classify',
            data=demjson.encode(task_items)
        )
        return self._parse_result(rs)

    # 任务分拣接口
    def classify_and_init_task(self, api_data: ApiData):
        rs = self._post(
            url=f'{self.endpoint}/api/materiel/classify-and-init-task',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 商品基础信息采集接口
    def start_sku_info_job(self, api_data: ApiData):
        rs = self._post(
            url=f'{self.endpoint}/api/task/start/sku-info',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 商品价格采集接口
    def start_sku_price_job(self, api_data: ApiData):
        rs = self._post(
            url=f'{self.endpoint}/api/task/start/sku-price',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 商品全量信息采集接口
    def start_sku_full_job(self, api_data: ApiData):
        rs = self._post(
            url=f'{self.endpoint}/api/task/start/sku-full',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 商品主详图采集接口
    def start_sku_image_job(self, api_data: ApiData):
        rs = self._post(
            url=f'{self.endpoint}/api/task/start/sku-image',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 图片结果打包接口
    def start_zip(self, api_data: ApiData):
        rs = self._get(
            url=f'{self.endpoint}/api/zip/zip',
            params=api_data.dict(),
        )
        return self._parse_result(rs)

    # 采集任务取消接口
    def cancel_job(self, batch_id: str, job_id: str = None):
        rs = self._get(
            url=f'{self.endpoint}/api/task/cancel',
            params={'job_id': job_id, 'batch_id': batch_id},
        )
        return self._parse_result(rs)

    # 删除批次接口
    def delete_batch(self, batch_id: str):
        rs = self._get(
            url=f'{self.endpoint}/api/task/delete',
            params={'batch_id': batch_id},
        )
        return self._parse_result(rs)

    # 获取所有平台
    def get_all_platforms(self):
        rs = self._get(
            url=f'{self.endpoint}/api/meta/platforms',
        )
        return self._parse_result(rs)

    # 获取所有平台
    def get_platforms_by_task_type(self, task_type: str):
        rs = self._get(
            url=f'{self.endpoint}/api/meta/task-type/platforms',
            params={'task_type': task_type},
        )
        return self._parse_result(rs)

    # 流式采集发布采集任务接口
    def stream_publish(self, api_data: StreamApiData):
        rs = self._post(
            url=f'{self.endpoint}/api/stream/publish',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 流式采集发布采集任务接口
    def stream_simple_publish(self, api_data: StreamApiData):
        rs = self._post(
            url=f'{self.endpoint}/api/stream/simple-publish',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 条码截图接口
    def barcode_screenshot(self, ):
        pass
