# -*- coding: utf-8 -*-
import logging
import threading
import traceback
from typing import Union, Dict, List
from .model import MsgType

LOGGER = logging.getLogger(__name__)


class AbstractMessageProcess(object):
    """
    抽象消息处理器
    """

    def process_message(self, msg_type: str, msg_data: Union[Dict, List] = None, tenant_code: str = None, batch_id: str = None):
        try:
            if msg_type == MsgType.DATA_SKU_TEXT.name:
                self.process_sku_text_data(tenant_code, batch_id, msg_data)
            elif msg_type == MsgType.DATA_SKU_IMAGES.name:
                self.process_sku_images_data(tenant_code, batch_id, msg_data)
            elif msg_type == MsgType.ACT_CLOSED.name:
                self.process_closed_action(tenant_code, batch_id, msg_data)
            elif msg_type == MsgType.ACT_OPENED.name:
                self.process_opened_action(tenant_code, batch_id, msg_data)
            else:
                self.process_others(tenant_code, batch_id, msg_data, msg_type)
        except Exception:
            LOGGER.error(f'[消息处理]解析异常 batch_id={batch_id}, msg_data={msg_data}, except={traceback.format_exc()}')

    def process_sku_text_data(self, tenant_code: str, batch_id: str, msg_data: Union[Dict, List]):
        print(f'[{threading.current_thread().name}]process: msg_type=process_sku_text_data, msg_data={msg_data}, tenant_code={tenant_code}, batch_id={batch_id}')
        pass

    def process_sku_images_data(self, tenant_code: str, batch_id: str, msg_data: Union[Dict, List]):
        print(f'[{threading.current_thread().name}]process: msg_type=process_sku_images_data, msg_data={msg_data}, tenant_code={tenant_code}, batch_id={batch_id}')
        pass

    def process_opened_action(self, tenant_code: str, batch_id: str, msg_data: Union[Dict, List]):
        print(f'[{threading.current_thread().name}]process: msg_type=process_opened_action, msg_data={msg_data}, tenant_code={tenant_code}, batch_id={batch_id}')
        pass

    def process_closed_action(self, tenant_code: str, batch_id: str, msg_data: Union[Dict, List]):
        print(f'[{threading.current_thread().name}]process: msg_type=process_closed_action, msg_data={msg_data}, tenant_code={tenant_code}, batch_id={batch_id}')
        pass

    def process_others(self, tenant_code: str, batch_id: str, msg_data: Union[Dict, List], msg_type: str):
        LOGGER.error(f'[消息处理]未知类型消息 msg_type={msg_type}, msg_data={msg_data}, tenant_code={tenant_code}, batch_id={batch_id}')


class AbstractStreamMessageProcess(object):
    """
    抽象流式采集消息处理器
    """

    def process_message(self, msg_type: str, msg_data: Union[Dict, List] = None):
        try:
            if msg_type == MsgType.STREAM_SKU_TEXT.name:
                self.process_stream_sku_text(msg_data)
            elif msg_type == MsgType.STREAM_SKU_IMAGES.name:
                self.process_stream_sku_images(msg_data)
            else:
                self.process_others(msg_data, msg_type)
        except Exception:
            LOGGER.error(f'[流采消息]解析异常 {traceback.format_exc()}')
            LOGGER.error(f'[流采消息]解析异常 msg_data={msg_data}, except={traceback.format_exc()}')

    def process_stream_sku_text(self, msg_data: dict):
        print(msg_data)
        pass

    def process_stream_sku_images(self, msg_data: dict):
        print(msg_data)
        pass

    def process_others(self, msg_data: Union[Dict, List], msg_type: str):
        LOGGER.error(f'[流采消息]未知类型消息 msg_type={msg_type}, msg_data={msg_data}')
