# [TASK001] - 重构项目：代码优化和结构组织

**Status:** Completed
**Added:** 2026-02-08
**Updated:** 2026-02-08
**Priority:** High

## Original Request

基于 PeekAPI 项目和最新的 NoneBot2 文档，重构 nonebot-plugin-peek 项目，包括代码优化和结构组织。

---

## 最终项目结构 ✅

```
src/nonebot_plugin_peek/
├── __init__.py       # 插件入口、元数据
├── config.py         # 配置模型 (Pydantic)
├── const.py          # 常量定义
├── dependencies.py   # 依赖注入 (APIClientDep, 工具函数)
├── handler.py        # 命令处理器 (peek, peep)
└── service.py        # PeekAPI 客户端
```

---

## 参考项目：nonebot-plugin-jmdownloader

### 学习到的模式

1. **依赖注入**: 使用 `Annotated[T, Depends(...)]` 创建类型别名
2. **分离 dependencies**: 将服务实例化和工具函数放入单独模块
3. **Handler 函数签名**: 通过依赖注入获取服务实例

### 依赖注入示例

```python
# dependencies.py
from typing import Annotated
from nonebot.params import Depends

_api_client = PeekAPIClient(...)

def get_api_client() -> PeekAPIClient:
    return _api_client

APIClientDep = Annotated[PeekAPIClient, Depends(get_api_client)]

# handler.py
@peek.handle()
async def handle_peek(client: APIClientDep):
    response = await client.get_screenshot(...)
```

---

## 完成内容 ✅

| 任务                           | 状态 |
| ------------------------------ | ---- |
| 删除根目录 config.py           | ✅    |
| 更新 pyproject.toml            | ✅    |
| 创建 const.py                  | ✅    |
| 重写 config.py                 | ✅    |
| 创建 service.py                | ✅    |
| **创建 dependencies.py**       | ✅    |
| 重写 handler.py (使用依赖注入) | ✅    |
| 重写 __init__.py               | ✅    |
| 更新 README.md                 | ✅    |
| Ruff 检查通过                  | ✅    |
| Pyright 检查通过               | ✅    |

---

## Progress Log

### 2026-02-08
- 创建任务文件
- 分析 PeekAPI 项目 API 结构
- 学习 NoneBot2 最佳实践
- 执行 Phase 1 重构
- 用户删除了 check 命令
- 分析 jmdownloader 项目架构
- **创建 dependencies.py 模块**
- Handler 改用依赖注入获取 API 客户端
- 所有代码检查通过

---

## 文件说明

### dependencies.py

包含：
- `APIClientDep` - PeekAPI 客户端依赖注入类型
- `plugin_data_dir` / `fallback_dir` - 数据目录
- `get_fallback_image()` - 获取备用图片
- `get_fallback_audio()` - 获取备用音频
- `send_notify()` - 发送通知

### handler.py

包含：
- `peek` 命令 - 获取屏幕截图
- `peep` 命令 - 获取音频录制

每个 handler 通过 `APIClientDep` 获取客户端实例。

---

## 配置项

| 配置项                | 默认值           | 说明             |
| --------------------- | ---------------- | ---------------- |
| `PEEK_HOST`           | `127.0.0.1:1920` | PeekAPI 服务地址 |
| `PEEK_KEY`            | 无               | API 密钥         |
| `PEEK_DEFAULT_RADIUS` | `5`              | 默认模糊半径     |
| `PEEK_NOTIFY_GROUP`   | 无               | 通知群号         |
| `PEEK_TIMEOUT`        | `60.0`           | 请求超时         |
| `PEEK_RETRIES`        | `2`              | 重试次数         |

---

## 命令列表

| 命令         | 权限     | 说明         |
| ------------ | -------- | ------------ |
| `/peek`      | 所有人   | 获取模糊截图 |
| `/peek 原图` | 超级用户 | 获取原图     |
| `/peep`      | 所有人   | 获取音频录制 |
