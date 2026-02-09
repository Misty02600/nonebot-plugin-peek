# System Patterns: nonebot-plugin-peek

## 系统架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   QQ 用户       │────▶│   NoneBot2      │────▶│   PeekAPI       │
│   发送命令      │     │   handler.py    │     │   本地服务      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                        │
                               ▼                        ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │ dependencies.py │     │  截图/录音      │
                        │ APIClientDep    │────▶│   数据          │
                        └─────────────────┘     └─────────────────┘
```

## 模块关系

```
__init__.py
├── require("nonebot_plugin_localstore")
├── import handler  # 注册命令
└── PluginMetadata

dependencies.py
├── require("nonebot_plugin_localstore")
├── _api_client 实例
├── APIClientDep 类型别名
├── plugin_data_dir / fallback_dir
├── get_fallback_image()
├── get_fallback_audio()
└── send_notify()

handler.py
├── dependencies.APIClientDep  # 依赖注入
├── config.plugin_config
├── const.*
├── peek 命令
└── peep 命令

service.py
├── StatusCode (IntEnum)
├── APIResponse (dataclass)
└── PeekAPIClient
    ├── get_screenshot()
    ├── get_recording()
    └── check_health()

config.py
└── Config (Pydantic BaseModel)
    └── peek_* 配置项

const.py
├── MSG_* 消息常量
└── FALLBACK_* 文件名常量
```

## 设计模式

### 1. 依赖注入模式

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

### 2. 响应类型模式

```python
class StatusCode(IntEnum):
    OK = 200
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    ERROR = 500

@dataclass
class APIResponse:
    status: StatusCode
    content: bytes | None = None
```

### 3. 模式匹配 + 守卫

```python
match response.status:
    case StatusCode.OK if response.content:
        # 成功且有内容
    case StatusCode.UNAUTHORIZED:
        # 未授权
    case _:
        # 其他情况
```

## 数据流

### peek 命令流程

```
1. 用户发送 /peek [原图]
           ↓
2. handler.handle_peek() 接收
           ↓
3. NoneBot 注入 APIClientDep
           ↓
4. 检查是否超级用户
           ↓
5. client.get_screenshot()
           ↓
6. match response.status 处理结果
           ↓
7. send_notify() 发送通知（可选）
           ↓
8. peek.finish() 回复用户
```

## 文件存储

```
{localstore_data_dir}/nonebot_plugin_peek/
└── fallback/
    ├── 401.jpg
    ├── 403.jpg
    ├── error.jpg
    ├── 403.wav
    └── error.wav
```

## 权限控制

| 功能              | 权限                |
| ----------------- | ------------------- |
| `/peek` 模糊截图  | 所有人              |
| `/peek 原图` 原图 | 超级用户 (使用 key) |
| `/peep` 录音      | 所有人              |
