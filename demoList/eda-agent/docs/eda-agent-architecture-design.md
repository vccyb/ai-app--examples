# EDA智能体系统实现计划

## 项目概述

构建一个面向EDA（电子设计自动化）场景的智能体系统，通过多Agent协作帮助工程师完成芯片设计任务。

**核心特点**：
- 中心化编排：主控Agent作为中央协调器
- 4类子Agent：EDA工具交互、RAG知识查询、通用数据处理、核心评判
- 对比型评判：基于用户目标指标，对比EDA结果，生成调整建议

---

## 技术栈

### 核心技术
| 组件 | 技术选型 | 理由 |
|------|---------|------|
| Agent框架 | **LangGraph** | 专为有状态多Agent协作设计，完美适配中心化编排 |
| 编程语言 | **Python 3.11+** | EDA工具Python API成熟，AI生态丰富 |
| LLM模型 | **Qwen-Max / Qwen-Plus** | 符合现有技术栈，中文支持优秀 |
| 数据库 | **PostgreSQL + pgvector** | 关系型数据可靠，支持向量检索 |
| Web框架 | **FastAPI** | 原生异步，自动API文档 |
| 前端 | **Vue 3 + Element Plus** | 与现有项目保持一致 |

---

## 系统架构

### 分层架构
```
Presentation Layer (Vue 3 / CLI)
        ↓
Agent Layer (LangGraph)
├── Master Agent (中央协调器)
├── EDA Tool Agent (工具交互)
├── RAG Agent (知识查询)
├── Evaluation Agent (核心评判)
└── General Agent (数据处理)
        ↓
Service Layer
├── EDA Tool Service (策略模式)
├── Knowledge Platform API (外部接口)
├── Database Service (PostgreSQL)
└── File Storage
```

### Agent协作流程（示例：优化时序）

```
用户："优化模块A时序，目标<10ns"
    ↓
1. Master Agent 解析任务 → {action: optimize, metric: timing, target: <10ns}
    ↓
2. RAG Agent 查询设计规范 → {max_clock: 100MHz, setup_time: 2ns}
    ↓
3. EDA Tool Agent 执行仿真 → {timing: 12ns, power: 50mW}
    ↓
4. Evaluation Agent 对比评判
   ├─ 查询RAG理解指标含义
   ├─ 对比：12ns > 10ns → FAILED
   ├─ 查询历史和最佳实践
   └─ 生成建议："降低时钟频率至80MHz"
    ↓
5. Master Agent 决策：未达标，需迭代
    ↓
6. 用户确认继续
    ↓
7. EDA Tool Agent 重新仿真(80MHz) → {timing: 9.5ns}
    ↓
8. Evaluation Agent 再次评判 → PASSED ✅
    ↓
9. General Agent 保存结果
    ↓
10. 返回用户："时序优化成功！当前9.5ns (目标<10ns)"
```

---

## 各Agent详细设计

### 1. Master Agent（主控Agent）

**职责**：
- 解析用户自然语言指令
- 任务分解与工作流编排
- 分派任务给子Agent
- 协调数据传递
- 决策是否继续迭代

**关键方法**：
```python
async def process_user_query(query: str) -> str:
    """主入口：处理用户查询"""

def parse_task(query: str) -> dict:
    """使用LLM解析为结构化任务"""

async def orchestrate_workflow(parsed_goal: dict) -> dict:
    """使用LangGraph编排工作流"""

def should_continue(state: EDATaskState) -> str:
    """迭代决策：继续/保存/失败"""
```

**输出示例**：
```json
{
  "task_id": "sim_20250112_001",
  "status": "completed",
  "iterations": 2,
  "final_result": {"timing": "9.5ns", "power": "45mW"},
  "evaluation": {"status": "PASSED", "reason": "时序9.5ns满足目标10ns"}
}
```

---

### 2. EDA Tool Agent（EDA工具交互Agent）

**职责**：
- 抽象不同EDA工具接口
- 执行仿真、获取参数
- 解析工具输出，提取指标
- 处理仿真错误

**工具策略接口**：
```python
class EDAToolStrategy(ABC):
    @abstractmethod
    async def run_simulation(params: dict) -> str:
        """启动仿真，返回任务ID"""

    @abstractmethod
    async def get_status(task_id: str) -> str:
        """获取任务状态"""

    @abstractmethod
    async def get_result(task_id: str) -> dict:
        """获取仿真结果"""
```

**当前实现**：MockEDATool（模拟2秒返回结果）
**未来扩展**：VivadoTool、DesignCompilerTool

**输出格式**：
```json
{
  "tool_name": "mock",
  "status": "SUCCESS",
  "metrics": {
    "timing": "12ns",
    "power": "50mW",
    "area": "1000um²"
  },
  "execution_time": 2.5
}
```

---

### 3. RAG Agent（RAG知识查询Agent）

**职责**：
- 调用外部知识平台API
- 查询设计规范、经验规则
- 获取指标解释和评价标准
- 缓存常用查询

