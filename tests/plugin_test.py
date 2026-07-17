"""插件集成测试"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from nonebug import App
from pydantic import ValidationError


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

    from nonebot_plugin_peek.config import Config, plugin_config

    assert plugin_config.peek_hosts == ["127.0.0.1:1920"]
    assert plugin_config.peek_default_radius == 5
    assert plugin_config.peek_timeout == 15.0
    assert plugin_config.peek_retries == 1

    with pytest.raises(ValidationError):
        Config(peek_retries=-1)


@pytest.mark.asyncio
async def test_dependencies_loaded(app: App):
    """测试依赖注入模块加载是否正常"""
    from nonebot import require

    require("nonebot_plugin_peek")

    from nonebot_plugin_peek.const import AUDIO_EXTENSIONS, FALLBACK_ERROR
    from nonebot_plugin_peek.dependencies import (
        ActiveClientDep,
        plugin_data_dir,
    )
    from nonebot_plugin_peek.utils import find_fallback

    assert ActiveClientDep is not None
    assert plugin_data_dir.exists()
    error_audio = find_fallback(plugin_data_dir, FALLBACK_ERROR, AUDIO_EXTENSIONS)
    assert error_audio is not None
    assert error_audio.suffix == ".mp3"


@pytest.mark.asyncio
async def test_notify_uses_triggering_bot(app: App, monkeypatch: pytest.MonkeyPatch):
    """通知应固定使用触发命令的 Bot"""
    from nonebot import require

    require("nonebot_plugin_peek")

    from nonebot_plugin_alconna.uniseg import UniMessage

    from nonebot_plugin_peek.config import plugin_config
    from nonebot_plugin_peek.handlers import _send_notify

    monkeypatch.setattr(plugin_config, "peek_notify_group", "123456789")
    monkeypatch.setattr(plugin_config, "peek_notify_user", None)

    send = AsyncMock()
    monkeypatch.setattr(UniMessage, "send", send)
    bot = MagicMock()

    await _send_notify(bot, UniMessage.text("reply"), "10001", "peek")

    assert send.await_count == 2
    assert all(call.kwargs["bot"] is bot for call in send.await_args_list)
