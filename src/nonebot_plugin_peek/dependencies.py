"""依赖注入模块"""

from pathlib import Path
from typing import Annotated

from nonebot import require
from nonebot.params import Depends

from .config import plugin_config
from .service import PeekAPIClient

require("nonebot_plugin_localstore")
from nonebot_plugin_localstore import get_plugin_data_dir

# region PeekAPI 客户端

_api_client = PeekAPIClient(
    host=plugin_config.peek_host,
    key=plugin_config.peek_key,
    timeout=plugin_config.peek_timeout,
    retries=plugin_config.peek_retries,
)


def get_api_client() -> PeekAPIClient:
    """获取 PeekAPI 客户端实例"""
    return _api_client


APIClientDep = Annotated[PeekAPIClient, Depends(get_api_client)]

# endregion

# region 数据目录

plugin_data_dir: Path = get_plugin_data_dir()

# endregion
