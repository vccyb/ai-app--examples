# 架构文档

## 项目概述

这是一个基于 **Anthropic API** 的智能自动化 Agent 系统，支持多轮对话、工具调用和会话持久化。

### 核心特性

- ✅ **多轮对话管理**：支持上下文维护的对话系统
- ✅ **工具调用**：Agent 可以自动调用预定义工具执行任务
- ✅ **会话持久化**：对话历史自动保存到 JSON 文件
- ✅ **动态 Agent 定义**：通过 Markdown + YAML frontmatter 定义 Agent
- ✅ **流式响应**：实时显示 Agent 思考过程
- ✅ **Unicode 支持**：完整支持中文、emoji 等特殊字符

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         用户界面                             │
│                    (main.py - CLI 交互)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   ConversationManager                         │
│                   (services/conversation_manager.py)          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  会话管理                                          │    │
│  │  - 创建/恢复会话                                   │    │
│  │  - 消息历史管理                                     │    │
│  │  - 会话持久化                                       │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Agent Prompt 管理                                  │    │
│  │  - 从 .md 文件加载                                  │    │
│  │  - YAML frontmatter 解析                            │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Anthropic API Client                      │
│                    (AsyncAnthropic SDK)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  API 请求                                           │    │
│  │  - 流式响应                                         │    │
│  │  - 工具调用                                         │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ↓                               ↓
┌────────────────────┐          ┌────────────────────┐
│   工具系统          │          │   配置管理          │
│  (tools/)          │          │  (config/)         │
│                    │          │                    │
│ • process_tools    │          │ • settings.py      │
│ • start_process    │          │ • security.py      │
│ • stop_process     │          │                    │
│ • list_processes   │          │                    │
└────────────────────┘          └────────────────────┘
         │
         ↓
┌────────────────────┐
│   数据持久化        │
│  (data/sessions/)  │
│                    │
│ • JSON 文件存储     │
│ • 自动保存          │
│ • 会话恢复          │
└────────────────────┘
```

---

## 目录结构

```
agents/v1/
├── .claude/                          # Claude 配置目录
│   └── agents/
│       └── general_agent.md          # Agent 定义（YAML + Markdown）
│
├── config/                           # 配置管理
│   ├── __init__.py
│   ├── settings.py                   # 全局设置
│   └── security.py                   # 安全规则
│
├── services/                         # 核心服务
│   ├── __init__.py
│   ├── conversation_manager.py       # 对话管理器
│   └── mcp_server.py                 # MCP 服务器（预留）
│
├── tools/                            # 工具定义
│   ├── __init__.py
│   └── process_tools.py              # 进程管理工具
│
├── utils/                            # 工具类
│   ├── __init__.py
│   └── agent_loader.py               # Agent 加载器
│
├── data/                             # 数据存储
│   └── sessions/                     # 会话历史（JSON）
│
├── main.py                           # 入口文件
├── .env                              # 环境配置
├── pyproject.toml                    # 项目配置
├── requirements.txt                  # Python 依赖
├── README.md                         # 项目说明
├── ARCHITECTURE.md                   # 架构文档（本文档）
├── USER_GUIDE.md                     # 用户手册
└── EXAMPLES.md                       # 案例手册
```

---

## 核心组件

### 1. ConversationManager（对话管理器）

**文件**: `services/conversation_manager.py`

**职责**:
- 管理多轮对话
- 维护对话历史
- 处理工具调用
- 会话持久化

**核心方法**:

```python
class ConversationManager:
    def __init__(self, agent_name: str, tools_callback=None)
    def start_conversation(self, session_id, initial_context=None)
    async def process_turn(self, session_id, user_message)
    def end_conversation(self, session_id)
    async def close(self)
```

**工作流程**:
1. 加载 Agent prompt
2. 创建/恢复会话
3. 处理用户输入
4. 调用 API（流式）
5. 检测工具调用 → 执行工具 → 返回结果
6. 保存会话

---

### 2. Agent Loader（Agent 加载器）

**文件**: `utils/agent_loader.py`

**职责**:
- 从 Markdown 文件加载 Agent 定义
- 解析 YAML frontmatter
- 提取 prompt 内容

**Agent 定义格式**:

```markdown
---
name: general_agent
description: 通用自动化 Agent
tools: [tool1, tool2]
---

# Agent Prompt 内容

你是一个智能助手...
```

---

### 3. Tool System（工具系统）

**文件**: `tools/process_tools.py`

**职责**:
- 定义可调用工具
- 执行工具逻辑
- 返回执行结果

**工具定义示例**:

```python
@tool(
    "start_process",
    "启动一个新进程",
    {"name": str, "command": str, "working_dir": str}
)
async def start_process(args: Dict) -> Dict:
    # 工具实现
    pass
```

**已实现工具**:
- `start_process`: 启动新进程
- `stop_process`: 停止进程
- `list_processes`: 列出所有进程
- `get_process_status`: 获取进程状态

---

### 4. Configuration（配置管理）

**文件**: `config/settings.py`

**职责**:
- 加载环境变量
- 管理全局配置
- 验证配置有效性

**配置项**:

```env
# .env 文件
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_BASE_URL=http://127.0.0.1:15721
MODEL=glm-4.7
MAX_TOKENS=4096
TEMPERATURE=0.7
SESSION_DIR=data/sessions
```

---

## 数据流

### 对话流程

```
用户输入
  ↓
ConversationManager.process_turn()
  ↓
构建消息历史（最近 20 条）
  ↓
