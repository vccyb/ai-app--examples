# 案例手册

## 目录

1. [基础案例](#基础案例)
2. [进阶案例](#进阶案例)
3. [实际应用场景](#实际应用场景)
4. [故障排查案例](#故障排查案例)

---

## 基础案例

### 案例 1: 单个进程管理

**场景**: 启动一个 sleep 进程，监控其状态，然后停止。

**完整对话流程**:

```
======================================================================
通用自动化 Agent - 交互模式
======================================================================
会话 ID: session_20260304_020000
模型: glm-4.7
Agent: general_agent
可用命令: /sessions (列出所有会话), /quit (退出)
输入消息开始对话

You: 启动一个 sleep 进程，名称 demo，时间 30 秒，工作目录 /tmp

Agent: 好的，我来为你启动一个 sleep 进程，运行 30 秒，工作目录为 /tmp。

[调用工具: start_process] ✓

**进程启动成功！**

| 属性 | 值 |
|------|-----|
| **进程名称** | demo |
| **进程 ID** | 68591 |
| **命令** | sleep 30 |
| **工作目录** | /tmp |
| **状态** | 运行中 |

You: 查看所有进程

Agent:

[调用工具: list_processes] ✓

**当前运行的进程**

| 进程名称 | 进程 ID (PID) | 状态 |
|----------|---------------|------|
| demo | 68591 | ✅ 运行中 |

**总计**: 1 个进程正在运行

You: 查看 demo 的详细状态

Agent:

[调用工具: get_process_status] ✓

**进程详细信息**

- **进程名称**: demo
- **PID**: 68591
- **运行状态**: ✅ 运行中
- **启动时间**: 2026-03-04 02:00:00

You: 停止 demo 进程

Agent: 好的，我来停止 demo 进程。

[调用工具: stop_process] ✓

进程 demo 已成功停止。

You: 查看所有进程

Agent:

[调用工具: list_processes] ✓

当前没有正在运行的进程。

You: quit
再见！
```

**关键点**:
- ✅ 使用明确的参数（名称、时间、目录）
- ✅ 定期检查进程状态
- ✅ 完成任务后及时停止进程

---

### 案例 2: 批量进程管理

**场景**: 同时启动多个进程，批量管理。

**完整对话流程**:

```
You: 帮我启动 3 个 sleep 进程，分别叫 task1, task2, task3，时间分别是 10, 20, 30 秒，都在 /tmp 目录

Agent: 好的，我来为你启动 3 个 sleep 进程。

[调用工具: start_process] ✓ (task1)
[调用工具: start_process] ✓ (task2)
[调用工具: start_process] ✓ (task3)

**所有进程已启动！**

| 进程名称 | PID | 时间 | 状态 |
|----------|-----|------|------|
| task1 | 68601 | 10 秒 | ✅ 运行中 |
| task2 | 68602 | 20 秒 | ✅ 运行中 |
| task3 | 68603 | 30 秒 | ✅ 运行中 |

You: 列出所有进程

Agent:

[调用工具: list_processes] ✓

**当前运行的进程**

| 进程名称 | PID | 状态 |
|----------|-----|------|
| task1 | 68601 | ✅ 运行中 |
| task2 | 68602 | ✅ 运行中 |
| task3 | 68603 | ✅ 运行中 |

You: 停止所有进程

Agent: 好的，我来停止所有进程。

[调用工具: stop_process] ✓ (task1)
[调用工具: stop_process] ✓ (task2)
[调用工具: stop_process] ✓ (task3)

**所有进程已停止！**

- task1: ✓ 已停止
- task2: ✓ 已停止
- task3: ✓ 已停止

You: 列出所有进程

Agent:

[调用工具: list_processes] ✓

当前没有正在运行的进程。
```

**关键点**:
- ✅ 可以用一条指令管理多个进程
- ✅ Agent 会理解并执行批量操作
- ✅ 每个操作都有清晰的反馈

---

## 进阶案例

### 案例 3: 进程监控和自动清理

**场景**: 启动长期运行的进程，定期检查状态，完成后清理。

**完整对话流程**:

```
You: 启动一个名为 backup 的进程，运行备份脚本 /home/user/backup.sh，工作目录 /home/user

Agent: 好的，我来启动备份进程。

[调用工具: start_process] ✓

**备份进程已启动！**

- 进程名称: backup
- PID: 68700
- 命令: /home/user/backup.sh
- 工作目录: /home/user

You: 查看 backup 的状态

Agent:

[调用工具: get_process_status] ✓

**进程状态**

- **进程名称**: backup
- **PID**: 68700
- **状态**: ✅ 运行中
- **运行时间**: 约 2 分钟

You: （等待 5 分钟后）

You: 查看 backup 的状态

Agent:

[调用工具: get_process_status] ✓

**进程状态**

- **进程名称**: backup
- **PID**: 68700
- **状态**: ⏹️ 已退出
- **退出时间**: 约 7 分钟前

进程已正常完成。如果需要重新启动，请告诉我。

You: 启动一个新的 backup 进程，同样的配置

Agent: 好的，再次启动备份进程。

[调用工具: start_process] ✓

**新的备份进程已启动！**

- 进程名称: backup
- PID: 68750
- 状态: ✅ 运行中
```

**关键点**:
- ✅ 长期进程的监控
- ✅ 检测进程完成状态
- ✅ 可以重启同名进程

---

### 案例 4: 多任务协调

**场景**: 按顺序执行多个任务，每个任务依赖前一个任务。

**完整对话流程**:

```
You: 我需要执行一个数据流程：
1. 先启动数据下载进程 download，运行 python download.py
2. 下载完成后，启动数据处理进程 process，运行 python process.py
3. 处理完成后，启动上传进程 upload，运行 python upload.py
所有进程都在 /data 目录运行

Agent: 好的，我来帮你执行这个数据流程。

首先启动下载进程：

[调用工具: start_process] ✓

**下载进程已启动！**

- 进程名称: download
- PID: 68800
- 命令: python download.py
- 目录: /data

You: （等待下载完成）

You: 查看 download 的状态

Agent:

[调用工具: get_process_status] ✓

进程 download 已完成。

现在启动数据处理进程：

[调用工具: start_process] ✓

**处理进程已启动！**

- 进程名称: process
- PID: 68850
- 命令: python process.py
- 目录: /data

You: （等待处理完成）

You: 查看 process 的状态

Agent:

[调用工具: get_process_status] ✓

进程 process 已完成。

最后启动上传进程：

[调用工具: start_process] ✓

**上传进程已启动！**

- 进程名称: upload
- PID: 68900
- 命令: python upload.py
- 目录: /data

You: 查看 upload 的状态

Agent:

[调用工具: get_process_status] ✓

**数据流程完成！**

所有进程都已成功执行：
- ✅ download - 完成
- ✅ process - 完成
- ✅ upload - 完成
```

**关键点**:
- ✅ Agent 可以理解复杂的多步骤流程
- ✅ 逐步引导执行每个阶段
- ✅ 提供清晰的状态反馈

---

## 实际应用场景

### 场景 1: Web 服务器管理

**需求**: 启动多个 Web 服务器实例，监控状态，按需扩容/缩容。

**操作流程**:

```
You: 启动 3 个 Web 服务器实例，名称 web1, web2, web3，运行 python server.py，端口分别是 8001, 8002, 8003

Agent: 我来为你启动 Web 服务器集群。

[调用工具: start_process] ✓ (web1)
[调用工具: start_process] ✓ (web2)
[调用工具: start_process] ✓ (web3)

**Web 服务器集群已启动！**

| 服务器 | PID | 端口 | 状态 |
|--------|-----|------|------|
| web1 | 69001 | 8001 | ✅ 运行中 |
| web2 | 69002 | 8002 | ✅ 运行中 |
| web3 | 69003 | 8003 | ✅ 运行中 |

You: 查看所有服务器状态

Agent:

[调用工具: list_processes] ✓

所有 Web 服务器正常运行中。

You: 我需要扩容，再加 2 个服务器

Agent: 好的，启动新的服务器实例。

[调用工具: start_process] ✓ (web4)
[调用工具: start_process] ✓ (web5)

**扩容完成！**

现在有 5 个服务器实例在运行。

You: 现在流量少了，停止 web4 和 web5

Agent: 好的，缩容服务器集群。

[调用工具: stop_process] ✓ (web4)
[调用工具: stop_process] ✓ (web5)

**缩容完成！**

当前运行的服务器：
- web1 (端口 8001)
- web2 (端口 8002)
- web3 (端口 8003)
```

---

### 场景 2: 定时任务管理

**需求**: 启动多个定时任务，监控执行情况。

**操作流程**:

```
You: 启动定时任务：
1. cleanup - 清理临时文件，运行 /scripts/cleanup.sh
2. backup - 数据库备份，运行 /scripts/backup.sh
3. report - 生成报告，运行 python /scripts/report.py

Agent: 好的，启动所有定时任务。

[调用工具: start_process] ✓ (cleanup)
[调用工具: start_process] ✓ (backup)
[调用工具: start_process] ✓ (report)

**定时任务已全部启动！**

| 任务 | PID | 脚本 | 状态 |
|------|-----|------|------|
| cleanup | 69101 | cleanup.sh | ✅ 运行中 |
| backup | 69102 | backup.sh | ✅ 运行中 |
| report | 69103 | report.py | ✅ 运行中 |

You: 检查所有任务状态

Agent:

[调用工具: list_processes] ✓
[调用工具: get_process_status] ✓ (cleanup)
[调用工具: get_process_status] ✓ (backup)
[调用工具: get_process_status] ✓ (report)

**任务状态汇总**

- cleanup: ✅ 运行中（已执行 5 分钟）
- backup: ⏹️ 已完成（执行时间: 10 分钟）
- report: ✅ 运行中（已执行 3 分钟）

backup 任务已完成，其他任务继续运行中。

You: 重启 backup 任务

Agent: 好的，重新启动 backup。

[调用工具: start_process] ✓

backup 任务已重新启动（新 PID: 69150）。
```

---

### 场景 3: 开发测试环境

**需求**: 启动开发环境所需的各种服务。

**操作流程**:

```
You: 启动开发环境，需要这些服务：
1. db - 数据库，运行 postgres -D /data/pg
2. redis - 缓存，运行 redis-server
3. api - API 服务，运行 python api.py
4. frontend - 前端服务，运行 npm run dev

Agent: 好的，我来启动完整的开发环境。

[调用工具: start_process] ✓ (db)
数据库启动中...

[调用工具: start_process] ✓ (redis)
缓存启动中...

[调用工具: start_process] ✓ (api)
API 服务启动中...

[调用工具: start_process] ✓ (frontend)
前端服务启动中...

**开发环境已启动！**

| 服务 | PID | 命令 | 状态 |
|------|-----|------|------|
| db | 69201 | postgres | ✅ 运行中 |
| redis | 69202 | redis-server | ✅ 运行中 |
| api | 69203 | python api.py | ✅ 运行中 |
| frontend | 69204 | npm run dev | ✅ 运行中 |

所有服务正常运行，开发环境就绪！

You: 查看所有服务状态

Agent:

[调用工具: list_processes] ✓

**开发环境状态**

所有服务运行正常：
- ✅ db - 数据库
- ✅ redis - 缓存
- ✅ api - API 服务
- ✅ frontend - 前端服务

You: 重启 api 服务

Agent: 好的，重启 API 服务。

[调用工具: stop_process] ✓ (api)
[调用工具: start_process] ✓ (api)

API 服务已重启（新 PID: 69250）。

You: 停止整个开发环境

Agent: 好的，停止所有开发服务。

[调用工具: stop_process] ✓ (db)
[调用工具: stop_process] ✓ (redis)
[调用工具: stop_process] ✓ (api)
[调用工具: stop_process] ✓ (frontend)

**开发环境已关闭！**

所有服务已停止。
```

---

## 故障排查案例

### 案例 5: 处理进程启动失败

**问题**: 进程启动失败，需要诊断原因。

**对话流程**:

```
You: 启动一个进程，名称 test，运行 python /nonexistent/script.py

Agent: 我来启动进程。

[调用工具: start_process] ✗

**进程启动失败！**

错误信息：无法找到文件 /nonexistent/script.py

可能的原因：
1. 文件路径错误
2. 文件不存在
3. 权限不足

You: 检查当前目录下有哪些文件

Agent: （Agent 无法直接列出文件，建议使用正确的路径）

You: 启动进程，使用正确的路径：python ./test.py，工作目录 /tmp

Agent: 好的，使用正确的路径启动。

[调用工具: start_process] ✓

**进程启动成功！**

- 进程名称: test
- PID: 69300
- 命令: python ./test.py
- 工作目录: /tmp
```

**关键点**:
- ✅ Agent 会报告详细的错误信息
- ✅ 提供可能的原因和建议
- ✅ 用户可以修正参数后重试

---

### 案例 6: 处理进程名称冲突

**问题**: 尝试启动同名进程，处理冲突。

**对话流程**:

```
You: 启动进程 worker，运行 python worker.py

Agent: 好的，启动 worker 进程。

[调用工具: start_process] ✗

**启动失败！**

错误：进程 'worker' 已存在

当前运行的进程：
- worker (PID: 69400)

请选择：
1. 停止旧的 worker 进程
2. 使用不同的名称

You: 停止旧的 worker 进程

Agent: 好的，停止 worker。

[调用工具: stop_process] ✓

worker 已停止。现在重新启动：

[调用工具: start_process] ✓

**worker 已重新启动！**

- PID: 69450
- 状态: ✅ 运行中
```

**关键点**:
- ✅ Agent 会检测名称冲突
- ✅ 提供清晰的解决选项
- ✅ 引导用户完成操作

---

### 案例 7: 恢复中断的会话

**问题**: 程序异常退出，需要恢复之前的对话。

**对话流程**:

```bash
# 第一次运行
$ python3 main.py

You: 启动进程 test，运行 sleep 100

Agent: ...（启动进程）

[程序意外中断]

# 再次运行
$ python3 main.py

You: 列出所有会话

Agent: 已保存的会话 (1):
  - session_20260304_020000

You: 恢复会话 session_20260304_020000

Agent: ✓ 已恢复会话: session_20260304_020000（3 条历史消息）

You: 查看之前的对话

Agent: 上一次对话中，我们启动了 test 进程。

让我查看当前状态：

[调用工具: list_processes] ✓

进程 test 仍在运行中。

You: 停止 test

Agent: 好的，停止进程。

[调用工具: stop_process] ✓

test 已停止。
```

**关键点**:
- ✅ 会话自动保存
- ✅ 可以恢复之前的对话
- ✅ 保留完整的上下文

---

## 最佳实践总结

### 1. 进程命名规范

✅ **推荐**:
```
web_server, db_backup, data_processor
task_<id>, service_<type>
```

❌ **不推荐**:
```
p1, p2, test, temp
```

### 2. 监控和日志

```
You: 启动日志监控进程，名称 log_monitor，运行 tail -f /var/log/app.log

Agent: ...（启动进程）

You: 查看监控进程状态

Agent: ...（检查状态）
```

### 3. 资源清理

```
You: 列出所有进程

Agent: ...（显示进程）

You: 停止不需要的进程

Agent: ...（清理进程）
```

### 4. 错误处理

遇到错误时：
1. 仔细阅读错误信息
2. 检查参数是否正确
3. 查看进程状态
4. 必要时重启进程

---

## 总结

通过这些案例，你可以看到 Agent 的强大功能：

- ✅ **简单直观**: 自然语言交互
- ✅ **批量操作**: 一次管理多个进程
- ✅ **智能引导**: 提供清晰的操作步骤
- ✅ **错误处理**: 友好的错误提示和建议
- ✅ **状态监控**: 实时了解进程状态

**开始使用 Agent，让进程管理变得简单高效！** 🚀
