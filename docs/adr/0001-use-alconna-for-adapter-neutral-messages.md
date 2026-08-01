# ADR-0001：使用 Alconna 保持适配器无关

## 状态

已采纳

## 日期

2026-02-17

## 当时遇到了什么

插件最初直接使用 OneBot V11 的命令、消息段和发送接口，命令实现与 QQ 适配器绑定。项目希望在不为
每个聊天平台维护一套 handler 的前提下支持更多 NoneBot 适配器，并让群、私聊通知目标可以使用非数字 ID。

## 最后决定

- 使用 `on_alconna` 和 Alconna 命令模型注册 `peek`、`peep`。
- 使用 UniMessage 的 `Image`、`Voice`、`Target` 构造回复和通知。
- 插件支持的适配器继承自 `nonebot_plugin_alconna`，运行时不依赖具体适配器。
- 通知目标 ID 在配置层统一为字符串；OneBot V11 只作为测试适配器保留。

## 为什么这样选

Alconna 已提供命令解析、通用消息段和跨适配器目标发送，能够把平台差异留在统一抽象层内，并保持现有
命令名称和使用方式不变。

## 没有采用的方案

- 继续只支持 OneBot V11：实现简单，但会把命令、消息和通知长期锁定在 QQ 协议上。
- 在插件内部维护适配器分支：无需额外抽象依赖，但每增加一个平台都要复制发送和消息转换逻辑。

## 带来的影响

- 有利：命令处理代码只维护一份，插件元数据能够声明 Alconna 支持的适配器集合。
- 代价：消息能力和目标寻址受 Alconna 及具体适配器实现约束。
- 风险：跨适配器通知仍需使用触发命令的 Bot；缺少对应 Bot 或目标格式不兼容时发送可能失败。

## 落实与确认

- 实施情况：已落实
- 代码：[`__init__.py`](../../src/nonebot_plugin_peek/__init__.py)、[`handlers.py`](../../src/nonebot_plugin_peek/handlers.py)
- 历史证据：[提交 `c630d60`](https://github.com/Misty02600/nonebot-plugin-peek/commit/c630d608623cb0ca9d256a87e77c268afaccc5e0)

## 相关文档

- [项目总览](../architecture/overview.md)
- [PLAN-0005](../plans/done/0005-migrate-to-alconna.md)
