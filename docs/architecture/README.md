# 从哪里开始看这个项目

## 先记住

- 这是一个 NoneBot2 插件，只负责编排命令、权限、远程请求和消息回复；截图与录音由外部 PeekAPI 完成。
- `peek` 获取屏幕截图，`peek 原图` 为超级用户请求无模糊截图，`peep` 获取录音。
- 多主机配置会优先选择用户空闲时间最短的 PeekAPI；全部不可达时回退到配置中的第一台。
- 命令与消息使用 Alconna 和 UniMessage，运行时不绑定具体聊天适配器。
- 长期事实维护在 `docs/`；不再使用 Memory Bank。

## 按问题查找

| 想知道什么 | 看哪里 |
|---|---|
| 系统边界、组成、数据与风险 | [项目总览](overview.md) |
| 一次截图或录音请求如何完成 | [命令请求 Flow](flows/command-request.md) |
| 为什么使用 Alconna 和当前多主机策略 | [ADR 索引](../adr/README.md) |
| 待办和历史工作 | [Plans](../plans/README.md) |
| 面向使用者的安装、配置和命令 | [项目 README](../../README.md) |
