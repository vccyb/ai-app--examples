# EDA智能体系统 - MVP设计文档（最小可行模型）

## 设计原则

**核心思想**：先做好最小可行模型，定义清楚Agent的职责和边界，实现一个可运行的简单系统。

### 不要做什么（留到后期）
- ❌ 复杂的状态持久化和断点续传（后期真实EDA仿真才需要）
- ❌ 复杂的参数空间和影响估算（后期真实工具才需要）
- ❌ LLM解析的安全边界验证（后期才需要）
- ❌ 颗细的WebSocket粒度控制（后期才需要）
- ❌ 多指标综合评判的Pareto最优（先用简单的逻辑）

---

## 核心Agent设计（5个）

### Agent架构图

```
┌─────────────────────────────────────────────┐
│                   用户输入                   │
│                  "优化时序<10ns"               │
└────────────────────┬──────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│            Master Agent（主控Agent）          │
│  职责：接收指令 → 分派任务 → 聚合结果  │
└──────┬──────────────────┬────────────┘
         ↓         ↓           ↓           ↓
    ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌───────────┐
    │RAG Agent  │ │EDA Agent  │ │Evaluation │ │General    │
    │知识查询    │ │工具执行   │ │Agent     │ │Agent     │
    └──────────┘ └──────────┘ │(评判）    │ │数据保存   │
                                       └──────────┘ └───────────┘
```

---

## 1. Master Agent（主控Agent）

### 职责定义
> **接收用户的自然语言指令，理解要做什么，然后分派给合适的子Agent，最后把结果聚合返回给用户。**

### 边界
- ✅ **可以做的**：
  - 解析用户指令（如"优化时序"）
  - 决定调用哪个子Agent
  - 把子Agent的结果整理成用户可读的文字

- ❌ **不做的**：
  - 不执行具体的EDA操作
  - 不理解复杂的EDA专业知识（靠子Agent）
  - 不处理状态持久化和恢复（后期再加）

### 输入输出
```python
# 输入
user_input: str  # "优化模块A的时序，目标<10ns"

# 输出（返回给用户）
result: str  # "时序12ns，未达目标10ns。建议降低时钟频率。"

# 内部调用（分派给子Agent）
→ RAG_Agent.query("模块A的设计规范")
→ EDA_Agent.run_simulation("模块A")
→ Evaluation_Agent.compare(target="10ns", actual="12ns")
→ General_Agent.save("模块A", {"timing": "12ns"})
```

### 核心方法（伪代码）
```python
class MasterAgent:
    def process(user_input: str) -> str:
        # 1. 理解用户意图
        intent = self.parse_intent(user_input)

        # 2. 分派任务
        if intent.type == "optimize":
            spec = rag_agent.query(intent.module)
            result = eda_agent.run(intent.module)
            evaluation = evaluator.compare(intent.target, result)
            general_agent.save(result)

            # 3. 聚合结果
            return f"当前{result.metrics.timing}，{evaluation.reason}。"
```

---

## 2. RAG Agent（知识查询Agent）

### 职责定义
> **提供知识查询接口，当前用简单的Mock数据，未来对接真实知识平台。**

### 边界
- ✅ **可以做的**：
  - 保存10条固定的知识数据
  - 根据查询词返回匹配的知识
  - 提供`query(keywords)`接口

- ❌ **不做的**：
  - 不实现真实向量检索（后期对接真实API）
  - 不缓存和历史记录（MVP阶段）
  - 不处理复杂的语义理解

### Mock数据示例（10条）
```python
# 固定知识库（key -> value）
KNOWLEDGE_BASE = {
    # 时序相关
    "时序优化": "降低时钟频率可以减少传播延迟，但可能影响吞吐量",
    "关键路径": "时序主要受组合逻辑深度和时钟频率影响",
    "100MHz": "典型时钟频率，时序约10ns",
    "80MHz": "降低频率后，时序可改善至8-9ns",

    # 功耗相关
    "功耗优化": "降低供电电压和时钟频率可减少动态功耗",
    "低功耗": "功耗<50mW为低功耗设计",

    # 面积相关
    "面积预算": "芯片面积直接影响成本，需控制在预算内",

    # 通用
    "默认": "根据最佳实践选择参数"
}

# 查询接口
def query(keywords: list[str]) -> str:
    # 简单匹配
    for key in KNOWLEDGE_BASE:
        if any(keyword in key for keyword in keywords):
            return KNOWLEDGE_BASE[key]
    return "未找到相关知识"
```

### 核心方法
```python
class RAGAgent:
    def query(self, keywords: list[str]) -> str:
        """查询知识，返回匹配的条目"""
        return self._mock_search(keywords)
```

---

## 3. EDA Agent（工具执行Agent）

### 职责定义
> **执行EDA工具（当前Mock），返回仿真结果数据。**

### 边界
- ✅ **可以做的**：
  - 提供`run_simulation(module)`接口
  - 返回固定的仿真结果（可以随机变化一点）
  - 提供工具状态查询

- ❌ **不做的**：
  - 不实现真实工具调用（后期加真实工具）
  - 不处理参数调整（只返回固定结果）
  - 不处理工具错误和重试（MVP阶段）

