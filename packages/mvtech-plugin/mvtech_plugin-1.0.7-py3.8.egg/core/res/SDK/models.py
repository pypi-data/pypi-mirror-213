from pydantic import BaseModel
"""
接入参数 校验工具类
"""


class PLUGIN_BASE_MODEL(BaseModel):
    version: str
    type: str
    body: dict
