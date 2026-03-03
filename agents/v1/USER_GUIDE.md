# 用户手册

## 目录

1. [快速开始](#快速开始)
2. [安装配置](#安装配置)
3. [基本使用](#基本使用)
4. [工具说明](#工具说明)
5. [高级功能](#高级功能)
6. [常见问题](#常见问题)
7. [最佳实践](#最佳实践)

---

## 快速开始

### 30 秒启动

```bash
# 1. 进入项目目录
cd agents/v1

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量（已有 .env 文件）
# 编辑 .env 文件，设置 API Key

# 4. 启动 Agent
python3 main.py
```

### 第一次对话

```
======================================================================
通用自动化 Agent - 交互模式
======================================================================
会话 ID: session_20260304_020000
模型: glm-4.7
Agent: general_agent
可用命令: /sessions (列出所有会话), /quit (退出)
输入消息开始对话

You: 你好
Agent: 你好！我是通用自动化 Agent。
我可以帮你管理进程、执行命令等任务。

有什么我可以帮你的吗？
```

---

## 安装配置

### 系统要求

- **Python**: 3.9 或更高版本
- **操作系统**: macOS, Linux, Windows
- **网络**: 需要访问 API 服务器

### 安装依赖

```bash
pip install -r requirements.txt
```

**依赖列表**:
- `anthropic` - Anthropic API SDK
- `python-dotenv` - 环境变量管理
- `pydantic` - 数据验证
- `pyyaml` - YAML 解析

### 配置环境变量

编辑 `.env` 文件：

```env
# API 配置
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=http://127.0.0.1:15721

# 模型配置
MODEL=glm-4.7
MAX_TOKENS=4096
TEMPERATURE=0.7

# 会话配置
SESSION_DIR=data/sessions
MAX_TURNS=20
```

**重要提示**:
- ⚠️ 不要将 `.env` 文件提交到版本控制
- ⚠️ 保护好你的 API 密钥
- ✅ `.gitignore` 已配置排除 `.env`

---

## 基本使用

### 启动 Agent

```bash
python3 main.py
```

### 对话示例

**示例 1: 启动进程**

```
You: 启动一个 sleep 进程，名称 test，时间 10 秒，工作目录 /tmp

Agent: 我来帮你启动一个 sleep 进程。

[调用工具: start_process] ✓

**进程启动成功！**

| 属性 | 值 |
|------|-----|
| **进程名称** | test |
| **进程 ID** | 12345 |
| **命令** | sleep 10 |
| **工作目录** | /tmp |

进程将在 10 秒后自动结束。
```

**示例 2: 查看进程**

```
You: 列出所有进程

Agent:

[调用工具: list_processes] ✓

**当前运行的进程**

| 进程名称 | PID | 状态 |
|----------|-----|------|
| test | 12345 | ✅ 运行中 |

**总计**: 1 个进程正在运行
```

**示例 3: 停止进程**

```
You: 停止 test 进程

Agent: 好的，我来停止 test 进程。

[调用工具: stop_process] ✓

进程 test 已成功停止。
```

### 退出程序

输入以下任一命令退出：

```
quit
exit
/quit
/exit
```

或按 `Ctrl+C` 强制退出。

---

## 工具说明

### 可用工具

| 工具名称 | 功能 | 参数 |
|---------|------|------|
| `start_process` | 启动新进程 | `name`, `command`, `working_dir` |
| `stop_process` | 停止进程 | `name` |
| `list_processes` | 列出所有进程 | 无 |
| `get_process_status` | 获取进程状态 | `name` |

### 工具详细说明

#### 1. start_process（启动进程）

**功能**: 启动一个新的子进程

**参数**:
- `name` (string): 进程名称，用于标识进程
- `command` (string): 要执行的命令
- `working_dir` (string): 工作目录

**示例**:
```
You: 启动一个名为 my_python 的进程，运行 python script.py，目录 /home/user

Agent: 我来帮你启动进程。

[调用工具: start_process] ✓

进程已启动！
- 名称: my_python
- 命令: python script.py
- 目录: /home/user
- PID: 12345
```

#### 2. stop_process（停止进程）

**功能**: 停止正在运行的进程

**参数**:
- `name` (string): 要停止的进程名称

**示例**:
```
You: 停止 my_python 进程

Agent: 好的，停止进程。

[调用工具: stop_process] ✓

进程 my_python 已停止。
```

#### 3. list_processes（列出进程）

**功能**: 列出所有管理的进程

**参数**: 无

**示例**:
```
You: 列出所有进程

Agent:

[调用工具: list_processes] ✓

当前进程列表：
- my_python (PID: 12345) - 运行中
- test_sleep (PID: 12346) - 运行中
```

#### 4. get_process_status（获取状态）

**功能**: 获取指定进程的详细状态

**参数**:
- `name` (string): 进程名称

**示例**:
```
You: 查看 my_python 的状态

Agent:

[调用工具: get_process_status] ✓

进程 my_python 详细信息：
- 运行状态: 运行中
- PID: 12345
- 启动时间: 2026-03-04 02:00:00
```

---

## 高级功能

### 会话管理

#### 列出所有会话

```
You: /sessions

已保存的会话 (3):
  - session_20260304_020000
  - session_20260304_020500
  - session_20260304_021000
```

#### 恢复旧会话

```bash
# 方法 1: 启动时指定
python3 main.py resume session_20260304_020000

# 方法 2: 启动后通过命令恢复
（暂未实现，但数据已保存）
```

### 会话持久化

所有对话自动保存到 `data/sessions/` 目录：

```
data/sessions/
├── session_20260304_020000.json
├── session_20260304_020500.json
└── session_20260304_021000.json
```

**会话文件内容**:
```json
{
  "session_id": "session_20260304_020000",
  "agent_name": "general_agent",
  "started_at": "2026-03-04T02:00:00",
  "messages": [
    {
      "role": "user",
      "content": "你好",
      "timestamp": "2026-03-04T02:00:05"
    },
    {
      "role": "assistant",
      "content": "你好！有什么可以帮助你的？",
      "timestamp": "2026-03-04T02:00:06"
    }
  ]
}
```

### 自定义 Agent

编辑 `.claude/agents/general_agent.md` 文件：

```markdown
---
name: general_agent
version: 1.0.0
description: 通用自动化 Agent
---

# 你的自定义 Prompt

你是一个专业的助手，专注于...

## 你的特点
- 特点 1
- 特点 2

## 使用指南
...（更多内容）
```

保存后重启 Agent 即可生效。

---

## 常见问题

### Q1: 程序启动报错 "API Key 未设置"

**A**: 检查 `.env` 文件是否存在，并正确设置了 `ANTHROPIC_API_KEY`。

### Q2: 工具调用失败

**A**:
1. 检查 API 是否支持工具调用
2. 查看错误信息，确认参数是否正确
3. 尝试用更明确的指令

### Q3: 会话没有保存

**A**:
1. 检查 `data/sessions/` 目录是否存在
2. 确认程序正常退出（使用 `quit` 命令）
3. 查看是否有权限写入文件

### Q4: Unicode 编码错误

**A**: 此问题已修复。如果仍有问题，请：
1. 确认使用的是最新代码
2. 清理 Python 缓存：`find . -type d -name "__pycache__" -exec rm -rf {} +`

### Q5: 进程启动失败

**A**:
1. 检查命令是否正确
2. 确认工作目录存在
3. 查看错误消息获取详细信息

---

## 最佳实践

### 1. 使用明确的指令

✅ **好的指令**:
```
启动一个名为 test 的进程，运行 sleep 10 命令，工作目录是 /tmp
```

❌ **不好的指令**:
```
启动个进程
```

### 2. 给进程起有意义的名字

✅ **好的命名**:
```
data_processor, web_server, backup_job
```

❌ **不好的命名**:
```
p1, p2, test
```

### 3. 定期清理旧会话

```bash
# 删除 7 天前的会话
find data/sessions/ -name "*.json" -mtime +7 -delete
```

### 4. 使用环境变量管理配置

不同环境使用不同的 `.env` 文件：

```bash
# 开发环境
cp .env.development .env

# 生产环境
cp .env.production .env
```

### 5. 监控进程状态

定期检查进程状态，及时处理异常：

```
You: 查看所有进程的状态

Agent: ...（列出所有进程）

You: 停止有问题的进程

Agent: ...（停止进程）
```

---

## 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 强制退出程序 |
| `Ctrl+D` | 退出程序（如果输入为空） |

---

## 命令参考

### 内置命令

| 命令 | 功能 |
|------|------|
| `/sessions` | 列出所有已保存的会话 |
| `/quit` | 退出程序 |
| `/exit` | 退出程序 |
| `quit` | 退出程序 |
| `exit` | 退出程序 |

---

## 技术支持

### 获取帮助

- 查看 `ARCHITECTURE.md` 了解系统架构
- 查看 `EXAMPLES.md` 查看更多案例
- 查看日志文件排查问题

### 反馈问题

如果遇到问题：
1. 查看常见问题部分
2. 检查日志输出
3. 确认配置是否正确

---

## 更新日志

### v1.0.0 (2026-03-04)

**初始版本**:
- ✅ 多轮对话支持
- ✅ 工具调用功能
- ✅ 会话持久化
- ✅ Unicode 支持
- ✅ 流式响应
- ✅ Agent 定义系统

---

**祝你使用愉快！** 🚀
