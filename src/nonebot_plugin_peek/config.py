"""插件配置模型"""

from nonebot import get_plugin_config
from pydantic import BaseModel, Field, validator


class Config(BaseModel):
    """插件配置项 (前缀: peek_)"""

    peek_hosts: list[str] = Field(
        default=["127.0.0.1:1920"],
        description="PeekAPI 服务地址列表",
    )

    @validator("peek_hosts", always=True)
    @classmethod
    def validate_peek_hosts(cls, v: list[str]) -> list[str]:
        """确保主机列表非空"""
        return v if v else ["127.0.0.1:1920"]

    peek_key: str | None = Field(
        default=None,
        description="API 密钥，用于获取低模糊度/原图",
    )

    peek_default_radius: int = Field(
        default=5,
        description="默认模糊半径，用于普通用户",
    )

    peek_notify_group: str | None = Field(
        default=None,
        description="通知群/频道 ID，收到请求时发送群通知",
    )

    peek_notify_user: str | None = Field(
        default=None,
        description="通知用户 ID，收到请求时私聊发送通知",
    )

    @validator("peek_notify_group", "peek_notify_user", pre=True)
    @classmethod
    def coerce_to_str(cls, v: object) -> str | None:
        """将数字自动转为字符串（兼容 Pydantic V1/V2）"""
        if v is None:
            return None
        return str(v)

    peek_timeout: float = Field(
        default=15.0,
        description="HTTP 请求超时时间（秒）",
    )

    peek_retries: int = Field(
        default=1,
        description="下载失败重试次数",
    )


# 加载配置
plugin_config = get_plugin_config(Config)
