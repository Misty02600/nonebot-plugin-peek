# 项目架构

## 先建立一个印象

`nonebot-plugin-peek` 位于聊天平台与 PeekAPI 之间。它不直接接触桌面捕获或音频设备，而是选择目标
PeekAPI、发起 HTTP 请求，并把二进制结果或错误兜底转换成跨适配器消息。

## 项目由什么组成

| 部分 | 负责什么 | 主要依赖 |
|---|---|---|
| 插件入口与配置 | 加载依赖、声明元数据、读取 `PEEK_*` 配置 | NoneBot2、Pydantic |
| 命令处理层 | 注册 `peek`、`peep`，处理权限、回复和通知 | Alconna、UniMessage |
| 客户端选择层 | 建立 PeekAPI 客户端并通过依赖注入提供当前目标 | NoneBot Depends、localstore |
| PeekAPI 客户端 | 请求截图、录音、空闲时间和健康检查，处理重试与状态码 | httpx |
| 备用资源 | 按错误类别和支持的扩展名查找图片或音频 | localstore 数据目录 |
| PeekAPI | 实际执行屏幕截图、模糊、录音和空闲时间检测 | 外部 Windows 服务 |

## 最重要的质量目标和约束

- 隐私边界：普通 `peek` 使用配置的默认模糊半径；只有超级用户在请求 `原图` 时才附带 API Key。
- 适配器解耦：运行时消息构造和目标发送使用 Alconna 通用接口，具体适配器只出现在测试依赖中。
- 故障可见：服务拒绝或不可达时优先发送对应备用资源，资源缺失时至少发送文字提示。
- 多主机确定性：多主机按 `/idle` 的空闲秒数选择，全部查询失败时固定使用第一项。
- 插件依赖 PeekAPI 的 HTTP 契约；它本身没有截图、录音或服务端隐私模式的实现。

## 平时怎么运行和部署

插件作为 NoneBot2 应用的一部分加载，通过 `.env` 提供 `PEEK_*` 配置。一个或多个 PeekAPI
通常运行在目标 Windows 电脑上，NoneBot 通过局域网、内网穿透或组网地址访问它们。

开发环境使用项目内 `.venv` 和 uv；pytest、Ruff、BasedPyright 分别负责测试、代码检查和类型检查。

## 数据和状态放在哪里

| 数据或状态 | 位置 | 生命周期 |
|---|---|---|
| 插件配置 | NoneBot 配置系统中的 `PEEK_*` 字段 | 插件加载时读取 |
| PeekAPI 客户端列表 | `dependencies.py` 模块内 `_clients` | 当前进程 |
| 请求和响应数据 | HTTP 与 `APIResponse` | 单次命令 |
| 备用图片和音频 | localstore 插件数据目录 | 文件持久化 |

插件没有数据库，也不持久化访问日志或主机选择结果。

## 关键流程和决定

- [命令请求 Flow](flows/command-request.md)
- [ADR-0001：使用 Alconna 保持适配器无关](../adr/0001-use-alconna-for-adapter-neutral-messages.md)
- [ADR-0002：按空闲时间选择多主机](../adr/0002-select-least-idle-host.md)

## 已知风险或还不确定的地方

- PeekAPI 没有协议版本协商；服务端响应结构变化需要插件同步兼容。
- 多主机全部无法提供 `/idle` 时仍会请求第一台主机，最终依赖普通错误与重试流程反馈失败。
- 通知发送发生在回复请求者之前；适配器发送通知时抛出的异常可能中断主回复。
