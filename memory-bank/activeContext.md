# Active Context: nonebot-plugin-peek

## 当前工作重点

项目已完成 **TASK005 迁移至 Alconna 通用解析**，插件现已支持所有适配器。

## 最近变更

- [2026-02-16] ✅ 完成 TASK005 迁移至 Alconna
  - 移除 OneBot V11 硬依赖，改用 nonebot-plugin-alconna 通用组件
  - on_command → on_alconna + Alconna/Args 命令定义
  - MessageSegment → Image/Voice 通用消息段
  - Message → UniMessage 通用消息序列
  - bot.send_group/private_msg → UniMessage.send(target=Target(...)) 通用发送
  - 通知 ID 类型 int → str，支持非数字 ID 平台
  - 抽取 _send_notify() 辅助函数消除重复代码
- [2026-02-09] ✅ 完成 TASK002 添加私聊通知用户配置
- [2026-02-08] ✅ 完成 TASK001 项目重构
  - 重新组织项目结构
  - 添加 httpx 和 localstore 依赖
  - 使用单下划线配置 (`PEEK_*`)
  - 封装 PeekAPI 客户端
  - 添加 `/peek_check` 命令
  - 完善 README 文档
- [2026-02-08] 初始化 Memory Bank

## 当前项目结构

```
src/nonebot_plugin_peek/
├── __init__.py      # 插件入口
├── config.py        # 配置模型
├── const.py         # 常量定义
├── dependencies.py  # 依赖注入 & HostManager
├── handler.py       # 命令处理器
└── service.py       # PeekAPI 客户端 & IdleInfo
```

## 下一步建议

### 可选改进

1. **添加测试**: 补充单元测试覆盖
2. **国际化**: 支持多语言消息
3. **更多命令选项**: 如指定分辨率、显示器选择
4. **访问日志**: 记录用户访问历史

## 活跃的决策和考虑

### 已完成

- ✅ 使用单下划线配置 (`PEEK_*`)
- ✅ 使用 NoneBot 内置 SUPERUSER
- ✅ 使用 nonebot-plugin-localstore
- ✅ 创建统一的 PeekAPIClient 类
- ✅ 添加服务健康检查命令
- ✅ 多主机支持（逗号分隔配置）
- ✅ 智能主机选择（基于空闲时间）

## 依赖项目

- **PeekAPI**: 本地屏幕截图/录音服务器
  - GitHub: https://github.com/Misty02600/PeekAPI
  - 端点: `/screen`, `/record`, `/check`, `/idle`

## 备用资源路径

用户需在以下目录放置备用资源：

```
{localstore_data_dir}/nonebot_plugin_peek/
├── 401.jpg
├── 403.jpg
├── error.jpg
├── 403.wav
└── error.wav
```
