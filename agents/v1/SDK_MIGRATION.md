# SDK 迁移说明（当前版本）

## 迁移目标

从“自定义对话/工具编排”迁移到“Claude Agent SDK + MCP 标准工具”。

当前迁移状态：已完成并稳定运行。

---

## 架构变化

### 旧模式（已移除）

- 自定义会话管理
- 自定义 skill 加载器
- 业务逻辑与工具协议耦合

### 新模式（当前）

- `ClaudeSDKClient` 负责会话生命周期
- `setting_sources=["project"]` 读取项目级 Skills
- `create_sdk_mcp_server` 暴露 MCP 工具
- `master_main.py` 统一入口

---

## 关键迁移点

### 1) Skills 加载

旧：手写加载器
新：SDK 根据 `setting_sources` 自动加载 `.claude/skills/*/SKILL.md`

### 2) 工具协议

旧：普通 async 函数直接被业务层调用
新：通过 `@tool` + `create_sdk_mcp_server` 注册，统一 `mcp__{server}__{tool}` 命名

### 3) 权限策略

当前统一策略：

- Allowed: `Skill`, `Read`, `mcp__eda-tools__*`, `mcp__himaqa-tools__*`
- Disallowed: `Bash`, `Write`, `Edit`, `AskUserQuestion`

### 4) 会话持久化

新增：`data/sessions/<session_id>.json`

- 以 SDK message dataclass 序列化结果为主
- 保留 `ResultMessage.usage` 等标准字段

---

## 本次修复（迁移后的稳定化）

1. 修复 `tools/sdk_tools.py` 中 async 调用未 `await` 问题（`coroutine was never awaited`）。
2. 统一 MCP 包装层与业务层参数口径（EDA/HimaQA 参数名一致）。
3. 收敛权限，避免 Agent 绕行 `Bash/Write`。
4. 固定 `setting_sources=["project"]`，规避用户级配置冲突导致的初始化超时。

---

## 环境要求

- Python 3.10+
- Node.js 与 Claude Code CLI 可用
- `.env` 中配置 `ANTHROPIC_API_KEY`

---

## 迁移后检查清单

- [ ] `python check_sdk_setup.py` 全通过
- [ ] `python master_main.py` 可启动
- [ ] MCP 工具可直接调用（无反复授权）
- [ ] `data/sessions` 有新会话文件
- [ ] `data/projects` / `data/results` 有新增记录

---

## 相关文档

- `ARCHITECTURE.md`
- `USER_GUIDE.md`
- `VERIFY_GUIDE.md`
