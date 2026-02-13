# EDA Agent 架构重构方案 v2
## 目标
构建可扩展的多场景 Agent 系统，支持：
* 多场景：验证、报告、未来更多场景
* 人机协作：计划确认、迭代优化
* 模块复用：基础服务可被任意场景组合调用
* 简单可运行：MVP 先跑通，预留扩展能力
## 整体架构
```warp-runnable-command
用户输入
    ↓
┌─────────────────────────────────────────┐
│          SceneManager (场景管理器)       │
│  - 注册所有场景                          │
│  - 路由到匹配的场景                      │
│  - 处理无匹配情况                        │
└───────────────────┬─────────────────────┘
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
┌────────┐    ┌────────┐    ┌────────┐
│Verify  │    │Report  │    │ 未来   │
│Scene   │    │Scene   │    │ 场景   │
└────┬───┘    └────┬───┘    └────────┘
     │             │
     └──────┬──────┘
            ↓
┌─────────────────────────────────────────┐
│           Services (基础服务层)          │
├─────────┬─────────┬─────────┬───────────┤
│ LLM     │ RAG     │ EDA     │ State     │
│ Service │ Service │ Service │ Service   │
└─────────┴─────────┴─────────┴───────────┘
```
## 核心模块设计
### 1. Services 层（基础服务，通用无业务逻辑）
#### LLMService
* 职责：统一的 LLM 调用接口
* 方法：`chat()`, `structured_output()`, `classify()`
* 配置：支持不同模型切换
#### RAGService
* 职责：知识查询
* 方法：`query(keywords)`, `get_spec(module)`
* 当前：硬编码 mock，接口预留向量检索
#### EDAService
* 职责：EDA 仿真执行
* 方法：`simulate(module, params)`, `get_status()`
* 当前：mock 返回，接口预留真实工具对接
#### StateService
* 职责：JSON 文件持久化
* 方法：`save(data)`, `query(filters)`, `get_history()`
* 存储：`data/state.json`
### 2. Scenes 层（场景，包含业务逻辑）
#### BaseScene（基类）
```python
class BaseScene:
    name: str           # 场景名
    description: str    # 场景描述
    keywords: list      # 触发关键词
    def match(user_input) -> float   # 匹配度 0-1
    def run(user_input) -> Generator # 执行（yield 步骤结果）
```
#### VerifyScene（验证场景）- MVP 重点
* 触发："验证"、"优化"、"测试" 等
* 流程：
    1. 解析目标（模块+指标+阈值）
    2. 生成执行计划
    3. 等待用户确认
    4. 执行计划（查询→仿真→评估→保存）
    5. 失败时询问是否迭代
#### ReportScene（报告场景）- 示例
* 触发："生成报告"、"导出结果" 等
* 流程：查询历史 → 汇总数据 → 生成报告
### 3. SceneManager（场景管理器）
* 职责：场景注册、路由、生命周期管理
* 路由逻辑：
    1. 遍历所有场景，计算 match 分数
    2. 选择最高分且 > 阈值的场景
    3. 无匹配则用 LLM 判断或拒绝
