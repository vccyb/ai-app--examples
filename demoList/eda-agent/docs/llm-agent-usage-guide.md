# EDA Agent 系统 - 新一代使用指南

## 概述

这是基于 LLM 驱动的新一代 EDA Agent 系统，相比旧版本的主要变化：

### 核心变化

| 特性 | 旧版本 | 新版本 |
|-----|-------|-------|
| **驱动方式** | 硬编码规则 | LLM 自动判断 |
| **对话模式** | 单次输入 | 多轮对话 |
| **Agent 调用** | Master Agent 分派 | AI 自动选择工具 |
| **扩展性** | 需要修改代码 | 只需添加新工具 |
| **灵活性** | 固定输入格式 | 自然语言理解 |

### 架构对比

**旧版本架构**：
```
用户输入 → Master Agent (硬编码解析)
         → RAG/EDA/Evaluation/General Agent (固定调用)
         → 结果返回
```

**新版本架构**：
```
用户多轮对话 → ConversationManager
           → LLM 判断是否需要调用工具
           → 自动选择合适的 Tool
           → 执行并返回结果
           → 继续对话
```

## 快速开始

### 1. 使用 Mock 模式（默认）

```bash
# 运行交互式 CLI
python3 cli_new.py

# 或明确指定
python3 cli_new.py --llm mock
```

**示例对话**：
```
你：查询模块A的设计规范
助手：我来帮您查询模块A的设计规范。
[工具调用] query_knowledge
参数: {"module": "模块A"}
[工具结果] {
  "knowledge": "已获取模块A的设计规范",
  "specification": {
    "timing": {"max_clock": "100MHz", "typical_timing": "10ns"},
    "power": {"max": "100mW"},
    "area": {"max": "1000um²"}
  },
  "sources": ["RAG知识库"]
}
助手：根据查询结果，模块A的设计规范如下：
- 时序：最大时钟100MHz，典型时序10ns
- 功耗：最大100mW
- 面积：最大1000um²
```

### 2. 接入真实 LLM（可选）

```bash
# 使用 Claude
export ANTHROPIC_API_KEY="your-api-key"
python3 cli_new.py --llm claude

# 使用 Qwen
export DASHSCOPE_API_KEY="your-api-key"
python3 cli_new.py --llm qwen
```

## 可用工具

### 1. query_knowledge - 查询设计规范

**用途**：查询模块的设计规范、时序要求、功耗限制等

**对话示例**：
- "查询模块A的设计规范"
- "模块B的时序要求是什么？"
- "告诉我模块C的功耗和面积限制"

**参数**：
```json
{
  "module": "模块A",
  "keywords": ["时序", "优化"]  // 可选
}
```

### 2. run_simulation - 运行仿真

**用途**：执行 EDA 仿真，获取实际性能指标

**对话示例**：
- "运行模块A的仿真"
- "仿真模块B"
- "测试一下模块C"

**参数**：
```json
{
  "module": "模块A",
  "parameters": {  // 可选
    "voltage": "0.9V"
  }
}
```

### 3. evaluate_result - 评判结果

**用途**：对比实际结果与目标，判断是否达标

**对话示例**：
- "评判时序12ns是否达到目标10ns"
- "评估功耗55mW是否满足小于50mW的要求"
- "对比一下实际结果和目标"

**参数**：
```json
{
  "goal": {
    "metric": "timing",
    "operator": "<",
    "value": "10ns"
  },
  "actual": {
    "timing": "12ns",
    "power": "50mW"
  }
}
```

### 4. save_result - 保存结果

**用途**：保存仿真结果、评判结果等到数据库

**对话示例**：
- "保存这个结果"
- "把这些数据存起来"

**参数**：
```json
{
  "data": {
    "task": "优化模块A时序",
    "module": "模块A"
  },
  "data_type": "task"  // task/simulation/evaluation
}
```

### 5. query_history - 查询历史

**用途**：查看之前的仿真结果、评判历史

**对话示例**：
- "查看模块A的历史记录"
- "显示之前的所有仿真结果"
- "我之前做过哪些优化？"

