# PLAN-0003：支持多主机并选择最近使用的设备

## 状态

已完成

## 完成时间

2026-02-10

## 最后结果和当前行为

`PEEK_HOSTS` 接受非空主机列表。单主机直接使用，多主机并发读取 `/idle` 并选择空闲时间最短的设备；
所有探测失败时回退到列表第一项。

## 怎么验证的

- 文档迁移时已对照当前 `select_active_client()` 实现复核单主机、最短空闲时间和全部不可达回退分支。
- 实现已进入 `main`：[提交 `65ce025`](https://github.com/Misty02600/nonebot-plugin-peek/commit/65ce02506f9b527279fc816efb12f828485a22ad)。
- 列表配置和验证随后在[提交 `c7cd926`](https://github.com/Misty02600/nonebot-plugin-peek/commit/c7cd9267638ddeaa451625364531f17d7684e145)中定型。

## 审批与提交

- 用户确认：历史任务记录为已完成
- Git 提交：`65ce025`，配置定型 `c7cd926`

## 文档同步到哪里

- [ADR-0002](../../adr/0002-select-least-idle-host.md)
- [命令请求 Flow](../../architecture/flows/command-request.md)

## 已知缺口和后续事项

- 当前没有针对 `select_active_client()` 分支行为的专门单元测试。
- 主机探测依赖 PeekAPI `/idle`；协议无版本协商，且全部探测失败时会继续尝试第一台主机。
