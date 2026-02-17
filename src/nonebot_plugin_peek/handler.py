"""命令处理器"""

from arclet.alconna import Alconna, Arparma, Option, store_true
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_alconna.uniseg import Image, Target, UniMessage, Voice

from .config import plugin_config
from .const import (
    AUDIO_EXTENSIONS,
    FALLBACK_401,
    FALLBACK_403,
    FALLBACK_ERROR,
    IMAGE_EXTENSIONS,
    MSG_401,
    MSG_403,
    MSG_ERROR,
)
from .dependencies import ActiveClientDep, plugin_data_dir
from .service import StatusCode
from .utils import find_fallback

# region 通知辅助


async def _send_notify(reply: UniMessage, user_id: str, command: str) -> None:
    """向配置的群/用户发送通知

    Args:
        reply: 要转发的回复消息
        user_id: 发起请求的用户 ID
        command: 命令名称 (peek / peep)
    """
    if plugin_config.peek_notify_group:
        group_target = Target(id=plugin_config.peek_notify_group, private=False)
        await UniMessage.text(f"用户 {user_id} 请求 {command}").send(
            target=group_target
        )
        await reply.send(target=group_target)

    if plugin_config.peek_notify_user:
        user_target = Target(id=plugin_config.peek_notify_user, private=True)
        await UniMessage.text(f"用户 {user_id} 请求 {command}").send(target=user_target)
        await reply.send(target=user_target)


# endregion

# region peek 命令

peek = on_alconna(
    Alconna("peek", Option("原图", action=store_true, default=False)),
    use_cmd_start=True,
    block=True,
)


@peek.handle()
async def handle_peek(
    bot: Bot,
    event: Event,
    client: ActiveClientDep,
    result: Arparma,
):
    """处理 peek 命令 - 获取屏幕截图"""
    is_superuser = await SUPERUSER(bot, event)

    # 仅当指定"原图"选项且是超级用户时才获取原图
    if result.query("原图.value") and is_superuser:
        radius = 0
        use_key = True
    else:
        radius = plugin_config.peek_default_radius
        use_key = False

    response = await client.get_screenshot(radius=radius, use_key=use_key)

    match response.status:
        case StatusCode.OK if response.content:
            msg = ""
            screenshot = Image(raw=response.content)
        case StatusCode.UNAUTHORIZED:
            msg = MSG_401
            fallback = find_fallback(plugin_data_dir, FALLBACK_401, IMAGE_EXTENSIONS)
            screenshot = Image(path=fallback) if fallback else None
        case StatusCode.FORBIDDEN:
            msg = MSG_403
            fallback = find_fallback(plugin_data_dir, FALLBACK_403, IMAGE_EXTENSIONS)
            screenshot = Image(path=fallback) if fallback else None
        case _:
            msg = MSG_ERROR
            fallback = find_fallback(plugin_data_dir, FALLBACK_ERROR, IMAGE_EXTENSIONS)
            screenshot = Image(path=fallback) if fallback else None

    # 构造消息
    reply = UniMessage.text(msg) if msg else UniMessage()
    if screenshot:
        reply += screenshot

    # 通知
    await _send_notify(reply, event.get_user_id(), "peek")

    await reply.finish(reply_to=True)


# endregion

# region peep 命令

peep = on_alconna(
    Alconna("peep"),
    use_cmd_start=True,
    block=True,
)


@peep.handle()
async def handle_peep(event: Event, client: ActiveClientDep):
    """处理 peep 命令 - 获取音频录制"""
    response = await client.get_recording()

    match response.status:
        case StatusCode.OK if response.content:
            msg = ""
            audio = Voice(raw=response.content)
        case StatusCode.FORBIDDEN:
            msg = MSG_403
            fallback = find_fallback(plugin_data_dir, FALLBACK_403, AUDIO_EXTENSIONS)
            audio = Voice(path=fallback) if fallback else None
        case _:
            msg = MSG_ERROR
            fallback = find_fallback(plugin_data_dir, FALLBACK_ERROR, AUDIO_EXTENSIONS)
            audio = Voice(path=fallback) if fallback else None

    # 构造消息
    reply = UniMessage.text(msg) if msg else UniMessage()
    if audio:
        reply += audio

    # 通知
    await _send_notify(reply, event.get_user_id(), "peep")

    await reply.finish()


# endregion
