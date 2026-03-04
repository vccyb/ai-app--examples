# Master Agent SDK System

基于 Claude Agent SDK 的单 Agent + 双 Skill 系统，面向 EDA 电路设计与 HimaQA 测试流程。

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 快速开始

```bash
cd /Users/chenyubo/Project/ai-project/agents/v1
source .venv/bin/activate
pip install -r requirements.txt
python check_sdk_setup.py
python master_main.py
```

## 当前实现要点

- `ClaudeSDKClient + ClaudeAgentOptions`
- `setting_sources=["project"]`
- MCP 工具服务器：`eda-tools` + `himaqa-tools`
- 显式允许 `mcp__eda-tools__*` / `mcp__himaqa-tools__*`
- 显式禁用 `Bash/Write/Edit/AskUserQuestion`
- 会话落盘：`data/sessions/<session_id>.json`（SDK 标准消息为主）

## 目录

- `doc/ARCHITECTURE.md`：架构设计与实现说明
- `doc/USER_GUIDE.md`：用户使用手册
- `doc/VERIFY_GUIDE.md`：验证与排障
- `doc/SDK_MIGRATION.md`：迁移与稳定化说明

## Python 版本

要求 `Python 3.10+`。
