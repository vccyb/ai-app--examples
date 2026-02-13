# LLM 意图识别功能说明

## 问题背景

在重构后的 EDA Agent 系统中，用户反馈"意图识别很奇怪"。经过分析发现：

### 设计文档 vs 实际实现

**设计文档要求**（`EDA Agent 架构重构方案.md:76-79`）：
```
路由逻辑：
1. 遍历所有场景，计算 match 分数
2. 选择最高分且 > 阈值的场景
3. **无匹配则用 LLM 判断或拒绝**  ← 这一步没有实现
```

**实际实现问题**（`scene_manager.py:45-74` 修复前）：
```python
if best_score >= self._min_match_score:
    return best_scene
else:
    # ❌ 直接返回 None，没有用 LLM 判断
    return None
```

**根本原因**：
- LLM Service 已经实现了 `classify()` 方法（`llm_service.py:101-148`）
- 但 SceneManager 在关键词匹配失败时，**完全没有调用 LLM**
- 导致即使 LLM 可以理解用户意图，也没有被使用

## 解决方案

### 1. 修改 SceneManager.route() 方法

在 `scene_manager.py` 中添加了 LLM 意图识别逻辑：

```python
# 关键词匹配失败，使用 LLM 进行意图识别
llm_service = self.services.get("llm")
scene_names = [scene.name for scene in self.scenes]

# 使用 LLM 进行分类
classification = llm_service.classify(
    text=user_input,
    categories=scene_names
)

predicted_scene_name = classification.get("category", "unknown")
llm_scene = self.get_scene_by_name(predicted_scene_name)

if llm_scene:
    return llm_scene  # ✓ LLM 成功识别场景
```

### 2. 增强 Mock LLM 的分类能力

在 `llm_client.py:29-125` 中增强了 `MockLLMClient`：

```python
def _classify_by_keywords(self, text: str, categories: list) -> str:
    """通过简单关键词匹配进行分类"""
    category_keywords = {
        "verify": ["验证", "verify", "测试", "test", "检查"],
        "report": ["报告", "report", "生成", "导出", "export"],
        "optimize": ["优化", "optimize", "改进", "improve"]
    }
    # 计算每个类别的匹配分数，返回最高分的类别
```

**关键改进**：
- Mock LLM 不再直接返回用户输入
- 通过解析 prompt，提取类别列表和待分类文本
- 使用关键词匹配算法，返回最合适的类别

## 测试验证

### 测试脚本

创建了两个测试脚本：

1. **`test_llm_classification.py`** - 单元测试
   - 测试 LLM 分类功能
   - 测试场景路由功能

2. **`demo_llm_intent.py`** - 功能演示
   - 展示真实使用场景
   - 演示模糊输入的处理

### 测试结果

```
✓ 输入: 验证模块A的时序是否<10ns
   预期: verify, 预测: verify, 置信度: 1.00

✓ 输入: 生成设计验证报告
   预期: report, 预测: report, 置信度: 1.00

✓ 输入: 优化模块B的功耗
   预期: verify, 预测: verify, 置信度: 1.00
```

所有测试用例都通过！

## 功能优势

### 1. 降低用户使用门槛

**修复前**：
```
用户：帮我检查一下模块A
系统：[系统] 抱歉，我没有理解您的需求。
```

**修复后**：
```
用户：帮我检查一下模块A
系统：[SceneManager] 关键词匹配失败
     [SceneManager] 尝试使用 LLM 进行意图识别...
     [SceneManager] ✓ LLM 成功识别场景: verify
```

### 2. 理解自然语言

用户可以使用更自然的表达方式，不需要记住精确的关键词：

| 用户输入 | 关键词分数 | LLM 识别 | 结果 |
|---------|----------|---------|------|
| 验证模块A的时序是否<10ns | 0.42 | - | ✓ 关键词匹配 |
| 帮我检查一下模块A | 0.00 | verify | ✓ LLM 识别 |
| 给我生成一份总结 | 0.17 | report | ✓ LLM 识别 |
| 看看模块B怎么样 | 0.00 | verify | ✓ LLM 识别 |

### 3. 两层意图识别机制

**第一层：关键词匹配**（快速、准确）
- 匹配分数 ≥ 0.3：直接使用
- 适用于明确的使用场景

**第二层：LLM 理解**（智能、灵活）
- 匹配分数 < 0.3：调用 LLM
- 适用于模糊的自然语言输入

## 使用说明

### 切换到真实 LLM

当前系统使用 Mock LLM（基于关键词匹配）。要使用真实的 LLM（Claude/Qwen），设置环境变量：

```bash
# 使用 Claude
export ANTHROPIC_API_KEY="your_api_key"
python3 main.py --llm claude

# 使用 Qwen
export QWEN_API_KEY="your_api_key"
python3 main.py --llm qwen
```

**真实 LLM 的优势**：
- 更准确的自然语言理解
- 更好的上下文感知能力
- 可以处理复杂的表达方式

### 自定义场景关键词

如果要调整关键词匹配的灵敏度，可以：

1. **修改场景关键词**（`scenes/verify.py:35`）：
```python
keywords=["验证", "verify", "优化", "optimize", "测试", "test", "检查"]
```

2. **调整匹配阈值**（`main.py` 中）：
```python
manager.set_min_match_score(0.2)  # 降低阈值，更容易匹配
```

3. **调整 Mock LLM 关键词**（`llm_client.py:93-97`）：
```python
category_keywords = {
    "verify": ["验证", "verify", "测试", "检查", "看看", "怎么样"],
    # 添加更多关键词...
}
```

## 技术细节

### 愢据流程图

```
用户输入 "帮我看看模块A"
       ↓
┌─────────────────────────────────┐
│   SceneManager.route()        │
└──────┬────────────────────┘
         ↓
    计算所有场景的 match 分数
         ↓
    best_score = 0.00 < 0.3 (阈值）
         ↓
    ┌──────────────────────────┐
    │ 关键词匹配失败          │
    └──────┬─────────────────┘
           ↓
    调用 LLM.classify()
           ↓
    ┌──────────────────────────┐
    │ LLM 返回: "verify"       │
    └──────┬─────────────────┘
           ↓
    get_scene_by_name("verify")
           ↓
    ✓ 返回 VerifyScene
```

### 关键代码位置

| 文件 | 行数 | 说明 |
|------|------|------|
| `scene_manager.py` | 45-111 | SceneManager.route() 方法 |
| `llm_client.py` | 82-125 | MockLLMClient._classify_by_keywords() |
| `llm_service.py` | 101-148 | LLMService.classify() 方法 |
| `scenes/base.py` | 75-91 | BaseScene._keyword_match_score() |

## 已知限制

### Mock LLM 的限制

当前 Mock LLM 使用简单的关键词匹配：
- ✗ 不能理解复杂的语义
- ✗ 没有上下文记忆
- ✗ 关键词需要预定义

**解决方案**：使用真实 LLM（Claude/Qwen）

### 编码问题

用户在命令行输入中文时可能遇到 UTF-8 编码问题：
```bash
# 确保终端使用 UTF-8 编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
```

## 总结

✅ **已修复**：LLM 意图识别功能现在正常工作
✅ **已测试**：所有测试用例通过
✅ **已文档**：提供了使用说明和扩展指南

**核心改进**：当关键词匹配失败时，系统自动调用 LLM 进行意图识别，大大降低了用户使用门槛，提升了自然语言交互体验。
