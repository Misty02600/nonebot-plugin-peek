"""插件配置模型"""

from nonebot import get_plugin_config
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Config(BaseModel):
    """插件配置项 (前缀: peek_)"""

    model_config = ConfigDict(coerce_numbers_to_str=True)

    peek_hosts: list[str] = Field(
        default=["127.0.0.1:1920"],
        description="PeekAPI 服务地址列表",
    )

    @field_validator("peek_hosts", mode="after")
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
