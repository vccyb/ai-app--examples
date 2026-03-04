# Master Agent 验证手册

## 目录

1. [环境验证](#环境验证)
2. [启动与权限验证](#启动与权限验证)
3. [功能验证](#功能验证)
4. [Session 历史验证](#session-历史验证)
5. [故障排除](#故障排除)
6. [回归脚本](#回归脚本)

---

## 环境验证

### 1. Python 与虚拟环境

```bash
python3 --version
which python3
```

要求：Python 3.10+

如使用虚拟环境：

```bash
source .venv/bin/activate
python -V
pip -V
```

### 2. 依赖检查

```bash
python check_sdk_setup.py
```

通过标准：输出 `✓ 所有检查通过！可以启动 Master Agent`

### 3. Skills 与配置文件检查

```bash
ls .claude/skills/*/SKILL.md
cat .env | grep -E "API_KEY|BASE_URL|MODEL"
```

预期：
- 存在 `.claude/skills/eda-skill/SKILL.md`
- 存在 `.claude/skills/himaqa-skill/SKILL.md`
- `.env` 中有 `ANTHROPIC_API_KEY`

---

## 启动与权限验证

### 1. 启动 Agent

```bash
python master_main.py
```

预期启动信息：
- `✓ Agent 已启动`
- 命令行出现 `You:` 提示

### 2. MCP 工具权限验证

在会话中输入：

```text
你好，创建一个测试项目 test_verify
```

预期：
- 出现 `🔧 [mcp__eda-tools__eda_create_project]`
- 不再反复提示你“去界面授权”

当前权限策略（代码级）：
- Allowed: `Skill`、`Read`、`mcp__eda-tools__*`、`mcp__himaqa-tools__*`
- Disallowed: `Bash`、`Write`、`Edit`、`AskUserQuestion`

说明：当前代码已显式允许以下 MCP 工具：
- `mcp__eda-tools__eda_create_project`
- `mcp__eda-tools__eda_add_component`
- `mcp__eda-tools__eda_connect`
- `mcp__eda-tools__eda_simulate`
- `mcp__eda-tools__eda_export`
- `mcp__himaqa-tools__himaqa_upload_netlist`
- `mcp__himaqa-tools__himaqa_notify_manager`
- `mcp__himaqa-tools__himaqa_query_history`
- `mcp__himaqa-tools__himaqa_get_report`

---

## 功能验证

### 测试 1: EDA 设计流程

对话示例：

```text
You: 创建项目 led_verify
You: 添加一个 330 欧姆电阻 R1
You: 添加一个红色 LED D1
You: 将 R1 的 2 脚连接到 D1 的 1 脚
You: 运行直流仿真
```

数据验证：

```bash
ls -lt data/projects | head -n 3
cat data/projects/led_verify.json
```

通过标准：
- 项目文件存在
- JSON 中有 `components` 与 `connections`

### 测试 2: HimaQA 提交流程

对话示例：

```text
You: 导出 led_verify 为 spice 网表到 ./data/results/led_verify.sp
You: 上传该网表并通知张经理测试
```

数据验证：

```bash
ls -lt data/results | head -n 5
```

通过标准：
- 有新的结果记录文件
- Agent 返回上传/通知成功信息

---

## Session 历史验证

当前 `master_main.py` 会把会话保存到：

- `data/sessions/<session_id>.json`

### 1. 检查新会话文件

```bash
ls -lt data/sessions | head -n 5
```

### 2. 检查 SDK 标准字段

```bash
latest=$(ls -t data/sessions/*.json | head -n 1)
echo "$latest"
python - <<'PY'
import json,glob
p=sorted(glob.glob('data/sessions/*.json'))[-1]
d=json.load(open(p))
print('format=', d.get('format'))
print('session_id=', d.get('session_id'))
print('events=', len(d.get('events',[])))
print('first_event_class=', d.get('events',[{}])[0].get('message_class'))
print('has_result_usage=', any(e.get('message_class')=='ResultMessage' and isinstance(e.get('data',{}),dict) and 'usage' in e.get('data',{}) for e in d.get('events',[])))
PY
```

通过标准：
- `format` 为 `claude-agent-sdk-session-v1`
- 存在 `session_id`
- `events` 非空
- 至少一个 `ResultMessage` 含 `usage` 字段

---

## 故障排除

### 问题 1: `Control request timeout: initialize`

原因：常见于本地用户级 Claude 设置与 SDK/MCP 组合冲突。

处理：
- 当前代码已固定 `setting_sources=["project"]`，请使用最新版 `master_main.py`
- 确认你启动的是当前目录代码：

```bash
pwd
python -c "import os;print(os.path.abspath('master_main.py'))"
```

### 问题 2: 终端里输入中文后出现 `command not found`

原因：你已退出 Agent 程序，输入被 shell 当命令执行。

处理：
- 先重新运行 `python master_main.py`
- 看到 `You:` 再输入自然语言

### 问题 3: 仍反复出现授权提示

处理：
- 检查 `.claude/settings.local.json` 中包含：
  - `mcp__eda-tools__*`
  - `mcp__himaqa-tools__*`
- 重启 Agent 进程

### 问题 4: 没有 session 文件

处理：
- 确认 `SESSION_DIR`（默认 `data/sessions`）
- 确认进程有写权限
- 至少完成一轮问答（含一条用户输入）后再检查目录

---

## 回归脚本

保存为 `test_agent.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[1/5] 环境检查"
python check_sdk_setup.py > /tmp/check_sdk_setup.log

echo "[2/5] 语法检查"
python -m py_compile master_main.py

echo "[3/5] 非交互启动冒烟"
printf '你好\nquit\n' | python master_main.py > /tmp/master_main_smoke.log || true

echo "[4/5] session 文件检查"
latest=$(ls -t data/sessions/*.json | head -n 1)
[ -n "$latest" ]
echo "latest session: $latest"

echo "[5/5] session 字段检查"
python - <<'PY'
import json,glob
p=sorted(glob.glob('data/sessions/*.json'))[-1]
d=json.load(open(p))
assert d.get('format')=='claude-agent-sdk-session-v1'
assert d.get('session_id')
assert len(d.get('events',[]))>0
print('session schema ok')
PY

echo "All checks passed"
```

运行：

```bash
chmod +x test_agent.sh
./test_agent.sh
```

---

## 验证通过标准

以下项全部满足即通过：

- `check_sdk_setup.py` 全部通过
- Agent 可启动并显示 `You:` / `Agent:`
- MCP 工具可直接调用，不反复卡授权
- `data/projects`、`data/results` 有新增记录
- `data/sessions/<session_id>.json` 存在且包含 SDK 标准事件字段
