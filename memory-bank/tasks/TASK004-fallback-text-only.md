# [TASK004] - 备用资源不存在时仅发送提示文字

**Status:** Completed
**Added:** 2026-02-10
**Updated:** 2026-02-10

## Original Request

当备用资源（如 `401.jpg`、`error.wav` 等）不存在时，插件不应崩溃，而应仅发送提示文字。
同时将备用资源纳入版本控制，让用户克隆仓库后开箱即用。

## Thought Process

### 问题分析

当前 `handler.py` 中，请求失败时直接引用备用文件：

```python
case StatusCode.UNAUTHORIZED:
    msg = MSG_401
    screenshot = MessageSegment.image(plugin_data_dir / FALLBACK_401)
```

如果文件不存在，`MessageSegment.image()` 发送失败，用户收不到任何反馈。

### 当前状态

- 备用资源在 `data/nonebot_plugin_peek/` 下（localstore 数据目录）
- `data/` 整个被 `.gitignore` 忽略
- 该目录目前 **只用于存放这些备用资源**，没有其他运行时数据
- 用户需要自行准备这些文件

### 方案

**取消 ignore + 文字兜底**：

1. 修改 `.gitignore`，取消忽略 `data/nonebot_plugin_peek/`，跟踪备用资源文件
2. `handler.py` 中发送前检查文件是否存在，不存在则仅发文字

这样：
- 克隆仓库的用户 → 开箱即用，自带默认资源
- 用户可以替换为自定义图片/音频
- 即使资源被删除也不会崩溃

## Implementation Plan

- [x] 1.1 修改 `.gitignore`：`data/*` + `!data/nonebot_plugin_peek/`
- [x] 1.2 确认 `data/nonebot_plugin_peek/` 下的资源文件被 git 跟踪
- [x] 2.1 修改 `handle_peek`：fallback 前检查文件存在性，不存在则仅发文字
- [x] 2.2 修改 `handle_peep`：同上
- [x] 3.1 更新 README：说明资源开箱即用，可自定义替换

## Progress Tracking

**Overall Status:** Completed - 100%

### Subtasks

| ID  | Description                | Status   | Updated    | Notes                                   |
| --- | -------------------------- | -------- | ---------- | --------------------------------------- |
| 1.1 | 修改 .gitignore            | Complete | 2026-02-10 | `data/*` + `!data/nonebot_plugin_peek/` |
| 1.2 | 跟踪资源文件               | Complete | 2026-02-10 | `git add -f` 强制添加                   |
| 2.1 | handle_peek 加文件存在检查 | Complete | 2026-02-10 | 构造 reply Message                      |
| 2.2 | handle_peep 加文件存在检查 | Complete | 2026-02-10 | 同上                                    |
| 3.1 | 更新 README                | Complete | 2026-02-10 |                                         |

## Progress Log

### 2026-02-10
- 创建任务文件
- 确定方案：取消 ignore 跟踪资源 + 文字兜底
- ✅ 修改 `.gitignore`：`data/` → `data/*` + `!data/nonebot_plugin_peek/`
- ✅ `git add -f` 跟踪 5 个资源文件
- ✅ 修改 `handle_peek`：fallback 分支加 `exists()` 检查，构造统一 `reply: Message`
- ✅ 修改 `handle_peep`：同上，peep 的 OK 分支也补上 `msg = ""`
- ✅ 更新 README：备用资源说明改为"仓库自带 + 可自定义 + 不存在发文字"
- ✅ 30 个测试全部通过
- ✅ basedpyright 0 errors, 0 warnings
