# [TASK002] - 添加私聊通知用户配置

**Status:** Pending
**Added:** 2026-02-09
**Updated:** 2026-02-09

## Original Request

添加一个配置项 `PEEK_NOTIFY_USER`，用于私聊发送通知给指定用户。和 `PEEK_NOTIFY_GROUP` 一样，填了就会给这个用户私聊发通知，没填就不发。

## Thought Process

当前插件只支持群聊通知（`PEEK_NOTIFY_GROUP`），用户希望增加私聊通知功能。这个需求很合理：

1. 如果机器人主人不想在群里暴露自己被 peek 的信息，可以选择私聊通知
2. 两种通知方式可以共存，也可以单独使用
3. 实现方式与群聊通知类似，使用 `bot.send_private_msg()`

## Implementation Plan

### 1. 添加配置项 (`config.py`)

在 `Config` 类中添加新配置项：

```python
peek_notify_user: int | None = None
"""通知用户 QQ 号，有请求时私聊发送通知"""
```

位置：放在 `peek_notify_group` 下面（第 20-21 行之后）

> 注：使用 `int | None` 而非 `int | str | None`，Pydantic 会自动将 `.env` 中的字符串转换为 int。与现有的 `peek_notify_group` 保持一致（后续可考虑统一优化）。

### 2. 修改 peek 命令通知逻辑 (`handler.py`)

在现有群通知逻辑（第 67-73 行）之后添加私聊通知：

```python
# 群通知
if plugin_config.peek_notify_group:
    gid = int(plugin_config.peek_notify_group)
    await bot.send_group_msg(
        group_id=gid, message=f"用户 {event.get_user_id()} 请求 peek"
    )
    await bot.send_group_msg(group_id=gid, message=Message(screenshot))

# 私聊通知
if plugin_config.peek_notify_user:
    uid = int(plugin_config.peek_notify_user)
    await bot.send_private_msg(
        user_id=uid, message=f"用户 {event.get_user_id()} 请求 peek"
    )
    await bot.send_private_msg(user_id=uid, message=Message(screenshot))
```

### 3. 修改 peep 命令通知逻辑 (`handler.py`)

同上，在第 98-104 行之后添加：

```python
# 私聊通知
if plugin_config.peek_notify_user:
    uid = int(plugin_config.peek_notify_user)
    await bot.send_private_msg(
        user_id=uid, message=f"用户 {event.get_user_id()} 请求 peep"
    )
    await bot.send_private_msg(user_id=uid, message=Message(audio))
```

### 4. 更新 README.md

在配置项表格中添加：

```markdown
|  `PEEK_NOTIFY_USER`   |  否   |       None       |     通知用户 QQ 号     |
```

### 5. 更新 techContext.md

在配置项表格中添加：

```markdown
| `PEEK_NOTIFY_USER`    | int/str/None | None             | 通知用户 QQ 号   |
```

## Progress Tracking

**Overall Status:** Not Started - 0%

### Subtasks
| ID  | Description             | Status      | Updated    | Notes                  |
| --- | ----------------------- | ----------- | ---------- | ---------------------- |
| 2.1 | 添加配置项              | Not Started | 2026-02-09 | config.py 第 21 行后   |
| 2.2 | peek 命令添加私聊通知   | Not Started | 2026-02-09 | handler.py 第 73 行后  |
| 2.3 | peep 命令添加私聊通知   | Not Started | 2026-02-09 | handler.py 第 104 行后 |
| 2.4 | 更新 README 文档        | Not Started | 2026-02-09 | 配置项表格             |
| 2.5 | 更新 techContext 配置表 | Not Started | 2026-02-09 | 配置项表格             |

## Progress Log

### 2026-02-09
- 任务创建
- 确定实现方案：与群聊通知并行，新增 `PEEK_NOTIFY_USER` 配置项
- 细化实现方案，添加具体代码位置和代码片段
