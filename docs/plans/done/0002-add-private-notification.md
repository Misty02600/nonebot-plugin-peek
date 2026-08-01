# PLAN-0002：添加私聊通知目标

## 状态

已完成

## 完成时间

2026-02-09

## 最后结果和当前行为

新增 `PEEK_NOTIFY_USER`，并与 `PEEK_NOTIFY_GROUP` 独立生效。每个已配置目标先收到请求者和命令说明，
再收到与命令发起者相同的完整回复；通知目标 ID 使用字符串以兼容非数字平台标识。

## 怎么验证的

- 插件测试确认通知使用触发命令的 Bot，避免多 Bot 环境选错发送账号。
- 初始实现已进入 `main`：[提交 `8b16a3f`](https://github.com/Misty02600/nonebot-plugin-peek/commit/8b16a3f181f110e74b849c71dbf314b3b3adf940)。
- 触发 Bot 修正已进入 `main`：[提交 `1625108`](https://github.com/Misty02600/nonebot-plugin-peek/commit/16251082826b0f9c898f471eae7c75b43cb4cdcc)。

## 审批与提交

- 用户确认：功能已合入并持续使用
- Git 提交：`8b16a3f`，后续修正 `1625108`

## 文档同步到哪里

- [项目总览](../../architecture/overview.md)
- [命令请求 Flow](../../architecture/flows/command-request.md)

## 已知缺口和后续事项

通知发送尚未与主回复隔离；适配器发送异常可能中断命令发起者的最终回复。
