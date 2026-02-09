# Project Brief: nonebot-plugin-peek

## 项目概述

`nonebot-plugin-peek` 是一个 NoneBot2 聊天机器人插件，允许群友通过 QQ 机器人远程查看主人电脑的屏幕截图或录制音频。

## 核心功能

1. **屏幕截图 (peek)**
   - 通过 `peek` 命令获取主人电脑的屏幕截图
   - 支持设置模糊半径，保护隐私
   - `peek 原图` 可获取无模糊的原图
   - 超级用户可使用密钥获取特殊权限

2. **音频录制 (peep)**
   - 通过 `peep` 命令获取主人电脑的音频录制
   - 实时录制并返回音频消息

3. **通知功能**
   - 可配置通知群，当有用户请求时发送通知

## 技术栈

- **框架**: NoneBot2 (v2.4.2+)
- **适配器**: OneBot v11 (QQ)
- **Python 版本**: 3.10+
- **包管理**: uv
- **代码规范**: Ruff
- **类型检查**: BasedPyright

## 项目状态

当前版本: **0.1.0** (初步开发版本)

项目处于早期开发阶段，基础功能已实现，但仍需完善。

## 目标用户

- 需要远程查看电脑屏幕的 NoneBot2 机器人用户
- 希望与群友分享电脑状态的用户

## 依赖服务

### PeekAPI

该插件需要配合 [PeekAPI](https://github.com/Misty02600/PeekAPI) 本地服务器使用。

**项目位置**: `e:\Dev\Projects\MigutBot\PeekAPI`

**API 端点**：

| 端点      | 方法     | 功能     | 参数                       | 返回       |
| --------- | -------- | -------- | -------------------------- | ---------- |
| `/screen` | GET      | 屏幕截图 | `r` (模糊半径), `k` (密钥) | image/jpeg |
| `/record` | GET      | 音频录制 | 无                         | audio/wav  |
| `/check`  | GET/POST | 健康检查 | 无                         | 200 OK     |

**状态码**：
- `200`: 成功
- `401`: 密钥错误（低模糊度时需要密钥）
- `403`: 私密模式（瑟瑟中）
- `500`: 服务错误

**配置文件** (`config.toml`):
```toml
[basic]
is_public = true      # 默认公开模式
api_key = "Imkei"     # API 密钥
host = "0.0.0.0"      # 监听 IP
port = 1920           # 监听端口

[screenshot]
radius_threshold = 3   # 模糊半径阈值
main_screen_only = false

[record]
duration = 20         # 录音时长（秒）
gain = 20             # 音量增益
```