**关键方法**：
```python
async def query_knowledge(query: str, knowledge_type: str) -> KnowledgeResult:
    """查询外部知识平台"""

async def get_specification(module: str) -> dict:
    """获取模块设计规范"""

async def explain_metric(metric_name: str) -> dict:
    """解释指标含义"""
```

**输出格式**：
```json
{
  "sources": [
    {"title": "时序优化指南", "relevance": 0.95}
  ],
  "answer": "关键路径优化需要关注时钟频率和逻辑深度...",
  "structured_spec": {
    "timing": {"max_clock": "100MHz"},
    "power": {"max": "100mW"}
  }
}
```

---

### 4. Evaluation Agent（评判Agent - 核心）

**职责**：
- 接收用户目标和EDA结果
- 查询RAG理解指标
- 对比结果与目标
- 生成推理和建议
- 明确告知是否可达

**对比型评判流程**：
```python
async def evaluate(goal: dict, result: dict, spec: dict) -> EvaluationResult:
    """
    1. 提取指标：metric="timing", target="10ns", actual="12ns"
    2. 单位转换：10ns → 10e-9s, 12ns → 12e-9s
    3. 对比判断：12e-9s < 10e-9s → False
    4. 查询RAG：优化策略、历史案例
    5. 生成建议："降低时钟至80MHz，预期改善至9.5ns"
    6. 返回：FAILED + 建议理由
    """
```

**关键特性**：
- **单位归一化**：支持ps/ns/us/ms等自动转换
- **多指标评判**：Pareto最优，综合权衡
- **LLM增强推理**：生成详细的推理过程
- **可行性验证**：避免生成无法执行的建议

**输出格式**：
```json
{
  "status": "FAILED",
  "reason": "时序12ns超过目标10ns，超限20%",
  "comparison": {
    "target": "10ns",
    "actual": "12ns",
    "diff": "+2ns"
  },
  "suggestion": "建议降低时钟频率至80MHz，预期时序改善至9.5ns",
  "confidence": 0.85,
  "feasible": true
}
```

---

### 5. General Agent（通用处理Agent）

**职责**：
- 数据库CRUD操作
- 保存仿真结果和评判历史
- 查询历史最优结果
- 数据统计分析

**关键方法**：
```python
async def save_simulation_result(result: SimulationResult) -> str:
    """保存到PostgreSQL"""

async def query_history(filters: dict) -> list[dict]:
    """查询历史记录"""

async def get_best_result(module: str, metric: str) -> dict:
    """获取最优结果"""
```

---

## 数据库设计

### 核心表结构

```sql
-- 任务表
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_query TEXT,
    parsed_goal JSONB,
    status VARCHAR(50),
    created_at TIMESTAMP
);

-- 仿真结果表
CREATE TABLE simulation_results (
    id UUID PRIMARY KEY,
    task_id UUID REFERENCES tasks(id),
    module VARCHAR(255),
    tool_name VARCHAR(100),
    metrics JSONB,  -- {"timing": "12ns", "power": "50mW"}
    status VARCHAR(50),
    created_at TIMESTAMP
);

-- 评判历史表
CREATE TABLE evaluation_history (
    id UUID PRIMARY KEY,
    task_id UUID REFERENCES tasks(id),
    goal JSONB,
    actual_result JSONB,
    evaluation_status VARCHAR(50),
    reasoning TEXT,
    suggestion TEXT,
    created_at TIMESTAMP
);
```

---

## 项目目录结构

```
eda-agent/
├── src/
│   ├── main.py                    # FastAPI入口
│   ├── config.py                  # 配置管理
│   │
│   ├── agents/                    # Agent实现
│   │   ├── master_agent.py         # 主控Agent
│   │   ├── eda_agent.py            # EDA工具Agent
│   │   ├── rag_agent.py            # RAG Agent
│   │   ├── evaluation_agent.py    # 评判Agent（核心）
│   │   └── general_agent.py        # 通用Agent
│   │
│   ├── workflows/                 # LangGraph工作流
│   │   └── optimization_workflow.py # 优化工作流图
│   │
│   ├── eda_tools/                 # EDA工具适配
│   │   ├── base.py                # 策略接口
│   │   ├── mock_tool.py           # Mock工具
│   │   ├── vivado_tool.py         # Vivado适配（预留）
│   │   └── dc_tool.py             # DC适配（预留）
│   │
│   ├── models/                    # 数据模型
│   │   ├── message.py              # 消息格式
│   │   ├── task.py                 # 任务模型
│   │   └── evaluation.py           # 评判模型
│   │
│   ├── database/                  # 数据库
│   │   ├── connection.py           # DB连接
│   │   ├── models.py               # ORM模型
│   │   └── repositories.py         # 数据访问层
│   │
│   ├── api/                       # FastAPI路由
│   │   └── routes.py               # API端点
│   │
│   └── services/                  # 业务服务
│       ├── task_service.py          # 任务管理
│       └── llm_service.py           # LLM调用封装
│
├── frontend/                       # Vue 3前端
│   └── src/
│       ├── components/              # 组件
│       ├── api/                    # API客户端
│       └── App.vue
│
├── tests/                         # 测试
│   ├── unit/                     # 单元测试
│   └── integration/              # 集成测试
│
├── scripts/                        # 脚本工具
│   ├── init_db.py                # 初始化数据库
│   └── seed_data.py              # 种子数据
│
├── pyproject.toml                  # Poetry依赖
├── docker-compose.yml              # 开发环境
└── README.md
```

