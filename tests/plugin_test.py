"""插件集成测试"""

import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_plugin_metadata(app: App):
    """测试插件元数据加载是否正常"""
    from nonebot import require

    assert require("nonebot_plugin_peek")

    from nonebot_plugin_peek import __plugin_meta__

    assert __plugin_meta__.name == "nonebot-plugin-peek"
    assert __plugin_meta__.description == "让群友视奸你的电脑"
    assert __plugin_meta__.type == "application"


@pytest.mark.asyncio
async def test_handlers_loaded(app: App):
    """测试命令处理器加载是否正常"""
    from nonebot import require

    require("nonebot_plugin_peek")

    from nonebot_plugin_peek.handlers import peek, peep

    assert peek is not None
    assert peep is not None


@pytest.mark.asyncio
async def test_config_loaded(app: App):
    """测试配置加载是否正常"""
    from nonebot import require

    require("nonebot_plugin_peek")

    from nonebot_plugin_peek.config import plugin_config

    assert plugin_config.peek_hosts == ["127.0.0.1:1920"]
    assert plugin_config.peek_default_radius == 5
    assert plugin_config.peek_timeout == 15.0
    assert plugin_config.peek_retries == 1


@pytest.mark.asyncio
async def test_dependencies_loaded(app: App):
    """测试依赖注入模块加载是否正常"""
    from nonebot import require

    require("nonebot_plugin_peek")

    from nonebot_plugin_peek.dependencies import (
        ActiveClientDep,
        plugin_data_dir,
    )

    assert ActiveClientDep is not None
    assert plugin_data_dir.exists()
