# Active Context: nonebot-plugin-peek

## 当前工作重点

项目已完成 **v0.1.0 重构**，代码结构优化完毕。

## 最近变更

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
├── __init__.py   # 插件入口
├── config.py     # 配置模型
├── const.py      # 常量定义
├── handler.py    # 命令处理器
└── service.py    # PeekAPI 客户端
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

## 依赖项目

- **PeekAPI**: 本地屏幕截图/录音服务器
  - GitHub: https://github.com/Misty02600/PeekAPI
  - 端点: `/screen`, `/record`, `/check`

## 备用资源路径

用户需在以下目录放置备用资源：

```
{localstore_data_dir}/nonebot_plugin_peek/fallback/
├── 401.jpg
├── 403.jpg
├── error.jpg
├── 403.wav
└── error.wav
```
