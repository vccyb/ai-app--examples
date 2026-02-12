# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**EDA Agent System** - A multi-agent system for EDA (Electronic Design Automation) tasks.

**Two Versions Available:**
1. **Legacy (v1)** - Rule-driven, Master Agent orchestrates sub-agents
2. **New Generation (v2)** - LLM-driven, AI automatically selects and calls tools ⭐

**Status**: Both versions functional. New generation recommended for natural language interaction.

The system demonstrates how multiple specialized agents can collaborate to solve EDA optimization tasks:

---

## Quick Start

### New Generation (v2) - LLM-Driven ⭐ **推荐**

```bash
# Interactive CLI with Mock LLM (default)
python3 cli_new.py

# With real LLM (requires API key)
python3 cli_new.py --llm claude  # Claude
python3 cli_new.py --llm qwen   # Qwen
```

**Features:**
- Natural language interaction
- AI automatically selects tools
- Multi-turn conversations
- See [docs/llm-agent-usage-guide.md](docs/llm-agent-usage-guide.md)

### Legacy (v1) - Rule-Driven
- User provides natural language instruction (e.g., "优化模块A时序<10ns")
- Master Agent parses and orchestrates the workflow
- Sub-agents handle specialized tasks (knowledge query, simulation, evaluation, data storage)
- Results are aggregated and returned to the user

`★ Insight ─────────────────────────────────────`
**Centralized vs. Decentralized Agents**: This project uses **centralized orchestration** (Master Agent controls the flow) rather than decentralized agent-to-agent negotiation. The benefits are: (1) Predictable debugging - you always know which agent is executing, (2) Clearer state management - state flows through one central coordinator, (3) Easier to understand - the control flow is explicit in the Master Agent code. This pattern is ideal when workflows are structured and predictable, as in EDA tasks where the flow is: query → simulate → evaluate → save.
`─────────────────────────────────────────────────`

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11+ | EDA tool APIs, rich AI ecosystem |
| **Framework** | None (MVP) | No FastAPI/Flask - uses CLI for testing |
| **Data Storage** | In-memory dict | No database - validates agent logic first |
| **LLM** | Mock/Rule-based | No real LLM calls - uses deterministic logic |
| **Testing** | Standalone scripts | `test_workflow.py`, `cli.py` |

### Dependencies (requirements.txt)

```
fastapi
uvicorn[standard]
pydantic
```

Note: FastAPI is listed but not actively used in the MVP. The system is tested via CLI.

## Architecture

### Agent Orchestration Flow

```
User Input: "优化模块A时序<10ns"
       ↓
┌─────────────────────────────────────────┐
│         Master Agent (Orchestrator)       │
│  1. Parse task                           │
│  2. Dispatch to sub-agents               │
│  3. Aggregate results                    │
└──────┬──────────────────┬────────────┘
       ↓         ↓           ↓           ↓
  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌───────────┐
  │RAG Agent  │ │EDA Tool │ │Evaluation │ │  General  │
  │Knowledge  │ │Agent    │ │Agent     │ │  Agent    │
  │Query      │ │         │ │          │ │           │
  └──────────┘ └──────────┘ │(评判）    │ │Data Store │
                                └──────────┘ └───────────┘
```

### Agent Responsibilities

| Agent | File | Responsibility | Key Methods |
|-------|------|----------------|--------------|
| **Master** | `master_agent.py` | Parse user input, orchestrate workflow, aggregate results | `process(user_input)`, `_parse_simple_input()` |
| **RAG** | `rag_agent.py` | Query knowledge base (10 fixed mock entries) | `query(keywords)`, `get_specification(module)` |
| **EDA Tool** | `eda_agent.py` | Run simulation (returns mock results with ±5% variation) | `run_simulation(module, parameters)` |
| **Evaluation** | `evaluation_agent.py` | Compare target vs actual, return PASS/FAIL + suggestion | `evaluate(goal, actual)` |
| **General** | `general_agent.py` | In-memory data storage (tasks, results, evaluations) | `save(data)`, `query(filters)` |

