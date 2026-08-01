# 流程：截图与录音命令请求

## 这条流程保证什么

`peek` 和 `peep` 共用同一套目标主机选择、PeekAPI 响应处理、备用资源与通知语义，同时让截图权限
和音频请求保持各自的参数规则。

## 外部参与者和触发条件

- 聊天用户通过 NoneBot 的命令前缀触发 `peek`、`peek 原图` 或 `peep`。
- NoneBot 提供当前 Bot、事件、超级用户权限和依赖注入。
- PeekAPI 提供 `/idle`、`/screen` 和 `/record`。
- 可选通知目标由 `PEEK_NOTIFY_GROUP`、`PEEK_NOTIFY_USER` 配置。

## 稳定的状态变化

1. Alconna 匹配命令，NoneBot 注入 `ActiveClientDep`。
2. 单主机配置直接使用唯一客户端；多主机并发查询 `/idle`，选择 `idle_seconds` 最小的客户端；
   全部查询失败时使用配置列表第一项。
3. `peek` 默认使用 `PEEK_DEFAULT_RADIUS` 且不附带密钥；请求 `原图` 时半径为 `0`，仅超级用户
   会附带 `PEEK_KEY`。`peep` 直接请求 `/record`。
4. 客户端将 200、401、403 原样映射为内部状态；网络异常和其他状态码在首次失败后最多重试
   `PEEK_RETRIES` 次，最终映射为通用错误。
5. 成功响应转换为图片或语音消息。失败响应按状态选择文字和备用资源；找不到资源时只保留文字。
6. 若配置了群或用户通知，插件先通过触发命令的 Bot 发送请求者说明和完整回复副本，再回复原请求者。

## 失败时的语义

- 截图 401：发送权限不足文字，并尽量附带 `401` 图片。
- 截图或录音 403：发送私密模式文字，并尽量附带对应的 `403` 资源。
- 其他状态、空成功响应或请求耗尽重试：发送服务错误文字，并尽量附带 `error` 资源。
- 备用资源缺失不会代替原始错误，也不会阻止纯文字提示。
- 通知发送没有独立隔离；通知目标发送失败可能阻止随后回复命令发起者。

## 相关决定

- [ADR-0001：使用 Alconna 保持适配器无关](../../adr/0001-use-alconna-for-adapter-neutral-messages.md)
- [ADR-0002：按空闲时间选择多主机](../../adr/0002-select-least-idle-host.md)
- [`handlers.py`](../../../src/nonebot_plugin_peek/handlers.py)
- [`service.py`](../../../src/nonebot_plugin_peek/service.py)