**参数**：
```json
{
  "filters": {
    "module": "模块A"
  }
}
```

### 6. optimize_design - 完整优化流程（高级）

**用途**：自动完成查询、仿真、评判、保存的完整流程

**对话示例**：
- "优化模块A的时序，目标小于10ns"
- "改进模块B的功耗，要控制在50mW以内"
- "优化模块C"

**参数**：
```json
{
  "module": "模块A",
  "target": {
    "metric": "timing",
    "operator": "<",
    "value": "10ns"
  }
}
```

## 对话场景示例

### 场景1：首次优化设计

```
你：优化模块A的时序，目标小于10ns

助手：我来帮您优化模块A的时序。让我先查询设计规范，然后运行仿真。
[工具调用] optimize_design
参数: {
  "module": "模块A",
  "target": {
    "metric": "timing",
    "operator": "<",
    "value": "10ns"
  }
}

[工具结果] {
  "status": "completed",
  "module": "模块A",
  "specification": {...},
  "simulation": {
    "timing": "11.7ns",
    "power": "48.6mW",
    "area": "1000um²"
  },
  "evaluation": {
    "status": "FAIL",
    "reason": "实际11.7ns未达目标10ns，差距+17.0%",
    "suggestion": "接近目标，微调参数可能达标（差距2.0ns）"
  }
}

助手：优化完成！结果如下：
仿真结果：时序 11.7ns，功耗 48.6mW，面积 1000um²
评判结果：未达标 ❌
- 实际时序 11.7ns 未达到目标 10ns
- 差距：+2.0ns (+17.0%)

建议：接近目标，微调参数可能达标（差距 2.0ns）
```

### 场景2：查看历史再优化

```
你：查看模块A的历史记录

助手：我来帮您查询模块A的历史记录。
[工具调用] query_history
参数: {"filters": {"module": "模块A"}}

[工具结果] {
  "count": 3,
  "records": [...]
}

助手：模块A 共有 3 条记录：
1. 任务：优化模块A时序
2. 仿真：时序 11.7ns
3. 评判：未达标

你：再优化一次，这次降低一点时钟频率

助手：好的，我来重新运行仿真，调整时钟频率。
[工具调用] run_simulation
参数: {"module": "模块A", "parameters": {"clock_freq": "80MHz"}}

...
```

### 场景3：多轮对话

```
你：你好

助手：你好！我是 EDA 设计助手，有什么可以帮您的吗？

你：你能做什么？

助手：我可以帮您完成 EDA 设计任务：
- 查询模块的设计规范（时序、功耗、面积要求）
- 运行仿真测试，获取实际性能指标
- 评判结果是否达标，并提供优化建议
- 保存和查询历史记录
- 执行完整的优化流程

您想从哪里开始？

你：查询模块B的功耗要求

助手：[执行查询...]
根据设计规范，模块B的功耗最大 80mW。

你：如果仿真结果是70mW，算达标吗？

助手：[执行评判...]
是的，70mW 小于 80mW 的目标，达标了！
```

## 技术架构

### 文件结构

```
eda-agent/
├── src/
│   ├── llm_client.py              # LLM 客户端抽象层
│   ├── eda_tools.py                # 工具定义和实现
│   ├── conversation_manager.py   # 会话管理器
│   └── agents/                    # 原有 Agent（保留兼容）
│       ├── rag_agent.py
│       ├── eda_agent.py
│       ├── evaluation_agent.py
│       ├── general_agent.py
│       └── master_agent.py
├── cli_new.py                        # 新一代 CLI
├── cli.py                            # 旧版 CLI（保留）
└── test_workflow.py           # 旧版测试（保留）
```

### 核心组件

#### 1. LLMClient (llm_client.py)

统一的 LLM 客户端接口，支持：
- **MockLLMClient** - 模拟 LLM，用于开发测试
- **ClaudeLLMClient** - Claude API
- **QwenLLMClient** - 阿里云 Qwen API

