"""依赖注入模块"""

import asyncio
from pathlib import Path
from typing import Annotated

from nonebot import require
from nonebot.log import logger
from nonebot.params import Depends

from .config import plugin_config
from .service import PeekAPIClient

require("nonebot_plugin_localstore")
from nonebot_plugin_localstore import get_plugin_data_dir

# region PeekAPI 多主机管理


class HostManager:
    """多主机管理器，自动选择最活跃的主机"""

    def __init__(
        self,
        hosts: list[str],
        key: str | None = None,
        timeout: float = 60.0,
        retries: int = 2,
    ):
        self.clients = [
            PeekAPIClient(host=host, key=key, timeout=timeout, retries=retries)
            for host in hosts
        ]
        self._active_client: PeekAPIClient | None = None

    @property
    def active_client(self) -> PeekAPIClient:
        """获取当前活跃的客户端（默认第一个）"""
        if self._active_client is not None:
            return self._active_client
        return self.clients[0]

    async def select_most_active(self) -> PeekAPIClient:
        """
        选择最近有用户操作的主机

        并发查询所有主机的空闲时间，返回空闲时间最短的主机客户端。
        如果所有主机都无法连接，返回第一个客户端。
        """
        if len(self.clients) == 1:
            self._active_client = self.clients[0]
            return self._active_client

        # 并发查询所有主机
        tasks = [client.get_idle_info() for client in self.clients]
        results = await asyncio.gather(*tasks)

        # 收集有效结果
        valid_results: list[tuple[PeekAPIClient, float]] = []
        for client, idle_info in zip(self.clients, results, strict=True):
            if idle_info is not None:
                valid_results.append((client, idle_info.idle_seconds))
                logger.debug(f"主机 {client.host} 空闲 {idle_info.idle_seconds:.1f}s")

        if not valid_results:
            logger.warning("所有主机均无法获取空闲时间，使用第一个主机")
            self._active_client = self.clients[0]
            return self._active_client

        # 选择空闲时间最短（最近操作）的主机
        self._active_client = min(valid_results, key=lambda x: x[1])[0]
        logger.info(f"选择最活跃主机: {self._active_client.host}")
        return self._active_client


# 初始化主机管理器
_host_manager = HostManager(
    hosts=plugin_config.peek_hosts,
    key=plugin_config.peek_key,
    timeout=plugin_config.peek_timeout,
    retries=plugin_config.peek_retries,
)


def get_host_manager() -> HostManager:
    """获取主机管理器实例"""
    return _host_manager


def get_api_client() -> PeekAPIClient:
    """获取当前活跃的 PeekAPI 客户端实例"""
    return _host_manager.active_client


HostManagerDep = Annotated[HostManager, Depends(get_host_manager)]
APIClientDep = Annotated[PeekAPIClient, Depends(get_api_client)]

# endregion

# region 数据目录

plugin_data_dir: Path = get_plugin_data_dir()

# endregion
