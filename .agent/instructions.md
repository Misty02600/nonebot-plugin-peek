# Project Intelligence: nonebot-plugin-peek

## 项目模式和偏好

### 代码风格

- 使用 Ruff 进行格式化和 lint
- 行长度限制: 88 字符
- 允许中文注释和字符串
- 使用 match case 模式匹配 (Python 3.10+)

### 命名约定

- 配置项前缀: `peek_` (单下划线)
- 命令名: 英文小写 (`peek`, `peep`)
- 模块名: 小写下划线 (`handler.py`, `service.py`)

### 框架使用

- NoneBot2 命令: 使用 `on_command` + `handle()` 装饰器
- 配置: 使用 Pydantic BaseModel + `get_plugin_config`
- HTTP 请求: 使用 httpx AsyncClient
- 存储: 使用 nonebot-plugin-localstore
- 依赖声明: 使用 `require()` 确保加载顺序

### 类型系统

- 使用 dataclass 定义数据结构
- 使用 IntEnum 定义状态码
- 使用 match case + guard 进行类型安全的分支

## 参考项目：nonebot-plugin-jmdownloader

### 分层架构（复杂插件适用）

```
plugin/
├── bot/          # NoneBot 相关
│   ├── dependencies.py   # 依赖注入
│   └── handlers/         # 命令处理器
├── core/         # 业务模型
│   ├── data_models.py
│   └── enums.py
└── infra/        # 外部服务
    ├── api_client.py
    └── data_manager.py
```

### 依赖注入模式

```python
from typing import Annotated
from nonebot.params import Depends

_service = MyService(...)

def get_service() -> MyService:
    return _service

ServiceDep = Annotated[MyService, Depends(get_service)]

# 使用时
async def handler(svc: ServiceDep):
    await svc.do_something()
```

### Handler 多函数模式

```python
on_command("cmd", handlers=[
    check1,      # 校验函数1，可调用 matcher.finish() 终止
    check2,      # 校验函数2
    main_logic,  # 主逻辑
])
```

## 开发工作流

### 常用命令

```bash
# 开发
uv sync
uv run python -m nonebot

# 检查
uv run ruff check src/
uv run ruff format src/
uv run basedpyright

# 测试
uv run pytest
```

### 提交规范

Conventional Commits:
- `feat:` 新功能
- `fix:` 修复
- `docs:` 文档
- `refactor:` 重构
- `test:` 测试

## 关键设计决策

### 2026-02-08 重构决策

1. **配置格式**: 单下划线 (`PEEK_*`) - 简单直观
2. **权限系统**: NoneBot 内置 `SUPERUSER`
3. **API 客户端**: `PeekAPIClient` 类封装请求逻辑
4. **代码结构**: 扁平结构（项目规模小）
5. **匹配守卫**: `case StatusCode.OK if response.content:` 类型安全

### 架构选择

- **简单插件 (如 peek)**: 扁平结构，单个 handler.py
- **复杂插件 (如 jmdownloader)**: 分层架构 bot/core/infra

## Ruff 规则配置

忽略的规则:
- `E402`: 允许模块导入不在顶部 (require 需要)
- `B008`: 允许默认参数调用函数 (NoneBot 依赖注入)
- `TID252`: 允许相对导入
- `RUF001-003`: 允许中文

## 依赖项目

- **PeekAPI**: https://github.com/Misty02600/PeekAPI
  - 本地屏幕截图/录音服务器
  - 必须在目标电脑运行

## 待学习

- 单元测试最佳实践
- 国际化方案
- 更多 NoneBot2 高级特性
- 依赖注入在复杂场景的应用
