# -*- coding: utf-8 -*-
import json
import logging
import time
import pika
import traceback
from pika.exceptions import StreamLostError
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Union
from ..util.decator import singleton
from .rabbit_keys import RabbitKeys
from .processor import AbstractMessageProcess
from .processor import AbstractStreamMessageProcess

LOGGER = logging.getLogger(__name__)


@singleton
class BatchResultReceiver(object):
    """
    【单例】异步采集结果接收
    1、通道随批次创建，随采集完成自动销毁
    2、消息与队列自动创建自动删除
    3、通道按批次区分
    """
    _biz_inited = False

    def __init__(self, processor: Union[AbstractMessageProcess, Callable], rabbit_uri: str, qos: int = None, queue_expires: int = None, inactivity_timeout: int = None, max_workers: int = None):
        self.processor = processor
        self.rabbit_uri = rabbit_uri
        self.qos = qos or 10
        self.queue_expires = queue_expires or 28800
        self.inactivity_timeout = inactivity_timeout or 1800
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        LOGGER.info(f'[采集结果]监听器初始化 rabbit_uri={self.rabbit_uri}')

    def submit_receiving_task(self, app_code: str, tenant_code: str, batch_id: str):
        try:
            self.executor.submit(self._receive_message, app_code, batch_id, tenant_code)
        except Exception:
            LOGGER.error(traceback.format_exc())

    def _receive_message(self, app_code: str, batch_id: str, tenant_code: str):
        """
        连接消息队列并启动消费，阻塞队列（需要独立线程运行或挂在后台任务运行）
        """
        LOGGER.info(f'[消息接收]开始接收 batch_id={batch_id}')

        if isinstance(self.processor, AbstractMessageProcess):
            _process_func = self.processor.process_message
        else:
            _process_func = self.processor
        _exchange_name = RabbitKeys.get_result_exchange_key(app_code)
        _routing_name = RabbitKeys.get_result_routing_key(app_code, batch_id)
        _queue_name = RabbitKeys.get_result_queue_key(app_code, batch_id)

        connection = pika.BlockingConnection(pika.URLParameters(self.rabbit_uri))
        channel = connection.channel()
        try:
            # 定义
            channel.queue_declare(queue=_queue_name, auto_delete=True, arguments={'x-expires': self.queue_expires * 1000})
            channel.exchange_declare(exchange=_exchange_name)
            channel.queue_bind(queue=_queue_name, exchange=_exchange_name, routing_key=_routing_name)
            LOGGER.info(f'[消息接收]队列信息 queue={_queue_name}, exchange={_exchange_name}, routing={_routing_name}')
            # 接收
            for method, properties, body in channel.consume(_queue_name, inactivity_timeout=self.inactivity_timeout, auto_ack=False):
                # 通道无活动消息一定时间后，自动终止消费（退出循环）
                if not method and not properties:
                    break
                try:
                    headers = properties.headers
                    if not headers:
                        LOGGER.error(f'[消息接收]消息结构异常 properties={properties}, body={body}')
                        continue
                    # 消息解析处理
                    msg_type = headers.get('msg_type', None)
                    body_json = json.loads(body.decode())
                    _process_func(msg_type, body_json, tenant_code, batch_id)
                except (StreamLostError, ConnectionAbortedError):
                    LOGGER.error(f'[消息接收]服务端关闭链接通道 batch_id={batch_id}')
                except Exception:
                    LOGGER.error(f'[消息接收]解析异常 batch_id={batch_id}, {traceback.format_exc()}')
                # 消息确认
                channel.basic_ack(method.delivery_tag)
        except Exception:
            LOGGER.error(f'[消息接收]接收过程异常 queue={_queue_name}, {traceback.format_exc()}')
        finally:
            try:
                # 关闭链接和通道（链接关闭通道自动关闭）
                channel.close()
                connection.close()
                LOGGER.info(f'[消息接收]销毁队列 batch_id={batch_id}, queue={_queue_name}')
            except Exception:
                LOGGER.error(f'[消息接收]关闭链接异常 queue={_queue_name}, {traceback.format_exc()}')

        LOGGER.info(f'[消息接收]接收完成 batch_id={batch_id}')


