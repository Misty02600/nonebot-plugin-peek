"""命令处理器"""

from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from .config import plugin_config
from .const import (
    FALLBACK_401,
    FALLBACK_403,
    FALLBACK_403_AUDIO,
    FALLBACK_ERROR,
    FALLBACK_ERROR_AUDIO,
    MSG_401,
    MSG_403,
    MSG_ERROR,
)
from .dependencies import APIClientDep, plugin_data_dir
from .service import StatusCode

# region peek 命令

peek = on_command("peek", block=True)


@peek.handle()
async def handle_peek(
    bot: Bot,
    event: MessageEvent,
    client: APIClientDep,
    args: Message = CommandArg(),
):
    """处理 peek 命令 - 获取屏幕截图"""
    arg_text = args.extract_plain_text().strip()
    is_superuser = await SUPERUSER(bot, event)

    # 仅当明确指定"原图"且是超级用户时才获取原图
    if arg_text == "原图" and is_superuser:
        radius = 0
        use_key = True
    else:
        radius = plugin_config.peek_default_radius
        use_key = False

    response = await client.get_screenshot(radius=radius, use_key=use_key)

    match response.status:
        case StatusCode.OK if response.content:
            msg = ""
            screenshot = MessageSegment.image(response.content)
        case StatusCode.UNAUTHORIZED:
            msg = MSG_401
            screenshot = MessageSegment.image(plugin_data_dir / FALLBACK_401)
        case StatusCode.FORBIDDEN:
            msg = MSG_403
            screenshot = MessageSegment.image(plugin_data_dir / FALLBACK_403)
        case _:
            msg = MSG_ERROR
            screenshot = MessageSegment.image(plugin_data_dir / FALLBACK_ERROR)

    # 群通知
    if plugin_config.peek_notify_group:
        await bot.send_group_msg(
            group_id=plugin_config.peek_notify_group,
            message=f"用户 {event.get_user_id()} 请求 peek",
        )
        await bot.send_group_msg(
            group_id=plugin_config.peek_notify_group, message=Message(screenshot)
        )

    # 私聊通知
    if plugin_config.peek_notify_user:
        await bot.send_private_msg(
            user_id=plugin_config.peek_notify_user,
            message=f"用户 {event.get_user_id()} 请求 peek",
        )
        await bot.send_private_msg(
            user_id=plugin_config.peek_notify_user, message=Message(screenshot)
        )

    await peek.finish(message=msg + screenshot, reply_message=True)


# endregion

# region peep 命令

peep = on_command("peep", block=True)


@peep.handle()
async def handle_peep(bot: Bot, event: MessageEvent, client: APIClientDep):
    """处理 peep 命令 - 获取音频录制"""
    response = await client.get_recording()

    match response.status:
        case StatusCode.OK if response.content:
            audio = MessageSegment.record(response.content)
        case StatusCode.FORBIDDEN:
            audio = MessageSegment.record(file=plugin_data_dir / FALLBACK_403_AUDIO)
        case _:
            audio = MessageSegment.record(file=plugin_data_dir / FALLBACK_ERROR_AUDIO)

    # 群通知
    if plugin_config.peek_notify_group:
        await bot.send_group_msg(
            group_id=plugin_config.peek_notify_group,
            message=f"用户 {event.get_user_id()} 请求 peep",
        )
        await bot.send_group_msg(
            group_id=plugin_config.peek_notify_group, message=Message(audio)
        )

    # 私聊通知
    if plugin_config.peek_notify_user:
        await bot.send_private_msg(
            user_id=plugin_config.peek_notify_user,
            message=f"用户 {event.get_user_id()} 请求 peep",
        )
        await bot.send_private_msg(
            user_id=plugin_config.peek_notify_user, message=Message(audio)
        )

    await peep.finish(message=audio)


# endregion