`★ Insight ─────────────────────────────────────`
**Mock Data Strategy**: The EDA Agent uses `random.uniform(0.95, 1.05)` to add ±5% variation to simulation results. This is a clever MVP technique - it prevents users from thinking the system is completely static while keeping debugging predictable. When adding real EDA tools later, you can keep the mock mode for testing by adding a `use_mock=True` parameter.
`─────────────────────────────────────────────────`

## Common Development Commands

### Running the System

```bash
# Run complete workflow test
python3 test_workflow.py

# Run interactive CLI
python3 cli.py "优化模块A时序<10ns"

# Test individual agents
python3 -c "from src.agents.rag_agent import RAGAgent; rag = RAGAgent(); print(rag.query(['时序', '优化']))"
python3 -c "from src.agents.eda_agent import EDAToolAgent; eda = EDAToolAgent(); print(eda.run_simulation('模块A'))"
python3 -c "from src.agents.evaluation_agent import EvaluationAgent; eva = EvaluationAgent(); goal = {'metric': 'timing', 'operator': '<', 'value': '10ns'}; actual = {'timing': '12ns'}; print(eva.evaluate(goal, actual))"
python3 -c "from src.agents.general_agent import GeneralAgent; ga = GeneralAgent(); print(ga.save({'test': 'data'}))"
```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
eda-agent/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── master_agent.py         # Main orchestrator
│   │   ├── rag_agent.py           # Knowledge query (10 mock entries)
│   │   ├── eda_agent.py           # EDA simulation (mock with variation)
│   │   ├── evaluation_agent.py   # Numerical comparison (PASS/FAIL)
│   │   └── general_agent.py       # In-memory data storage
│   └── main.py                    # FastAPI entry point (unused in MVP)
├── tests/                          # Empty (tests embedded in agent files)
├── docs/                          # Design documents
│   ├── eda-agent-architecture-design.md  # Full architecture
│   ├── mvp-agent-design.md               # MVP specifications
│   ├── mvp-completion-report.md          # Completion status
│   └── cli-usage-guide.md               # CLI usage examples
├── cli.py                         # Interactive REPL interface
├── test_workflow.py              # End-to-end workflow test
├── requirements.txt              # Dependencies
└── CLAUDE.md                     # This file
```

## Key Implementation Details

### Master Agent Task Parsing

The `_parse_simple_input()` method uses simple string matching to extract:
- **Action**: Assumes "optimize" (优化)
- **Module**: Extracts word after "优化"
- **Goal**: Extracts target value after "<" operator

**Example**: `"优化模块A时序<10ns"` → `{action: "optimize", module: "模块A", goal: {metric: "timing", operator: "<", value: "10ns"}}`

### Evaluation Agent Comparison Logic

Supports operators: `<`, `<=`, `>`, `>=`, `==`

```python
def _compare(self, actual: float, operator: str, target: float) -> bool:
    if operator == "<": return actual < target
    elif operator == "<=": return actual <= target
    # ... etc
```

**Unit Handling**: Automatically strips units (e.g., "10ns" → 10.0) before comparison.

### RAG Agent Knowledge Base

Fixed 10-entry mock knowledge base stored in `KNOWLEDGE_BASE` dictionary. Query uses simple substring matching - no vector search or embeddings.

## Data Flow Example

### User Request: "优化模块A时序<10ns"

```
1. Master.process("优化模块A时序<10ns")
   ↓
2. RAG.get_specification("模块A")
   Returns: {"timing": {"max_clock": "100MHz", "typical_timing": "10ns"}, ...}
   ↓
3. EDA.run_simulation("模块A")
   Returns: {"timing": "11.7ns", "power": "48.6mW", "area": "1000um²"}  (±5% variation)
   ↓
4. Evaluation.evaluate({"metric": "timing", "operator": "<", "value": "10ns"}, {"timing": "11.7ns", ...})
   Returns: {"status": "FAIL", "reason": "实际11.7ns未达目标10ns，差距+17.0%", "suggestion": "接近目标，微调参数可能达标（差距2.0ns）"}
   ↓
5. General.save() (3 calls for task, simulation, evaluation)
   Returns: "已保存，ID: record_1", "已保存，ID: record_2", "已保存，ID: record_3"
   ↓