### Mock结果格式
```python
# 固定返回结果（可以根据输入略有变化）
def mock_run(module: str) -> dict:
    import random

    # 模拟：不同模块有不同基准性能
    base_results = {
        "模块A": {"timing": "12ns", "power": "50mW", "area": "1000um²"},
        "模块B": {"timing": "8ns", "power": "70mW", "area": "1200um²"},
        "模块C": {"timing": "15ns", "power": "40mW", "area": "800um²"}
    }

    result = base_results.get(module, base_results["模块A"])

    # 加一点随机变化（±5%），模拟"优化效果"
    variation = random.uniform(0.95, 1.05)

    return {
        "timing": f"{float(result['timing']) * variation:.1f}ns",
        "power": f"{float(result['power'][:-2]) * variation:.1f}mW",
        "area": result["area"]
    }
```

### 核心方法
```python
class EDAAgent:
    def run_simulation(self, module: str) -> dict:
        """运行仿真，返回结果"""
        return self._mock_run(module)
```

---

## 4. Evaluation Agent（评判Agent）

### 职责定义
> **对比用户目标和仿真结果，给出是否达标的判断和建议。**

### 边界
- ✅ **可以做的**：
  - 对比两个数值（如10ns vs 12ns）
  - 给出PASS/FAIL判断
  - 生成简单建议文本
  - 处理单个指标评判

- ❌ **不做的**：
  - 不处理多指标综合（MVP阶段只评判单个指标）
  - 不实现复杂的建议生成（用固定模板）
  - 不估算参数影响（后期再加）

### 评判逻辑（最简单）
```python
def evaluate(target: str, actual: str) -> dict:
    """最简单的对比逻辑"""
    # 1. 提取数字
    target_value = float(target[:-2])  # "10ns" -> 10
    actual_value = float(actual[:-2])  # "12ns" -> 12

    # 2. 对比判断
    passed = actual_value < target_value

    # 3. 生成结果
    return {
        "status": "PASS" if passed else "FAIL",
        "target": target,
        "actual": actual,
        "reason": f"实际{actual_value}{'未达标' if not passed else '达标'}",
        "suggestion": _generate_simple_suggestion(target_value, actual_value) if not passed else None
    }

def _generate_simple_suggestion(target: float, actual: float) -> str:
    """生成固定建议"""
    gap = actual - target
    gap_ratio = gap / target

    if gap_ratio > 0.2:  # 差距>20%
        return f"差距较大({gap_ratio:.1%})，建议检查参数或工具配置"
    else:  # 差距<20%
        return f"接近目标，微调参数可能达标（差距{gap:.1f}）"
```

### 核心方法
```python
class EvaluationAgent:
    def evaluate(self, target: str, actual: dict) -> dict:
        """评判单个指标"""
        actual_value = actual.get("timing")
        return self._compare(target, actual_value)
```

---

## 5. General Agent（通用Agent）

### 职责定义
> **负责数据保存和查询，当前只做内存存储。**

### 边界
- ✅ **可以做的**：
  - 提供`save(data)`和`query(filters)`接口
  - 用Python字典存储数据
  - 简单的历史查询

- ❌ **不做的**：
  - 不实现真实数据库（MVP阶段用内存）
  - 不处理复杂查询条件
  - 不做数据导入导出

### 内存存储示例
```python
# 简单的内存存储
DATABASE = {
    "tasks": [],  # 任务列表
    "results": [],  # 仿真结果列表
    "evaluations": []  # 评判历史列表
}

def save(data: dict) -> str:
    """保存数据到内存"""
    DATABASE["tasks"].append(data)
    return f"已保存，ID: {len(DATABASE['tasks'])}"

def query(filters: dict = None) -> list[dict]:
    """查询数据"""
    if filters:
        return [item for item in DATABASE["tasks"] if item.get("module") == filters.get("module")]
    return DATABASE["tasks"]
```

### 核心方法
```python
class GeneralAgent:
    def save(self, data: dict) -> str:
        """保存数据"""
        self.database["tasks"].append(data)
        return f"已保存，ID: {len(self.database['tasks'])}"

    def query(self, filters: dict = None) -> list:
        """查询数据"""
        if not filters:
            return self.database["tasks"]
        return [t for t in self.database["tasks"] if t.get("module") == filters.get("module")]
```

---

## 完整工作流示例

### 用户输入
```
"优化模块A的时序，目标<10ns"
```

### Agent调用链路（简化版）
```
用户 → Master Agent
     ↓
  1. 解析：action=optimize, module=A, target=10ns
     ↓
  2. 调用 RAG Agent → "模块A的设计规范"
     ↓
  3. RAG返回 → "降低时钟频率可以减少传播延迟"
     ↓
  4. 调用 EDA Agent → run_simulation("模块A")
     ↓
  5. EDA返回 → {"timing": "12ns", "power": "50mW", "area": "1000um²"}
     ↓
  6. 调用 Evaluation Agent → evaluate(target="10ns", actual={"timing": "12ns"})
     ↓
  7. Evaluation返回 → {
        "status": "FAIL",
        "reason": "实际12ns未达标10ns",
        "suggestion": "接近目标，微调参数可能达标（差距2.0ns）"
     }
     ↓
  8. 调用 General Agent → save({"module": "A", "result": {...}})
     ↓
  9. 返回用户 → "当前时序12ns，未达目标10ns。接近目标，微调参数可能达标（差距2.0ns）。已保存到数据库。"
```

