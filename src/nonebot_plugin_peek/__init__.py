"""
nonebot-plugin-peek

让群友视奸你的电脑
"""

from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import Config

# 声明依赖
require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")

# 导入处理器 (注册命令)
from . import handlers as handlers

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-peek",
    description="让群友视奸你的电脑",
    usage="""命令:
/peek - 获取屏幕截图（模糊）
/peek 原图 - 获取原图（超级用户）
/peep - 获取音频录制""",
    type="application",
    homepage="https://github.com/Misty02600/nonebot-plugin-peek",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)
