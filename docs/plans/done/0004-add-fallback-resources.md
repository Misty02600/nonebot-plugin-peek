# PLAN-0004：添加备用资源和纯文字兜底

## 状态

已完成

## 完成时间

2026-02-11

## 最后结果和当前行为

仓库提供 401、403 和通用错误的默认图片或音频。请求失败时按固定文件名前缀和支持的扩展名查找资源；
资源不存在时仍发送对应文字，不因本地文件缺失让命令完全失败。

## 怎么验证的

- 当前插件测试确认 localstore 数据目录中的通用错误音频可以被资源查找函数发现；handler 源码在查找结果为
  `None` 时只构造文字消息。
- 初始实现已进入 `main`：[提交 `2c0d7e1`](https://github.com/Misty02600/nonebot-plugin-peek/commit/2c0d7e16acf98b4f33ccfd27cf053965a6d2f814)。
- 通用音频回退格式在[提交 `1625108`](https://github.com/Misty02600/nonebot-plugin-peek/commit/16251082826b0f9c898f471eae7c75b43cb4cdcc)中修正为可发送的 MP3。

## 审批与提交

- 用户确认：历史任务记录为已完成
- Git 提交：`2c0d7e1`，后续修正 `1625108`

## 文档同步到哪里

- [项目总览](../../architecture/overview.md)
- [命令请求 Flow](../../architecture/flows/command-request.md)

## 已知缺口和后续事项

- 当前没有直接执行 handler 并验证“资源缺失时只发送文字”的测试。
- 默认资源不会自动修复被用户删除或替换后的文件；缺失时仅保证文字反馈。
