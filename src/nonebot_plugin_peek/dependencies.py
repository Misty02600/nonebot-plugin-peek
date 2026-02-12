"""依赖注入模块"""

from pathlib import Path
from typing import Annotated

from nonebot.params import Depends
from nonebot_plugin_localstore import get_plugin_data_dir

from .config import plugin_config
from .service import PeekAPIClient, select_active_client

# region PeekAPI 客户端

_clients = [
    PeekAPIClient(
        host=host,
        key=plugin_config.peek_key,
        timeout=plugin_config.peek_timeout,
        retries=plugin_config.peek_retries,
    )
    for host in plugin_config.peek_hosts
]


async def get_active_client() -> PeekAPIClient:
    """获取最活跃的 PeekAPI 客户端"""
    return await select_active_client(_clients)


ActiveClientDep = Annotated[PeekAPIClient, Depends(get_active_client)]

# endregion

# region 数据目录

plugin_data_dir: Path = get_plugin_data_dir()

# endregion