---

## 项目结构（最小版）

```
eda-agent/
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI入口（最简单：一个/execute端点）
│   │
│   ├── agents/                    # Agent实现
│   │   ├── __init__.py
│   │   ├── master_agent.py         # 主控Agent
│   │   ├── rag_agent.py            # RAG Agent（10条Mock数据）
│   │   ├── eda_agent.py            # EDA Agent（Mock仿真）
│   │   ├── evaluation_agent.py    # 评判Agent（简单对比）
│   │   └── general_agent.py        # 通用Agent（内存存储）
│   │
│   └── models/                    # 简单的数据模型
│       ├── __init__.py
│       ├── message.py              # 消息格式
│       └── task.py                 # 任务模型
│
├── tests/                         # 测试
│   ├── __init__.py
│   └── test_agents.py            # 简单的Agent测试
│
├── requirements.txt                 # 依赖列表
└── README.md                       # 项目说明
```

---

## 技术栈（MVP版本）

| 组件 | 技术 | 说明 |
|------|------|------|
| 语言 | **Python 3.11+** | 基础设施 |
| Web框架 | **FastAPI** | 提供REST API |
| LLM | **Mock** | 不调用真实LLM，用规则逻辑 |
| 数据库 | **内存字典** | 不用PostgreSQL，用Python dict |
| 前端 | **curl** | 不做Vue，用命令行测试 |

**依赖（requirements.txt）**：
```
fastapi
uvicorn[standard]
pydantic
```

---

## API接口（最简单）

### POST /api/execute
执行用户指令的单一端点。

**请求**：
```json
{
  "user_input": "优化模块A的时序，目标<10ns"
}
```

**响应**：
```json
{
  "status": "success",
  "result": "当前时序12ns，未达目标10ns。接近目标，微调参数可能达标（差距2.0ns）。已保存到数据库。",
  "trace": [
    "RAG查询：模块A的设计规范",
    "EDA仿真：模块A -> 时序12ns",
    "评判：FAIL（12ns > 10ns）",
    "数据保存：ID=1"
  ]
}
```

---

## 实现优先级（MVP阶段）

### 第1步：基础框架（半天）
- [ ] 创建项目目录结构
- [ ] 配置requirements.txt
- [ ] 实现FastAPI的单一端点`/api/execute`
- [ ] 测试：`curl -X POST http://localhost:8000/api/execute -d {...}`

### 第2步：5个Agent基础实现（1-2天）
- [ ] Master Agent：简单的意图解析和分派逻辑
- [ ] RAG Agent：10条固定Mock数据，关键词匹配
- [ ] EDA Agent：固定Mock结果（可以加随机变化）
- [ ] Evaluation Agent：数值对比，返回PASS/FAIL
- [ ] General Agent：内存字典存储

### 第3步：端到端测试（半天）
- [ ] 完整工作流测试：输入"优化时序"→ 完整输出
- [ ] 边界测试：各种奇怪的输入是否报错
- [ ] 文档化：更新README说明如何使用

---

## 验收标准

MVP完成的标志：
- ✅ 可以用curl发送请求，得到完整响应
- ✅ 5个Agent都有独立实现且职责清晰
- ✅ RAG的10条知识可以查询到
- ✅ Evaluation可以正确判断PASS/FAIL
- ✅ 整个流程跑通：用户输入 → Master分派 → 子Agent执行 → 结果返回
- ✅ 代码结构清晰，容易理解

**不做的事情**（明确排除）：
- ❌ 不需要PostgreSQL数据库
- ❌ 不需要真实LLM调用
- ❌ 不需要Vue前端界面
- ❌ 不需要复杂的状态管理
- ❌ 不需要WebSocket实时更新

---

## 为什么要先做MVP

1. **快速验证核心概念**：Agent协作是否可行？
2. **降低复杂度**：不被非EDA细节（状态管理、断点续传）分散注意力
3. **清晰的职责边界**：每个Agent做什么和不做什么非常清楚
4. **易于调试**：所有逻辑都在内存中，错误容易定位
5. **可扩展基础**：MVP跑通后，再加真实数据库、真实LLM等

---

`★ Insight ─────────────────────────────────────`
**MVP（最小可行产品）的价值**：这个设计完全剥离了EDA领域的复杂度，聚焦在"Agent协作模式"本身的验证上。RAG只用10条Mock数据、EDA只用固定结果、Evaluation只用简单对比，这些都非常容易理解和调试。等这个MVP能跑通，我们就能确信"多个Agent协作"这个核心模式是可行的，然后逐步加真实工具、真实数据、复杂逻辑。
`─────────────────────────────────────────────────`
