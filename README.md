<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://github.com/Misty02600/nonebot-plugin-template/releases/download/assets/NoneBotPlugin.png" width="310" alt="logo"></a>

## ✨ nonebot-plugin-peek ✨
[![LICENSE](https://img.shields.io/github/license/Misty02600/nonebot-plugin-peek.svg)](./LICENSE)
[![python](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org)
[![Adapters](https://img.shields.io/badge/Adapters-OneBot%20v11-blue)](#supported-adapters)
<br/>

[![uv](https://img.shields.io/badge/package%20manager-uv-black?logo=uv)](https://github.com/astral-sh/uv)
[![ruff](https://img.shields.io/badge/code%20style-ruff-black?logo=ruff)](https://github.com/astral-sh/ruff)

</div>

## 📖 介绍

让群友实践你的电脑屏幕和音频。需要配合 [PeekAPI](https://github.com/Misty02600/PeekAPI) 服务运行。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-peek --upgrade
使用 **pypi** 源安装

    nb plugin install nonebot-plugin-peek --upgrade -i "https://pypi.org/simple"
使用**清华源**安装

    nb plugin install nonebot-plugin-peek --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"


</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-peek
安装仓库 main 分支

    uv add git+https://github.com/Misty02600/nonebot-plugin-peek@main
</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-peek
安装仓库 main 分支

    pdm add git+https://github.com/Misty02600/nonebot-plugin-peek@main
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-peek
安装仓库 main 分支

    poetry add git+https://github.com/Misty02600/nonebot-plugin-peek@main
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_peek"]

</details>

<details>
<summary>使用 nbr 安装(使用 uv 管理依赖可用)</summary>

[nbr](https://github.com/fllesser/nbr) 是一个基于 uv 的 nb-cli，可以方便地管理 nonebot2

    nbr plugin install nonebot-plugin-peek
使用 **pypi** 源安装

    nbr plugin install nonebot-plugin-peek -i "https://pypi.org/simple"
使用**清华源**安装

    nbr plugin install nonebot-plugin-peek -i "https://pypi.tuna.tsinghua.edu.cn/simple"

</details>


## ⚙️ 配置

插件使用[nonebot_plugin_localstore](https://github.com/nonebot/plugin-localstore)储存数据和下载缓存。


在 nonebot2 项目的 `.env` 文件中添加下表中的配置

|        配置项         | 必填  |        默认值        |               说明                |
| :-------------------: | :---: | :------------------: | :-------------------------------: |
|     `PEEK_HOSTS`      |  否   | `["127.0.0.1:1920"]` | PeekAPI 服务地址列表（JSON 格式） |
|      `PEEK_KEY`       |  否   |         None         |     API 密钥（用于获取原图）      |
| `PEEK_DEFAULT_RADIUS` |  否   |         `5`          |      默认的截图高斯模糊半径       |
|  `PEEK_NOTIFY_GROUP`  |  否   |         None         |        通知群号（群通知）         |
|  `PEEK_NOTIFY_USER`   |  否   |         None         |    通知用户 QQ 号（私聊通知）     |
|    `PEEK_TIMEOUT`     |  否   |        `60.0`        |        请求超时时间（秒）         |
|    `PEEK_RETRIES`     |  否   |         `2`          |           失败重试次数            |

**配置示例**：

```dotenv
# 单主机配置
PEEK_HOSTS=["192.168.1.100:1920"]

# 多主机配置（自动选择最近操作的主机）
PEEK_HOSTS=["pc1.local:1920","pc2.local:1920","192.168.1.100:1920"]

PEEK_KEY=your_secret_key
PEEK_DEFAULT_RADIUS=5
PEEK_NOTIFY_GROUP=123456789
PEEK_NOTIFY_USER=987654321
```

## 🎉 使用

> [!TIP]
> 以下指令需要添加配置的 `COMMAND_START`

### 指令表

|    指令     |   权限   | 需要@ |   范围    |          说明          |
| :---------: | :------: | :---: | :-------: | :--------------------: |
|   `peek`    |  所有人  |  否   | 私聊/群聊 |    获取模糊屏幕截图    |
| `peek 原图` | 超级用户 |  否   | 私聊/群聊 | 获取原图（需配置密钥） |
|   `peep`    |  所有人  |  否   | 私聊/群聊 |      获取音频录制      |

### 备用资源

当请求失败时，插件会尝试返回备用图片/音频。仓库已自带默认资源，位于：

```
data/nonebot_plugin_peek/
├── 401.jpg        # 权限不足时显示
├── 403.jpg        # 私密模式时显示/播放
├── error.jpg      # 错误时显示/播放
├── 403.wav
└── error.wav
```

支持的图片格式：`.jpg` `.png` `.gif` `.webp`
支持的音频格式：`.wav` `.mp3` `.ogg` `.flac`

插件按文件名前缀（`401`、`403`、`error`）匹配，可替换为任意支持的格式。若资源文件不存在，仅发送文字提示。

## 📦 依赖项目

插件需要配合 [PeekAPI](https://github.com/Misty02600/PeekAPI) 使用。如果电脑没有公网，建议搭配 [frp](https://github.com/fatedier/frp) 或者 [Tailscale](https://tailscale.com/)。

## 📄 许可证

本项目采用 [MIT](./LICENSE) 许可证。
