# [TASK005] - 迁移至 Alconna 通用解析

**Status:** Completed
**Added:** 2026-02-16
**Updated:** 2026-02-16
**Priority:** High

## Original Request

利用 Alconna 文档，将当前项目的 OneBot V11 解析替换为 Alconna 通用解析，实现跨平台适配器支持。

---

## 问题分析

### 当前状况

项目当前硬依赖 `nonebot.adapters.onebot.v11`：

1. **handler.py** — 使用 OB11 专属类型：
   - `from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, MessageSegment`
   - `MessageSegment.image(...)` / `MessageSegment.record(...)` 构造消息
   - `bot.send_group_msg(...)` / `bot.send_private_msg(...)` 发送通知
   - `on_command("peek")` 创建响应器

2. **\_\_init\_\_.py** — 声明 `supported_adapters={"~onebot.v11"}`

3. **pyproject.toml** — 依赖 `nonebot-adapter-onebot`

4. **dependencies.py** — 无 OB11 依赖，无需修改

5. **config.py** — `peek_notify_group: int` / `peek_notify_user: int` 使用 QQ 号/群号概念

### 目标

用 `nonebot-plugin-alconna` 的通用组件替换所有 OB11 专属 API，使插件支持任意适配器。

---

## 迁移方案

### 参考文档

- `bot-docs/nonebot2/docs/best-practice/alconna/README.mdx` — 总览
- `bot-docs/nonebot2/docs/best-practice/alconna/matcher.mdx` — `on_alconna` 响应器 & 依赖注入
- `bot-docs/nonebot2/docs/best-practice/alconna/command.md` — Alconna 命令定义
- `bot-docs/nonebot2/docs/best-practice/alconna/uniseg/segment.md` — 通用消息段 (`Image`, `Audio`, `Text` 等)
- `bot-docs/nonebot2/docs/best-practice/alconna/uniseg/message.mdx` — `UniMessage` 构建 & 发送
- `bot-docs/nonebot2/docs/best-practice/alconna/uniseg/utils.mdx` — `Target`, `MsgTarget` 发送对象

### 变更清单

#### 1. 依赖变更

| 文件 | 变更 |
|------|------|
| `pyproject.toml` | 添加 `nonebot-plugin-alconna>=0.59.0`；移除 `nonebot-adapter-onebot` (仅运行时依赖) |
| `__init__.py` | `require("nonebot_plugin_alconna")`；移除 `supported_adapters` 限制 |

#### 2. handler.py — 命令定义 & 消息构造

| 旧 (OB11) | 新 (Alconna) |
|---|---|
| `from nonebot import on_command` | `from nonebot_plugin_alconna import on_alconna` |
| `from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, MessageSegment` | `from nonebot_plugin_alconna import Image, Match, on_alconna` + `from nonebot_plugin_alconna.uniseg import UniMessage, Voice, MsgTarget, Target` |
| `from nonebot.params import CommandArg` | Alconna `Args` + `Match` 依赖注入 |
| `on_command("peek", block=True)` | `on_alconna(Alconna("peek", Args["mode?", str]), use_cmd_start=True, block=True)` |
| `args: Message = CommandArg()` | `mode: Match[str]` 依赖注入 |
| `MessageSegment.image(content)` | `Image(raw=content)` / `Image(path=fallback)` |
| `MessageSegment.record(content)` | `Voice(raw=content)` / `Voice(path=fallback)` (record 对应 Voice) |
| `Message(msg)` + `reply += screenshot` | `UniMessage.text(msg)` + `.image(...)` |
| `await peek.finish(message=reply, reply_message=True)` | `await UniMessage(...).finish(reply_to=True)` |

#### 3. handler.py — 通知发送

| 旧 (OB11) | 新 (Alconna) |
|---|---|
| `bot.send_group_msg(group_id=..., message=...)` | `await UniMessage(...).send(target=Target(id=str(group_id), private=False))` |
| `bot.send_private_msg(user_id=..., message=...)` | `await UniMessage(...).send(target=Target(id=str(user_id), private=True))` |

#### 4. config.py — 通知目标类型 (可选)

- `peek_notify_group: int | None` → `peek_notify_group: str | None` (改为字符串以兼容非数字 ID 平台)
- `peek_notify_user: int | None` → `peek_notify_user: str | None`
- 此为可选变更，初期保持 `int` 也可通过 `str(...)` 转换

#### 5. \_\_init\_\_.py

```python
# 旧
require("nonebot_plugin_localstore")
from . import handler as handler
__plugin_meta__ = PluginMetadata(
    ...
    supported_adapters={"~onebot.v11"},
)

# 新
require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")
from . import handler as handler
__plugin_meta__ = PluginMetadata(
    ...
    # 移除 supported_adapters 或设为 None (支持所有适配器)
)
```

