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
    assert __plugin_meta__.supported_adapters is not None
    assert "~onebot.v11" in __plugin_meta__.supported_adapters


@pytest.mark.asyncio
async def test_handlers_loaded(app: App):
    """测试命令处理器加载是否正常"""
    from nonebot import require

    require("nonebot_plugin_peek")

    from nonebot_plugin_peek.handler import peek, peep

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
    assert plugin_config.peek_timeout == 60.0
    assert plugin_config.peek_retries == 2


@pytest.mark.asyncio
async def test_dependencies_loaded(app: App):
    """测试依赖注入模块加载是否正常"""
    from nonebot import require

    require("nonebot_plugin_peek")

    from nonebot_plugin_peek.dependencies import (
        APIClientDep,
        get_api_client,
        plugin_data_dir,
    )

    assert APIClientDep is not None
    assert plugin_data_dir.exists()

    client = get_api_client()
    assert client is not None
