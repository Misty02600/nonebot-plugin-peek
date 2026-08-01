# PLAN-0005：迁移到 Alconna 通用消息层

## 状态

已完成

## 完成时间

2026-02-17

## 最后结果和当前行为

命令注册迁移到 `on_alconna`，回复和通知使用 UniMessage 的通用图片、语音与目标类型。运行时移除
OneBot V11 硬依赖，插件元数据继承 Alconna 支持的适配器集合；OneBot 仅作为测试适配器。

## 怎么验证的

- 插件加载测试确认 Alconna handler 正常注册，通知测试确认通用消息通过触发 Bot 发送。
- 实现已进入 `main`：[提交 `c630d60`](https://github.com/Misty02600/nonebot-plugin-peek/commit/c630d608623cb0ca9d256a87e77c268afaccc5e0)。

## 审批与提交

- 用户确认：历史任务记录为已完成
- Git 提交：`c630d60`

## 文档同步到哪里

- [ADR-0001](../../adr/0001-use-alconna-for-adapter-neutral-messages.md)
- [命令请求 Flow](../../architecture/flows/command-request.md)

## 已知缺口和后续事项

跨适配器能力仍受各适配器对图片、语音和主动目标发送的支持程度限制。