---

## 实现里程碑

### 阶段1：核心框架（1-2周）
- [ ] 项目初始化（Poetry、FastAPI、目录结构）
- [ ] 数据库搭建（PostgreSQL + SQLAlchemy模型）
- [ ] LLM集成（Qwen模型调用封装）
- [ ] 基础API路由（/health, /api/tasks）

**验收**：
```bash
curl http://localhost:8000/health  # {"status": "ok"}
```

---

### 阶段2：基础Agent（2-3周）
- [ ] EDA Tool Agent（Mock工具实现）
- [ ] RAG Agent（API封装 + Mock响应）
- [ ] Evaluation Agent（对比型评判逻辑）
- [ ] General Agent（数据库CRUD）
- [ ] 单元测试（覆盖率>80%）

**验收**：
```bash
pytest tests/unit/ -v --cov
```

---

### 阶段3：主控和工作流（2-3周）
- [ ] Master Agent（任务解析 + 编排）
- [ ] LangGraph工作流定义（状态图、条件边）
- [ ] 错误处理和降级策略
- [ ] 集成测试

**验收**：
```bash
curl -X POST http://localhost:8000/api/tasks/optimize \
  -d '{"query": "优化模块A时序，目标<10ns"}'
```

---

### 阶段4：前端和交互（2周）
- [ ] Vue 3项目搭建
- [ ] 任务输入和进度展示
- [ ] WebSocket实时更新
- [ ] 结果可视化

**验收**：浏览器输入指令，看到完整流程

---

### 阶段5：完善和优化（1-2周）
- [ ] 性能优化（缓存、查询优化）
- [ ] 安全加固（JWT鉴权、输入验证）
- [ ] 监控和日志（Prometheus、结构化日志）
- [ ] 文档完善

---

## 关键实现文件（优先级排序）

1. **`src/agents/evaluation_agent.py`** - 核心评判逻辑
2. **`src/agents/master_agent.py`** - 中心化编排
3. **`src/workflows/optimization_workflow.py`** - LangGraph状态图
4. **`src/eda_tools/base.py`** - 工具接口抽象
5. **`src/database/models.py`** - 数据模型
6. **`src/api/routes.py`** - API端点
7. **`frontend/src/App.vue`** - 前端主界面

---

## 技术决策（已确认）

1. **LLM模型**：✅ **Qwen-Max**（能力更强，适合复杂推理和评判）
2. **迭代确认机制**：✅ **用户确认模式**
   - 每次迭代后，系统给出详细的建议（方案、参数、理由）
   - 用户可确认继续或提供反馈
   - 如果用户不认可，基于用户输入信息分析后再迭代

**详细交互设计**：
```json
// 评判Agent返回后的UI交互示例
{
  "iteration": 1,
  "current_result": {"timing": "12ns", "power": "50mW"},
  "evaluation": {
    "status": "FAILED",
    "reason": "时序12ns超过目标10ns，超限20%"
  },
  "next_iteration_suggestions": [
    {
      "option": "A",
      "description": "降低时钟频率至80MHz",
      "parameters": {"clock_freq": "80MHz"},
      "expected_impact": {"timing": "-2.5ns", "power": "-5mW"},
      "reason": "降低时钟可减少传播延迟，但可能影响吞吐量"
    },
    {
      "option": "B",
      "description": "优化关键路径（插入流水线）",
      "parameters": {"pipeline_depth": 2},
      "expected_impact": {"timing": "-3ns", "area": "+50um²"},
      "reason": "流水线可减少逻辑深度，但增加面积"
    }
  ]
}

// 用户操作
// 1. 点击"确认方案A" → 使用方案A的参数继续
// 2. 点击"确认方案B" → 使用方案B的参数继续
// 3. 输入自定义建议 → 基于用户输入重新分析和迭代
```
3. **并发规模**：✅ **1-5人**（小规模，轻量级配置）
4. **集成范围**：✅ **全部Mock**（快速验证Agent编排和评判逻辑）

---

## 技术栈（更新）

---

`★ Insight ─────────────────────────────────────`
这个架构设计采用了**中心化编排模式**，相比去中心化自主协商，它的优势是流程可控、调试简单、易于理解状态变化。LangGraph的状态机机制天然支持这种模式，通过条件边（conditional edges）可以优雅地表达"达标→保存、未达标→迭代"的决策逻辑。评判Agent的对比型设计结合了规则判断和LLM推理，既保证了准确性（数值对比），又提供了可解释性（推理过程）。
`─────────────────────────────────────────────────`
