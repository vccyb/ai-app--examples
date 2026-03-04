# 架构文档 - Master Agent SDK 实现

## 项目概述

本项目是基于 **Claude Agent SDK (Python)** 的单 Agent + 双 Skill 系统，面向 EDA 电路设计与 HimaQA 测试流程。

当前实现目标：
- 使用 SDK 原生 `ClaudeSDKClient` 做多轮会话
- 使用 MCP in-process server 暴露 EDA/HimaQA 工具
- 通过 `setting_sources=["project"]` 加载项目级 Skills
- 会话过程落盘到 `data/sessions/<session_id>.json`（保留 SDK 标准消息结构）

---

## 总体架构

```text
用户输入
  -> master_main.py
  -> ClaudeSDKClient(ClaudeAgentOptions)
     - setting_sources=["project"]
     - mcp_servers={eda-tools, himaqa-tools}
     - allowed_tools=[Skill, Read, mcp__...]
     - disallowed_tools=[Bash, Write, Edit, AskUserQuestion]
  -> Agent 推理 + Skill 选择
  -> MCP 工具调用
  -> storage 持久化 + session 事件落盘
```

---

## 目录结构

```text
agents/v1/
├── .claude/
│   ├── agents/master_agent.md
│   ├── skills/eda-skill/SKILL.md
│   ├── skills/himaqa-skill/SKILL.md
│   └── settings.local.json
├── config/
├── data/
│   ├── sessions/        # 会话事件落盘（SDK 标准消息为主）
│   ├── projects/        # 项目数据
│   └── results/         # 工具执行结果
├── storage/
│   ├── project_store.py
│   └── result_store.py
├── tools/
│   ├── eda_tools.py
│   ├── himaqa_tools.py
│   └── sdk_tools.py
├── master_main.py
├── check_sdk_setup.py
├── README.md
├── USER_GUIDE.md
├── VERIFY_GUIDE.md
└── SDK_MIGRATION.md
```

---

## 运行时配置

`master_main.py` 中的关键 `ClaudeAgentOptions`：

- `setting_sources=["project"]`
- `mcp_servers={"eda-tools": ..., "himaqa-tools": ...}`
- `allowed_tools`：
  - `Skill`
  - `Read`
  - `mcp__eda-tools__*`（5个）
  - `mcp__himaqa-tools__*`（4个）
- `disallowed_tools=["Bash", "Write", "Edit", "AskUserQuestion"]`

设计意图：
- 限制 Agent 绕路执行（例如通过 Bash/Write 伪造流程）
- 强制业务能力走 MCP 工具
- 降低权限弹窗与不确定行为

---

## Skills 机制

项目级 Skills 来源：
- `.claude/skills/eda-skill/SKILL.md`
- `.claude/skills/himaqa-skill/SKILL.md`

说明：
- 使用 `project` source，避免用户级 `~/.claude` 配置与 MCP 初始化冲突
- Skill 负责意图路由与提示词约束
- 实际动作由 MCP 工具完成

---

## 工具层设计

### 1) 业务实现层
- `tools/eda_tools.py`
- `tools/himaqa_tools.py`

这两层是 async 函数，负责业务逻辑与持久化。

### 2) SDK MCP 包装层
- `tools/sdk_tools.py`

职责：
- `@tool(...)` 暴露给 Agent SDK
- 参数口径映射到业务实现口径
- `await` 调用底层 async 工具
- 统一返回 MCP 文本内容

---

## 持久化设计

### 业务数据
- 项目数据：`data/projects/*.json`
- 工具结果：`data/results/*.json`

### 会话数据
`master_main.py` 会把每轮事件写入：
- `data/sessions/<session_id>.json`

数据格式：
- `format: claude-agent-sdk-session-v1`
- `events[]` 以 SDK dataclass `asdict(...)` 结果为主
- 保留 `SystemMessage/AssistantMessage/ResultMessage` 关键字段（例如 `session_id`, `usage`, `result`）

---

## 已知约束

- 若把 `setting_sources` 加入 `"user"`，在当前环境下可能触发 `Control request timeout: initialize`。
- 当前策略禁用了 `Bash/Write/Edit/AskUserQuestion`，属于刻意限制，以保证流程稳定性与可审计性。

---

## 结论

当前版本是“SDK 标准 + MCP 工具优先 + 会话可追溯”的稳定实现：
- 可运行
- 可验证
- 可落盘
- 文档与代码已对齐
