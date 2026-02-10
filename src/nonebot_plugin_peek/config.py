"""插件配置模型"""

from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    """插件配置项 (前缀: peek_)"""

    peek_host: str = "127.0.0.1:1920"
    """PeekAPI 服务地址，支持逗号分隔多主机 (host1:port,host2:port)"""

    @property
    def peek_hosts(self) -> list[str]:
        """解析为主机列表"""
        return [h.strip() for h in self.peek_host.split(",") if h.strip()]

    peek_key: str | None = None
    """API 密钥，用于获取低模糊度/原图"""

    peek_default_radius: int = 5
    """默认模糊半径，用于普通用户"""

    peek_notify_group: int | None = None
    """通知群号，收到请求时发送群通知"""

    peek_notify_user: int | None = None
    """通知用户 QQ 号，收到请求时私聊发送通知"""

    peek_timeout: float = 60.0
    """HTTP 请求超时时间（秒）"""

    peek_retries: int = 2
    """下载失败重试次数"""


# 加载配置
plugin_config = get_plugin_config(Config)