@singleton
class StreamResultReceiver(object):
    """
    【单例】异步采集结果接收
    1、通道随批次创建，随采集完成自动销毁
    2、消息与队列自动创建自动删除
    3、通道按批次区分
    """

    def __init__(self, processor: Union[AbstractStreamMessageProcess, Callable], rabbit_uri: str, max_watcher_count: int = None, max_processor_count: int = None):
        self.processor = processor
        self.rabbit_uri = rabbit_uri
        # 默认值，和zcbot_spider保持一致
        self.queue_expires = 28800
        _max_watcher_count = max_watcher_count or 4
        _max_processor_count = max_processor_count or 24
        self.watcher_executor = ThreadPoolExecutor(max_workers=_max_watcher_count, thread_name_prefix='stream-watcher')
        self.processor_executor = ThreadPoolExecutor(max_workers=_max_processor_count, thread_name_prefix='stream-processor')
        LOGGER.info(f'[流采结果]监听器初始化 rabbit_uri={self.rabbit_uri}')

    def watch(self, exchange_name: str, routing_name: str, queue_name: str):
        self.watcher_executor.submit(self._receive_message, exchange_name, routing_name, queue_name)

    def _declare(self, exchange_name: str, routing_name: str, queue_name: str):
        # 定义
        connection = pika.BlockingConnection(pika.URLParameters(self.rabbit_uri))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, arguments={'x-expires': self.queue_expires * 1000})
        channel.exchange_declare(exchange=exchange_name)
        channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_name)
        LOGGER.info(f'[流采结果]队列信息 queue={queue_name}, exchange={exchange_name}, routing={routing_name}')

        return connection, channel

    def _receive_message(self, exchange_name: str, routing_name: str, queue_name: str):
        """
        连接消息队列并启动消费，阻塞队列（需要独立线程运行或挂在后台任务运行）
        """
        LOGGER.info(f'[流采结果]开始接收')

        _process_func = self.processor
        if isinstance(self.processor, AbstractStreamMessageProcess):
            _process_func = self.processor.process_message

        connection, channel = self._declare(exchange_name, routing_name, queue_name)
        try:
            # 接收
            for method, properties, body in channel.consume(queue_name, auto_ack=False):
                # 保持通道激活状态
                if not method or not properties or not properties.headers:
                    LOGGER.error(f'[流采结果]无效消息 method={method}, properties={properties}, body={body}')
                    continue
                # 消息解析并发处理
                msg_type = properties.headers.get('msg_type', None)
                body_json = json.loads(body.decode())
                self.processor_executor.submit(_process_func, msg_type, body_json)
                # 消息确认
                channel.basic_ack(method.delivery_tag)
        except (StreamLostError, ConnectionAbortedError):
            LOGGER.error(f'[流采结果]服务端关闭链接通道StreamLostError,ConnectionAbortedError -> 重连 {traceback.format_exc()}')
        except pika.exceptions.ConnectionClosedByBroker:
            LOGGER.error(f'[流采结果]链接关闭异常ConnectionClosedByBroker -> 重连 {traceback.format_exc()}')
        except pika.exceptions.AMQPChannelError:
            LOGGER.error(f'[流采结果]通道关闭异常AMQPChannelError -> 重连 {traceback.format_exc()}')
        except pika.exceptions.AMQPConnectionError:
            LOGGER.error(f'[流采结果]链接关闭异常AMQPConnectionError -> 重连 {traceback.format_exc()}')
        except Exception:
            LOGGER.error(f'[流采结果]接收过程异常 -> 重连 {traceback.format_exc()}')
        finally:
            try:
                # 关闭链接和通道（链接关闭通道自动关闭）
                channel.close()
                connection.close()
                LOGGER.info(f'[流采结果]销毁队列')
            except Exception:
                LOGGER.error(f'[流采结果]关闭链接异常 {traceback.format_exc()}')

            # 递归重试
            time.sleep(10)
            LOGGER.warning(f'[流采结果]异常重试中...')
            self._receive_message(exchange_name, routing_name, queue_name)
