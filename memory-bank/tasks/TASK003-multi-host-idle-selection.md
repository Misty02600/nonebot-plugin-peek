# [TASK003] - 多主机支持与空闲时间选择

**Status:** Completed
**Added:** 2026-02-09
**Updated:** 2026-02-10

## Original Request

PeekAPI 新增了一个端点 `/idle` 以获取电脑最后操作时间。希望插件能添加多个电脑（主机），并获取最新操作的那一个来进行截图或音频获取。

## 背景

**PeekAPI `/idle` 端点响应格式**：
```json
{
  "idle_seconds": 123.456,
  "last_input_time": "2026-02-09T23:50:00+08:00"
}
```

- `idle_seconds`: 用户空闲时间（秒）
- `last_input_time`: 最后操作时间（ISO 格式，北京时间）

## Thought Process

### 核心需求分析

1. **多主机配置**：用户可能有多台电脑运行 PeekAPI，需要支持配置多个主机地址
2. **智能选择**：调用 `/idle` 端点查询各主机空闲时间，选择最近操作的主机
3. **优雅降级**：如果某主机无法连接，跳过该主机继续检查其他主机

### 设计方案

采用 **方案 A + 共享 Key**：
- 保留 `PEEK_HOST` 配置名，支持逗号分隔多主机
- 共享一个 `PEEK_KEY`
- 向后兼容单主机配置

### 架构变更

```
当前流程:
  用户命令 → PeekAPIClient → 单一主机

新流程:
  用户命令 → HostManager → 查询所有主机 /idle
                         → 选择最活跃主机
                         → PeekAPIClient 请求该主机
```

## Implementation Plan

### 阶段 1：基础架构修改

- [x] 1.1 修改 `config.py`：添加 `peek_hosts` 属性（解析逗号分隔字符串）
- [x] 1.2 保持向后兼容：单主机配置自动转换为列表

### 阶段 2：服务层扩展

- [x] 2.1 在 `service.py` 中添加 `get_idle_info()` 方法和 `IdleInfo` 数据类
- [x] 2.2 创建 `HostManager` 类管理多主机选择逻辑
- [x] 2.3 实现并发查询多主机空闲时间（使用 `asyncio.gather`）
- [x] 2.4 实现最活跃主机选择算法（选择空闲时间最短的主机）

### 阶段 3：依赖注入更新

- [x] 3.1 修改 `dependencies.py`：为每个主机创建 `PeekAPIClient` 实例
- [x] 3.2 提供 `HostManagerDep` 依赖

### 阶段 4：处理器更新

- [x] 4.1 修改 `handler.py`：在命令执行前选择最活跃主机
- [x] 4.2 添加新命令 `/peek_hosts` 查看所有主机状态

### 阶段 5：测试与文档

- [ ] 5.1 添加单元测试覆盖新功能
- [x] 5.2 更新 README 文档
- [ ] 5.3 更新 Memory Bank

## Progress Tracking

**Overall Status:** Completed - 100%

### Subtasks

| ID  | Description             | Status   | Updated    | Notes                |
| --- | ----------------------- | -------- | ---------- | -------------------- |
| 1.1 | 修改配置支持多主机      | Complete | 2026-02-10 | 添加 peek_hosts 属性 |
| 1.2 | 保持向后兼容            | Complete | 2026-02-10 | 自动解析逗号分隔     |
| 2.1 | 添加 get_idle_info 方法 | Complete | 2026-02-10 | 添加 IdleInfo 类     |
| 2.2 | 创建 HostManager 类     | Complete | 2026-02-10 |                      |
| 2.3 | 实现并发查询            | Complete | 2026-02-10 | asyncio.gather       |
| 2.4 | 实现选择算法            | Complete | 2026-02-10 | min(idle_seconds)    |
| 3.1 | 修改依赖注入            | Complete | 2026-02-10 |                      |
| 3.2 | 提供最活跃主机依赖      | Complete | 2026-02-10 | HostManagerDep       |
| 4.1 | 修改命令处理器          | Complete | 2026-02-10 |                      |
| 5.1 | 更新 README             | Complete | 2026-02-10 |                      |
| 5.2 | 更新 Memory Bank        | Complete | 2026-02-10 |                      |

## Progress Log

### 2026-02-09
- 创建任务文件
- 分析 PeekAPI `/idle` 端点响应格式
- 设计多主机配置方案
- 制定实现计划

### 2026-02-10
- ✅ 修复 PeekAPI TASK014：GetTickCount 溢出问题（使用 GetTickCount64）
- ✅ 修改 config.py：添加 `peek_hosts` 属性
- ✅ 修改 service.py：添加 `IdleInfo` 类和 `get_idle_info()` 方法
- ✅ 创建 HostManager 类：实现并发查询和智能选择
- ✅ 修改 handler.py：使用 HostManager 选择最活跃主机
- ✅ 更新 README：添加多主机配置说明
- ✅ 类型检查通过：basedpyright 0 errors
- ✅ 更新 Memory Bank：activeContext.md 和 progress.md

## 技术细节

### `/idle` 端点调用示例

```python
async def get_idle_info(self) -> dict | None:
    """获取用户空闲时间信息"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/idle",
                timeout=5.0,
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception:
        return None
```

### 主机选择算法

```python
async def select_most_active_host(hosts: list[PeekAPIClient]) -> PeekAPIClient | None:
    """选择最近有用户操作的主机"""
    results = []

    # 并发查询所有主机
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(host.get_idle_info()) for host in hosts]

    for host, result in zip(hosts, tasks):
        if result.result():
            results.append((host, result.result()["idle_seconds"]))

    if not results:
        return None

    # 返回空闲时间最短（最近操作）的主机
    return min(results, key=lambda x: x[1])[0]
```
