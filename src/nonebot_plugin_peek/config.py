"""插件配置模型"""

from nonebot import get_plugin_config
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    """插件配置项 (前缀: peek_)"""

    peek_hosts: list[str] = ["127.0.0.1:1920"]
    """PeekAPI 服务地址列表，使用 JSON 格式 (["host1:port","host2:port"])"""

    @field_validator("peek_hosts", mode="after")
    @classmethod
    def validate_peek_hosts(cls, v: list[str]) -> list[str]:
        """确保主机列表非空"""
        return v if v else ["127.0.0.1:1920"]

    peek_key: str | None = None
    """API 密钥，用于获取低模糊度/原图"""

    peek_default_radius: int = 5
    """默认模糊半径，用于普通用户"""

    peek_notify_group: int | None = None
    """通知群号，收到请求时发送群通知"""

    peek_notify_user: int | None = None
    """通知用户 QQ 号，收到请求时私聊发送通知"""

    peek_timeout: float = 15.0
    """HTTP 请求超时时间（秒）"""

    peek_retries: int = 1
    """下载失败重试次数"""


# 加载配置
plugin_config = get_plugin_config(Config)
