# Master Agent 用户手册

## 快速开始

```bash
cd /Users/chenyubo/Project/ai-project/agents/v1
source .venv/bin/activate
python check_sdk_setup.py
python master_main.py
```

启动后你会看到：
- `✓ Agent 已启动`
- `You:` 输入提示

退出命令：
- `quit`
- `exit`
- `/quit`
- `/exit`

---

## 使用方式

### 1. EDA 设计

示例：

```text
You: 创建项目 led_demo
You: 添加一个 330 欧姆电阻 R1
You: 添加一个红色 LED D1
You: 将 R1 的 2 脚连接到 D1 的 1 脚
You: 运行直流仿真
You: 导出 led_demo 的 spice 网表
```

### 2. HimaQA 提测

```text
You: 上传 led_demo 网表到 HimaQA
You: 通知张经理测试
You: 查询 led_demo 历史记录
```

### 3. 端到端

```text
You: 设计一个 LED 电路并提交给张经理测试
```

---

## 当前权限策略（重要）

为了避免 Agent 绕路执行无关命令，当前代码中：

允许：
- `Skill`
- `Read`
- `mcp__eda-tools__*`
- `mcp__himaqa-tools__*`

禁止：
- `Bash`
- `Write`
- `Edit`
- `AskUserQuestion`

如果你看到 Agent 试图走 Bash/Write，通常是运行了旧代码或旧会话。

---

## 会话与数据保存

### 会话历史
每次对话会自动保存到：
- `data/sessions/<session_id>.json`

文件内容以 SDK 标准消息结构为主（`SystemMessage/AssistantMessage/ResultMessage`）。

### 业务数据
- 项目：`data/projects/*.json`
- 工具结果：`data/results/*.json`

---

## 常见问题

### Q1: 为什么会提示 `command not found`？
你已经退出了 Agent 程序，输入被 shell 当命令执行。

处理：重新运行 `python master_main.py`，看到 `You:` 再输入。

### Q2: 为什么出现 `Control request timeout: initialize`？
常见原因是用户级配置干扰。当前代码已固定：
- `setting_sources=["project"]`

请确保使用最新 `master_main.py`。

### Q3: 为什么工具调用看起来执行了但没生效？
请确认你使用的是最新 `tools/sdk_tools.py`（已修复 async await 与参数映射）。

---

## 推荐验证

详细验证步骤见：
- `doc/VERIFY_GUIDE.md`

最短验证：

```bash
python check_sdk_setup.py
python master_main.py
```