### 4. 交互控制器
* 职责：处理人机交互（确认、迭代、退出）
* 关键：场景 `yield` 出需要确认的节点，控制器等待用户输入
## 文件结构
```warp-runnable-command
eda-agent/
├── src/
│   ├── __init__.py
│   ├── services/              # 基础服务
│   │   ├── __init__.py
│   │   ├── llm_service.py     # LLM 调用
│   │   ├── rag_service.py     # 知识查询
│   │   ├── eda_service.py     # EDA 仿真
│   │   └── state_service.py   # JSON 持久化
│   │
│   ├── scenes/                # 场景
│   │   ├── __init__.py
│   │   ├── base.py            # 场景基类
│   │   ├── verify.py          # 验证场景
│   │   └── report.py          # 报告场景（示例）
│   │
│   ├── scene_manager.py       # 场景管理器
│   └── controller.py          # 交互控制器
│
├── data/
│   └── state.json             # 持久化文件
│
├── main.py                    # 入口
└── config.py                  # 配置（API Key 等）
```
## 数据流设计
### 场景执行的 yield 协议
```python
# 场景 yield 的消息类型
{"type": "info", "content": "..."}           # 普通信息
{"type": "plan", "steps": [...], "need_confirm": True}  # 计划，需确认
{"type": "step_result", "step": 1, "result": {...}}     # 步骤结果
{"type": "ask", "question": "...", "options": [...]}    # 询问用户
{"type": "done", "summary": {...}}           # 完成
{"type": "error", "message": "..."}          # 错误
```
### 持久化数据结构 (state.json)
```json
{
  "tasks": [
    {"id": "t1", "input": "...", "scene": "verify", "status": "done", "created_at": "..."}
  ],
  "simulations": [
    {"id": "s1", "task_id": "t1", "module": "模块A", "result": {...}}
  ],
  "evaluations": [
    {"id": "e1", "task_id": "t1", "goal": {...}, "actual": {...}, "status": "PASS"}
  ]
}
```
## 实现步骤
### Phase 1: 基础框架
1. 创建 `services/state_service.py` - JSON 持久化
2. 创建 `services/llm_service.py` - LLM 封装
3. 创建 `services/rag_service.py` - 复用现有 RAGAgent
4. 创建 `services/eda_service.py` - 复用现有 EDAToolAgent
### Phase 2: 场景框架
5. 创建 `scenes/base.py` - 场景基类
6. 创建 `scene_manager.py` - 场景管理器
7. 创建 `controller.py` - 交互控制器
### Phase 3: 验证场景
8. 创建 `scenes/verify.py` - 验证场景完整实现
### Phase 4: 集成测试
9. 创建 `main.py` - 入口
10. 端到端测试
### Phase 5: 扩展示例
11. 创建 `scenes/report.py` - 报告场景（可选）
## 交互流程示例
```warp-runnable-command
$ python main.py
🚀 EDA Agent 启动
注册场景: verify(验证场景), report(报告场景)
你: 验证模块A的时序是否满足<10ns
[SceneManager] 匹配场景: verify (score=0.95)
[VerifyScene] 解析任务:
  - 模块: 模块A
  - 指标: timing
  - 目标: < 10ns
[VerifyScene] 生成执行计划:
  1. 查询模块A设计规范
  2. 运行模块A仿真
  3. 评估timing是否<10ns
  4. 保存验证记录
系统: 确认执行以上计划？(y/n/修改)
你: y
[执行] 步骤1: 查询规范... ✓
  规范: timing典型值10ns, 最大100MHz
[执行] 步骤2: 运行仿真... ✓
  结果: timing=11.2ns, power=48mW
[执行] 步骤3: 评估结果... ✗
  状态: FAIL
  原因: 实际11.2ns未达目标10ns，差距+1.2ns(+12%)
系统: 未达标。是否调整参数重试？(y/n)
你: y
系统: 请输入调整方案（或输入'建议'让系统推荐）:
你: 建议
[LLM建议] 可尝试降低时钟频率至90MHz，预计timing可改善至~9.8ns
系统: 采用此建议？(y/n)
你: y
[迭代] 使用新参数重新仿真...
  结果: timing=9.6ns ✓
[执行] 步骤4: 保存记录... ✓
系统: 验证完成！模块A timing=9.6ns < 10ns ✓
```
## 扩展性设计
### 新增场景
1. 在 `scenes/` 下创建新文件
2. 继承 `BaseScene`，实现 `match()` 和 `run()`
3. 在 `scene_manager.py` 中注册
### 新增服务
1. 在 `services/` 下创建新文件
2. 在 `SceneManager` 初始化时注入到场景
### 对接真实 EDA 工具
1. 修改 `eda_service.py` 的实现
2. 场景代码无需改动
## 待考虑问题
1. **会话上下文**：多轮对话时如何保持上下文？
   → 当前方案：每个任务独立，不支持跨任务上下文
2. **并发**：多个任务同时运行？
   → 当前方案：单任务串行，MVP 够用
3. **错误恢复**：执行中断如何恢复？
   → 当前方案：任务状态持久化，可查看历史但不支持恢复
4. **单位解析**：如何处理各种单位格式？
   → 当前方案：在提示中明确支持的格式（ns/mW/um²）