#### 6. 测试更新

- 测试中移除 OB11 相关 mock（`fake.py` 等）
- 使用 Alconna 的测试工具或保持 OB11 作为测试适配器

---

## Implementation Plan

- [ ] 1.1 `pyproject.toml`: 添加 `nonebot-plugin-alconna` 依赖
- [ ] 1.2 `__init__.py`: 添加 `require("nonebot_plugin_alconna")`，移除 `supported_adapters`
- [ ] 2.1 `handler.py`: 替换 import — 移除 OB11，导入 Alconna/UniMessage
- [ ] 2.2 `handler.py`: `on_command` → `on_alconna`，使用 `Alconna` 定义命令
- [ ] 2.3 `handler.py`: `handle_peek` — `MessageSegment.image` → `Image`，`Message` → `UniMessage`
- [ ] 2.4 `handler.py`: `handle_peek` — 通知逻辑改用 `UniMessage.send(target=Target(...))`
- [ ] 2.5 `handler.py`: `handle_peep` — 同上，`MessageSegment.record` → `Voice`
- [ ] 2.6 `handler.py`: `handle_peep` — 通知逻辑改用 `UniMessage.send(target=Target(...))`
- [ ] 2.7 `handler.py`: `finish` 改用 `UniMessage.finish(reply_to=True)`
- [ ] 3.1 `config.py`: 通知 ID 类型 `int | None` → `str | None` (可选)
- [ ] 4.1 更新测试
- [ ] 5.1 运行 basedpyright / ruff 检查
- [ ] 5.2 运行测试确认通过
- [ ] 5.3 更新 README

## Progress Tracking

**Overall Status:** Completed - 100%

### Subtasks

| ID  | Description                        | Status   | Updated    | Notes |
| --- | ---------------------------------- | -------- | ---------- | ----- |
| 1.1 | 添加 alconna 依赖                 | Complete | 2026-02-16 | 移除 nonebot-adapter-onebot 运行时依赖 |
| 1.2 | 更新 __init__.py                   | Complete | 2026-02-16 | require + 移除 supported_adapters |
| 2.1 | handler.py import 替换            | Complete | 2026-02-16 | Bot/Event 从 nonebot.adapters 导入 |
| 2.2 | on_command → on_alconna           | Complete | 2026-02-16 | Alconna + Args |
| 2.3 | handle_peek 消息构造              | Complete | 2026-02-16 | Image(raw/path) + UniMessage |
| 2.4 | handle_peek 通知逻辑              | Complete | 2026-02-16 | _send_notify 辅助函数 |
| 2.5 | handle_peep 消息构造              | Complete | 2026-02-16 | Voice(raw/path) + UniMessage |
| 2.6 | handle_peep 通知逻辑              | Complete | 2026-02-16 | 复用 _send_notify |
| 2.7 | finish 改用 UniMessage            | Complete | 2026-02-16 | reply.finish(reply_to=True) |
| 3.1 | config 通知 ID 类型变更           | Complete | 2026-02-16 | int→str + field_validator 兼容 |
| 4.1 | 更新测试                           | Complete | 2026-02-16 | 修复配置类型 + 旧默认值断言 |
| 5.1 | 代码检查                           | Complete | 2026-02-16 | basedpyright 0 errors, ruff 0 errors |
| 5.2 | 测试通过                           | Complete | 2026-02-16 | 26 passed, 0 failed |
| 5.3 | 更新 README                       | Complete | 2026-02-16 | 适配器标签 + 配置表说明 |

## Progress Log

### 2026-02-16
- 创建任务文件
- 分析当前 OB11 依赖点
- 阅读 Alconna 文档，确定迁移方案
- ✅ pyproject.toml: 添加 nonebot-plugin-alconna，移除 nonebot-adapter-onebot 运行时依赖
- ✅ __init__.py: require("nonebot_plugin_alconna")，移除 supported_adapters
- ✅ config.py: notify ID 类型 int → str + field_validator 兼容旧配置
- ✅ handler.py: 全面迁移
  - on_command → on_alconna + Alconna/Args
  - MessageSegment.image/record → Image/Voice
  - Message → UniMessage
  - bot.send_group_msg/send_private_msg → UniMessage.send(target=Target(...))
  - 抽取 _send_notify() 辅助函数消除重复
- ✅ 测试更新: 配置类型、旧默认值断言、移除 supported_adapters 检查
- ✅ basedpyright 0 errors, ruff 0 errors
- ✅ 26 个测试全部通过
- ✅ 更新 README 适配器标签和配置说明
