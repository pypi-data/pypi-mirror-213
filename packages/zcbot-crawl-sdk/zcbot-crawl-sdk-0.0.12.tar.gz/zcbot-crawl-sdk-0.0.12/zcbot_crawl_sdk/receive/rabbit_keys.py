# -*- coding: UTF-8 -*-

class RabbitKeys(object):

    # 结果集交换机名称
    @staticmethod
    def get_result_exchange_key(app_code: str):
        return f'zcbot.result.{app_code}'

    # 结果集路由名称
    @staticmethod
    def get_result_routing_key(app_code: str, batch_id: str):
        return f'zcbot.result.{app_code}.{batch_id}'

    # 结果集队列名称
    @staticmethod
    def get_result_queue_key(app_code: str, batch_id: str):
        return f'zcbot.result.{app_code}.{batch_id}'

    # ===============================

    # rabbitmq结果集交换机名称
    @staticmethod
    def get_rabbit_stream_result_exchange_key():
        return f'zcbot.stream_result'

    # rabbitmq路由名称
    @staticmethod
    def get_rabbit_stream_result_routing_key(app_code: str):
        return f'zcbot.stream_result.{app_code}'

    # rabbitmq结果集队列名称
    @staticmethod
    def get_rabbit_stream_result_queue_key(app_code: str):
        return f'zcbot.stream_result.{app_code}'
