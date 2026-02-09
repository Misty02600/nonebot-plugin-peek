# Technical Context: nonebot-plugin-peek

## 技术栈

### 核心依赖

| 技术                      | 版本    | 用途             |
| ------------------------- | ------- | ---------------- |
| Python                    | ≥3.10   | 编程语言         |
| NoneBot2                  | ≥2.4.2  | 机器人框架       |
| httpx                     | ≥0.27.0 | HTTP 客户端      |
| nonebot-plugin-localstore | ≥0.7.4  | 数据存储         |
| nonebot-adapter-onebot    | ≥2.4.6  | QQ 适配器 (测试) |

### 开发工具

| 工具         | 用途              |
| ------------ | ----------------- |
| uv           | 包管理器          |
| Ruff         | 代码格式化和 Lint |
| BasedPyright | 类型检查          |
| pytest       | 测试框架          |
| commitizen   | 提交规范          |
| git-cliff    | 变更日志生成      |

## 开发环境设置

### 安装依赖

```bash
# 使用 uv 安装
uv sync

# 安装开发依赖
uv sync --group dev
```

### 运行测试

```bash
uv run pytest
```

### 代码检查

```bash
# Ruff 检查
uv run ruff check src/

# 格式化
uv run ruff format src/

# 类型检查
uv run basedpyright
```

## 项目结构

```
nonebot-plugin-peek/
├── src/
│   └── nonebot_plugin_peek/
│       ├── __init__.py      # 插件入口、元数据
│       ├── config.py        # 配置模型
│       ├── const.py         # 常量定义
│       ├── handler.py       # 命令处理器
│       └── service.py       # PeekAPI 客户端
├── tests/
│   ├── conftest.py
│   ├── fake.py
│   └── plugin_test.py
├── memory-bank/             # Memory Bank
├── pyproject.toml
├── README.md
└── justfile
```

## 配置项

| 配置项                | 类型     | 默认值           | 说明               |
| --------------------- | -------- | ---------------- | ------------------ |
| `PEEK_HOST`           | str      | `127.0.0.1:1920` | PeekAPI 服务地址   |
| `PEEK_KEY`            | str/None | None             | API 密钥           |
| `PEEK_DEFAULT_RADIUS` | int      | 5                | 默认模糊半径       |
| `PEEK_NOTIFY_GROUP`   | int/None | None             | 通知群号（群通知） |
| `PEEK_NOTIFY_USER`    | int/None | None             | 通知用户（私聊）   |
| `PEEK_TIMEOUT`        | float    | 60.0             | 请求超时（秒）     |
| `PEEK_RETRIES`        | int      | 2                | 重试次数           |

## 技术约束

1. **仅支持 OneBot v11**: 目前只适配 QQ 平台
2. **需要 PeekAPI 服务**: 必须在目标电脑运行 PeekAPI
3. **Python 3.10+**: 使用 match case 语法

## 关键模块说明

### service.py - PeekAPIClient

封装所有 PeekAPI 调用：
- `get_screenshot(radius, use_key)` - 获取截图
- `get_recording()` - 获取录音
- `check_health()` - 健康检查

### handler.py - 命令处理器

- `peek` - 截图命令
- `peep` - 录音命令
- `check` - 服务状态检查（超级用户）

### config.py - 配置

使用 Pydantic BaseModel，单下划线前缀 (`PEEK_*`)