特点：
- 工厂模式，易于扩展新的 LLM 提供商
- 统一的 API 接口
- 自动工具调用检测（Mock 模式）

#### 2. ConversationManager (conversation_manager.py)

会话管理器，负责：
- 管理消息历史
- 调用 LLM 获取响应
- 自动执行工具调用
- 多轮对话循环

特点：
- 自动检测工具调用
- 工具结果自动反馈给 LLM
- 支持多轮对话直到完成

#### 3. EDA Tools (eda_tools.py)

将原有 Agent 转换为 Claude Tool 格式：
- `query_knowledge` - 查询工具
- `run_simulation` - 仿真工具
- `evaluate_result` - 评判工具
- `save_result` - 保存工具
- `query_history` - 查询工具
- `optimize_design` - 复合工具

特点：
- 保留原有 Agent 实现
- 添加 Claude Tool Schema 定义
- 统一的工具执行接口

## 开发指南

### 添加新工具

1. **在 `eda_tools.py` 中添加工具函数**：
```python
def my_new_tool(param1: str, param2: int) -> Dict:
    """工具实现"""
    # 调用原有 Agent 或实现新逻辑
    return {"result": "..."}
```

2. **定义 Tool Schema**：
```python
my_new_tool_schema = ToolParam(
    name="my_new_tool",
    description="工具描述，告诉 AI 何时使用此工具",
    input_schema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."},
            "param2": {"type": "integer", "description": "..."}
        },
        "required": ["param1"]
    }
)
```

3. **注册工具**：
```python
def get_tool_schemas() -> list:
    return [
        # ... 其他工具
        my_new_tool_schema,
    ]
```

4. **在工具映射中添加**：
```python
def run_tool(tool_name: str, tool_input: Dict) -> Any:
    tools_map = {
        # ... 其他工具
        "my_new_tool": my_new_tool,
    }
    # ...
```

### 集成真实 LLM

#### 使用 Claude

```python
from src.llm_client import create_llm_client
from src.conversation_manager import ConversationManager

# 创建 Claude 客户端
conv = ConversationManager(
    llm_client_type="claude",
    api_key="your-anthropic-api-key"
)

# 运行对话
conv.add_user_message("优化模块A时序，目标小于10ns")
conv.run_conversation()
```

#### 使用 Qwen

```python
# 类似方式，只需改变类型
conv = ConversationManager(
    llm_client_type="qwen",
    api_key="your-dashscope-api-key"
)
```

## 常见问题

### Q: 为什么 Mock 模式下也能自动调用工具？

A: MockLLMClient 实现了简单的关键词匹配逻辑，模拟 LLM 的工具调用判断。虽然是 Mock，但可以验证整个工作流程。

### Q: 如何查看 LLM 实际调用了什么工具？

A: 在对话过程中，系统会显示：
```
[工具调用] query_knowledge
参数: {"module": "模块A"}
```

### Q: 工具调用失败了怎么办？

A: 系统会捕获错误并反馈给 LLM，LLM 会自动决定是否重试或使用其他方法。

### Q: 如何清空对话重新开始？

A: 输入 `清空` 或 `clear` 命令。

### Q: 旧版 CLI 还能用吗？

A: 可以。旧版 `cli.py` 和新版 `cli_new.py` 共存，互不影响。

## 下一步

1. **尝试使用**：
   ```bash
   python3 cli_new.py
   ```

2. **接入真实 LLM**：
   - 获取 API Key
   - 运行 `--llm claude` 或 `--llm qwen`

3. **添加自定义工具**：
   - 参考开发指南
   - 扩展系统能力

`★ Insight ─────────────────────────────────────`
**新版本的核心价值**：通过 LLM 自动判断调用哪个工具，系统变得更加智能和灵活。用户不再需要记住固定的命令格式，可以用自然语言描述需求。而且添加新工具非常简单 - 只需定义工具和 Schema，LLM 会自动学习何时使用它。这为未来接入更多 EDA 工具（Vivado、Design Compiler 等）打下了基础。
`─────────────────────────────────────────────────
