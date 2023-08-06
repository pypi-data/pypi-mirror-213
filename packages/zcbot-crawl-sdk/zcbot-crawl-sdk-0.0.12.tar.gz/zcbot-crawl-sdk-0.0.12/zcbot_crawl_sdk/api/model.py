from enum import Enum
from typing import List, Union, Dict
from pydantic import BaseModel, Field
from ..util import time as time_lib


class TaskType(str, Enum):
    """
    任务类型枚举
    """
    # 商品基础信息
    SKU_INFO = 'sku_info'
    # 商品价格
    SKU_PRICE = 'sku_price'
    # 商品基础信息及价格等详细信息
    SKU_FULL = 'sku_full'
    # 商品主详图
    SKU_IMAGE = 'sku_image'
    # 信息抽取
    SKU_EXTRACT = 'sku_extract'
    # 流式采集商品编码（如编码）
    STREAM_SKU_ID = 'stream_sku_id'
    # 流式采集商品价格信息
    STREAM_SKU_PRICE = 'stream_sku_price'
    # 流式采集商品基础信息及价格等详细信息
    STREAM_SKU_FULL = 'stream_sku_full'
    # 流式采集商品主详图
    STREAM_SKU_IMAGE = 'stream_sku_image'
    # 流式采集同款商品
    STREAM_SKU_SAME = "stream_sku_same"


class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # 主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )


class TaskItem(BaseData):
    """
    任务物料模型
    """
    # 对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = None
    # 商品链接
    url: str
    # 用户指定编号(采图时需要)
    rowId: str = None
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = None


class ApiData(BaseModel):
    """
    通用数据接收模型
    """
    # 应用编码
    app_code: str
    # 批次编号
    batch_id: str = None
    # 租户编码
    tenant_code: str = None
    # 任务类型
    task_type: TaskType = None
    # 任务明细清单
    task_items: List[TaskItem] = None
    # 文件名称配置键
    file_name_config: str = 'default'
    # 是否重新打包
    force_rezip: bool = False


class StreamTaskItem(BaseData):
    """
    流式采集任务物料模型
    """
    # 【输入】对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = None
    # 【输入】商品链接
    url: str = None
    # 电商平台编码
    platCode: str = None
    # 【输入】来源APP（流采模式必填）
    appCode: str = None
    # 任务编号（批次）
    batchId: str = None
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = None


class StreamApiData(BaseModel):
    """
    流式采集通用数据接收模型
    """
    # 【输入】应用编码
    app_code: str
    # 【输入】任务类型
    task_type: TaskType = None
    # 【输入】任务明细清单
    task_items: List[StreamTaskItem] = None
    # 【输入】文件名称配置键
    file_name_config: str = 'default'
