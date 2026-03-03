# 通用自动化 Agent 系统

一个基于 Anthropic API 的智能自动化 Agent，支持多轮对话、工具调用和会话持久化。

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ 特性

- 🤖 **智能对话**: 自然语言交互，理解复杂指令
- 🛠️ **工具调用**: 自动调用预定义工具执行任务
- 💾 **会话持久化**: 自动保存对话历史，支持会话恢复
- 📝 **动态配置**: 通过 Markdown 文件定义 Agent 行为
- ⚡ **流式响应**: 实时显示 Agent 思考过程
- 🌍 **Unicode 支持**: 完整支持中文、emoji 等特殊字符

---

## 🚀 快速开始

### 安装

```bash
# 进入项目目录
cd agents/v1

# 安装依赖
pip install -r requirements.txt
```

### 配置

编辑 `.env` 文件：

```env
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_BASE_URL=http://127.0.0.1:15721
MODEL=glm-4.7
MAX_TOKENS=4096
TEMPERATURE=0.7
SESSION_DIR=data/sessions
```

### 启动

```bash
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

You: 启动一个 sleep 进程，名称 test，时间 10 秒

Agent: 我来帮你启动进程。

[调用工具: start_process] ✓

**进程启动成功！**

- 进程名称: test
- PID: 12345
- 命令: sleep 10
- 工作目录: /tmp
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 系统架构详解 |
| [USER_GUIDE.md](USER_GUIDE.md) | 完整用户手册 |
| [EXAMPLES.md](EXAMPLES.md) | 实际应用案例 |

---

## 🛠️ 支持的工具

| 工具 | 功能 | 示例 |
|------|------|------|
| `start_process` | 启动新进程 | "启动 sleep 进程，10 秒" |
| `stop_process` | 停止进程 | "停止 test 进程" |
| `list_processes` | 列出所有进程 | "列出所有进程" |
| `get_process_status` | 获取进程状态 | "查看 test 的状态" |

---

## 📁 项目结构

```
agents/v1/
├── .claude/                    # Claude 配置
│   └── agents/
│       └── general_agent.md    # Agent 定义
├── config/                     # 配置管理
│   ├── settings.py             # 全局设置
│   └── security.py             # 安全规则
├── services/                   # 核心服务
│   ├── conversation_manager.py # 对话管理器
│   └── mcp_server.py           # MCP 服务器
├── tools/                      # 工具定义
│   └── process_tools.py        # 进程管理工具
├── utils/                      # 工具类
│   └── agent_loader.py         # Agent 加载器
├── data/                       # 数据存储
│   └── sessions/               # 会话历史
├── main.py                     # 入口文件
├── .env                        # 环境配置
├── requirements.txt            # 依赖列表
├── README.md                   # 项目说明
├── ARCHITECTURE.md             # 架构文档
├── USER_GUIDE.md               # 用户手册
└── EXAMPLES.md                 # 案例手册
```

---

## 💡 使用示例

### 启动进程

```
You: 启动一个 sleep 进程，名称 demo，时间 30 秒，工作目录 /tmp
Agent: 好的，我来启动进程。
[调用工具: start_process] ✓
进程已启动！PID: 12345
```

### 管理进程

```
You: 列出所有进程
Agent: [调用工具: list_processes] ✓
当前运行: demo (PID: 12345)

You: 停止 demo
Agent: [调用工具: stop_process] ✓
进程 demo 已停止。
```

### 会话管理

```bash
# 列出所有会话
python3 main.py list

# 恢复历史会话
python3 main.py resume session_20260304_020000
```

---

## 🎯 核心功能

### 1. 多轮对话

支持上下文维护的多轮对话，Agent 能记住之前的对话内容。

### 2. 工具调用

Agent 可以自动调用工具执行任务：
- 启动和管理进程
- 执行系统命令
- 处理文件操作

### 3. 会话持久化

所有对话自动保存到 `data/sessions/` 目录，支持会话恢复。

### 4. 动态 Agent 定义

通过 Markdown + YAML frontmatter 定义 Agent，无需修改代码。

---

## 🔧 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | API 密钥 | 必填 |
| `ANTHROPIC_BASE_URL` | API 地址 | http://127.0.0.1:15721 |
| `MODEL` | 模型名称 | glm-4.7 |
| `MAX_TOKENS` | 最大 token 数 | 4096 |
| `TEMPERATURE` | 温度参数 | 0.7 |
| `SESSION_DIR` | 会话目录 | data/sessions |

### Agent 定义

编辑 `.claude/agents/general_agent.md`:

```markdown
---
name: general_agent
version: 1.0.0
description: 通用自动化 Agent
---

# Agent Prompt

你是一个智能助手，专门帮助用户管理进程...
```

---

## 🚧 扩展开发

### 添加新工具

1. 在 `tools/` 目录创建新文件
2. 使用 `@tool` 装饰器定义工具
3. 在 `process_turn()` 中注册工具

示例：

```python
# tools/file_tools.py
from typing import Dict

def tool(name: str, description: str, schema: dict):
    def decorator(func):
        func._tool_name = name
        func._tool_description = description
        func._tool_schema = schema
        return func
    return decorator

@tool(
    "read_file",
    "读取文件内容",
    {"path": str}
)
async def read_file(args: Dict) -> Dict:
    with open(args['path']) as f:
        return {"content": f.read()}
```

### 添加新 Agent

创建 `.claude/agents/new_agent.md`:

```markdown
---
name: new_agent
description: 新的 Agent
---

你的自定义 prompt...
```

使用时指定：

```python
manager = ConversationManager(agent_name="new_agent")
```

---

## 🚧 故障排查

### 常见问题

**Q: API 调用失败**
```
A: 检查 .env 文件配置，确认 API Key 正确
```

**Q: 工具调用不工作**
```
A: 确认 API 支持工具调用功能
```

**Q: 会话没有保存**
```
A: 检查 data/sessions/ 目录权限
```

**Q: Unicode 编码错误**
```
A: 此问题已修复，确保使用最新代码
```

更多问题请查看 [USER_GUIDE.md](USER_GUIDE.md)。

---

## 📈 开发路线图

### v1.0 (当前版本)

- ✅ 多轮对话
- ✅ 工具调用
- ✅ 会话持久化
- ✅ Unicode 支持
- ✅ 流式响应

### v1.1 (计划中)

- [ ] 更多工具（文件操作、网络请求）
- [ ] Web UI 界面
- [ ] 数据库存储后端
- [ ] 性能监控
- [ ] 多 Agent 协调

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [Anthropic](https://www.anthropic.com/) - Claude API
- [智谱 AI](https://open.bigmodel.cn/) - GLM 模型

---

**开始使用，体验智能自动化！** 🚀