调用 Anthropic API（流式）
  ↓
  ├─ TextEvent → 累积文本 → 显示给用户
  ├─ ContentBlockStartEvent → 检测工具调用
  ├─ ContentBlockDeltaEvent → 收集工具参数
  └─ ContentBlockStopEvent → 完成工具收集
  ↓
如果检测到工具调用：
  ├─ 执行工具函数
  ├─ 获取执行结果
  ├─ 将结果返回给 API
  └─ 继续循环处理最终响应
  ↓
保存会话到 JSON
  ↓
返回给用户
```

### 工具调用流程

```
API 返回 tool_use
  ↓
提取工具名称和参数
  ↓
执行工具函数
  ↓
格式化结果
  ↓
发送 tool_result 给 API
  ↓
API 处理结果 → 最终回复
```

---

## 关键设计决策

### 1. 为什么使用 Markdown 定义 Agent？

**优点**:
- ✅ 易于编辑和维护
- ✅ 支持版本控制
- ✅ 可读性好
- ✅ 符合 Claude Code 标准

**示例**:
```markdown
---
name: general_agent
description: 我的自动化 Agent
---

你是一个专业的助手...
```

### 2. 为什么使用 JSON 存储会话？

**优点**:
- ✅ 人类可读
- ✅ 易于调试
- ✅ 跨语言支持
- ✅ 无需额外依赖

**数据结构**:
```json
{
  "session_id": "session_20260304_012030",
  "agent_name": "general_agent",
  "started_at": "2026-03-04T01:20:30",
  "messages": [
    {
      "role": "user",
      "content": "启动一个进程",
      "timestamp": "2026-03-04T01:20:35"
    }
  ]
}
```

### 3. 为什么使用流式响应？

**优点**:
- ✅ 实时反馈
- ✅ 更好的用户体验
- ✅ 减少感知延迟

**实现**:
```python
async with self.client.messages.stream(...) as stream:
    async for event in stream:
        if event.type == "text":
            yield event.text  # 实时输出
```

---

## 技术栈

### 后端框架

- **Python**: 3.9+
- **AsyncIO**: 异步编程
- **Anthropic SDK**: API 调用

### 依赖包

```
anthropic          # Anthropic API SDK
python-dotenv      # 环境变量管理
pydantic           # 数据验证
pyyaml             # YAML 解析
```

### API

- **模型**: 智谱 GLM-4.7（Claude API 兼容）
- **协议**: HTTP + SSE（Server-Sent Events）
- **特性**: 流式响应、工具调用

---

## 安全考虑

### 1. API 密钥管理

- ✅ 使用 `.env` 文件存储密钥
- ✅ `.gitignore` 排除 `.env`
- ✅ 不在代码中硬编码密钥

### 2. 命令验证

虽然当前实现未启用，但预留了安全验证框架：

```python
# config/security.py
DEFAULT_BLOCKED_COMMANDS = {
    "exec", "system", "eval", "rm -rf"
}

def validate_command(command: str) -> Dict:
    # 验证命令是否安全
    pass
```

### 3. 进程隔离

- 使用 `asyncio.subprocess` 创建隔离进程
- 每个进程独立运行
- 可控的进程生命周期

---

## 扩展性

### 添加新工具

1. 在 `tools/` 目录创建新文件
2. 使用 `@tool` 装饰器定义工具
3. 在 `process_turn()` 中添加工具映射

**示例**:
```python
# tools/file_tools.py

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

1. 在 `.claude/agents/` 创建新 `.md` 文件
2. 定义 Agent prompt 和工具
3. 在代码中指定新的 `agent_name`

**示例**:
```python
manager = ConversationManager(agent_name="researcher")
```

### 自定义存储后端

继承 `ConversationManager` 并重写存储方法：

```python
class DatabaseConversationManager(ConversationManager):
    def _save_session(self, session):
        # 保存到数据库
        pass

    def _load_session(self, session_id):
        # 从数据库加载
        pass
```

---

## 性能优化

### 1. 消息历史限制

只保留最近 20 条消息，避免 token 消耗过大：

```python
messages = session.messages[-20:]
```

### 2. 流式响应

使用流式 API，实时输出，减少等待时间：

```python
async for text in stream.text_stream:
    yield text  # 立即输出
```

### 3. 异步 I/O

所有 I/O 操作都是异步的，提高并发性能：

```python
async def process_turn(...):
    async with self.client.messages.stream(...) as stream:
        # 异步处理
```

---

## 故障处理

### 常见问题

1. **API 超时**
   - 检查网络连接
   - 验证 API 地址和密钥

2. **Unicode 编码错误**
   - 已自动处理非法字符
   - 使用 `_sanitize_for_json()` 清理

3. **会话文件损坏**
   - 删除损坏的文件
   - 系统会自动创建新会话

### 日志调试

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 未来改进

### 短期

- [ ] 添加更多工具（文件操作、网络请求等）
- [ ] 支持多 Agent 协调
- [ ] 添加命令行参数解析

### 长期

- [ ] Web UI 界面
- [ ] 数据库存储后端
- [ ] 分布式任务队列
- [ ] Agent 性能监控

---

## 总结

这是一个简洁、高效的 Agent 系统，核心特性包括：

✅ **简洁的架构**：清晰的模块划分
✅ **易于扩展**：插件化工具系统
✅ **生产就绪**：完整的错误处理和持久化
✅ **开发友好**：Markdown 配置，清晰的代码结构

适合作为学习和开发的起点，可以根据需要灵活扩展。