6. Master aggregates and returns result dict
```

## CLI Interface (cli.py)

The `cli.py` file provides an interactive REPL with commands:

| Command | Description |
|---------|-------------|
| `优化 [模块] [指标] <值>` | Execute optimization task |
| `查询 [模块]` | Query module specifications |
| `帮助` / `help` | Show help |
| `历史` / `history` | Show last 5 conversation entries |
| `退出` / `quit` / `q` | Exit system |

**Example Session**:
```
🤖 EDA Agent系统 - 交互式界面
🎯 EDA > 优化模块A时序<10ns
🔄 正在处理: 优化模块A时序<10ns
[Master] 收到用户指令: 优化模块A时序<10ns
[Master] 步骤1：查询RAG知识...
...
🎯 EDA > quit
👋 再见！
```

## Testing Strategy

### Test Files

Each agent file has `if __name__ == "__main__"` block with standalone tests:

```bash
# Test RAG Agent
python3 src/agents/rag_agent.py

# Test EDA Agent
python3 src/agents/eda_agent.py

# Test Evaluation Agent
python3 src/agents/evaluation_agent.py

# Test General Agent
python3 src/agents/general_agent.py

# Test Master Agent (full workflow)
python3 src/agents/master_agent.py
```

### End-to-End Test

```bash
python3 test_workflow.py
```

Expected output includes:
- All 5 agent execution logs
- PASS/FAIL status
- Simulation results (timing, power, area)
- Evaluation reasoning and suggestion

## Design Philosophy (MVP Approach)

This project intentionally **omits** complex features to focus on core agent collaboration:

- ❌ No database (uses in-memory dict)
- ❌ No real LLM calls (uses rule-based logic)
- ❌ No real EDA tools (mock results with variation)
- ❌ No vector search (simple keyword matching)
- ❌ No complex state management (single-pass execution)
- ❌ No frontend (CLI-only)

**Why**: This approach validates that multi-agent orchestration works before investing in complex integrations. Once the MVP is proven, real components can be added incrementally.

## Known Issues and TODOs

### Current Limitations

1. **Simple Input Parsing**: Only handles "优化[模块][指标]<值>" format
2. **No Error Recovery**: Exceptions propagate without graceful handling
3. **Single Metric Evaluation**: Can't evaluate timing + power + area simultaneously
4. **No Iteration**: Doesn't loop/retry on failure (single execution only)
5. **Mock Data**: All results are predetermined
6. **No Persistence**: All data lost on restart

### Future Enhancements

See `docs/eda-agent-architecture-design.md` for full production architecture including:
- LangGraph for complex workflow state management
- Real EDA tool integration (Vivado, Design Compiler)
- PostgreSQL for persistence
- Qwen-Max LLM for natural language understanding
- Vue 3 frontend with WebSocket updates
- Multi-metric Pareto optimization

## Important File Locations

| File | Purpose | Key Lines |
|-------|---------|-----------|
| `master_agent.py:23-95` | Main orchestration logic | `process()` method |
| `evaluation_agent.py:11-74` | Core comparison logic | `evaluate()` method |
| `eda_agent.py:12-49` | Simulation mocking | `run_simulation()` with random variation |
| `cli.py:112-159` | REPL main loop | Input handling and command routing |
| `test_workflow.py:15-65` | End-to-end test | Complete workflow validation |

## Glossary

- **EDA**: Electronic Design Automation - software tools for designing electronic systems
- **RAG**: Retrieval-Augmented Generation - knowledge query pattern
- **Agent**: Autonomous software component with specific responsibilities
- **Orchestration**: Coordinating multiple agents to complete a workflow
- **Mock**: Simulated implementation for testing without real dependencies

---

`★ Insight ─────────────────────────────────────`
**When to Extend This MVP**: This MVP is ideal for learning agent orchestration patterns. To extend it to production, consider: (1) Start with **real database** - adds persistence with minimal behavior change, (2) Then add **real LLM** for natural language parsing, (3) Finally add **real EDA tools** - the most complex integration due to API differences between tools. This incremental approach ensures you can debug each layer before adding the next complexity.
`─────────────────────────────────────────────────`
