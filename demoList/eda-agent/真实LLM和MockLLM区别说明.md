# 真实 LLM vs Mock LLM - 完整说明

## 问题

> 为什么我要写 Mock LLM 的实现？不是应该直接调用真实 LLM 吗？

## 答案

**真实情况**：系统会自动调用真实 LLM，我只是添加了 Mock 作为后备。

## 代码流程

### 场景1：使用真实 Claude API

```bash
# 设置环境变量
export ANTHROPIC_API_KEY="sk-ant-xxx..."

# 运行
python3 main.py --llm claude
```

**调用链**：
```
用户输入: "帮我检查模块A"
   ↓
scene_manager.route(user_input)
   ├→ llm_service.classify(text, categories)
   │     ↓
   │  LLMService.classify()
   │     ↓
   │  self.client.messages_create(params)
   │     ↓
   │  ClaudeLLMClient.messages_create(params)  ← 真实 Claude 客户端
   │     ↓
   │  client.messages.create(**params)           ← Anthropic SDK
   │     ↓
   │  HTTP POST to api.anthropic.com
   │     ↓
   └─→ 返回真实 AI 理解: "verify"

verify_scene._parse_task(user_input)
   ├→ _simple_parse() 失败 (正则不匹配)
   │     ↓
   │  _llm_parse()
   │     ↓
   │  llm_service.chat(messages)
   │     ↓
   │  self.client.messages_create(params)
   │     ↓
   │  ClaudeLLMClient.messages_create(params)  ← 真实 Claude 客户端
   │     ↓
   │  client.messages.create(**params)           ← Anthropic SDK
   │     ↓
   │  HTTP POST to api.anthropic.com
   │     ↓
   └─→ 返回真实 AI 解析的 JSON: {"module": "模块A", "goal": null}
```

### 场景2：使用 Mock LLM（默认）

```bash
# 不设置 API Key
python3 main.py  # 默认 --llm mock
```

**调用链**：
```
用户输入: "帮我检查模块A"
   ↓
scene_manager.route(user_input)
   ├→ llm_service.classify(text, categories)
   │     ↓
   │  LLMService.classify()
   │     ↓
   │  self.client.messages_create(params)
   │     ↓
   │  MockLLMClient.messages_create(params)  ← Mock 客户端
   │     ↓
   │  检测请求类型 (classify)
   │     ↓
   │  _classify_by_keywords()              ← 使用关键词匹配
   │     ↓
   └─→ 返回模拟结果: "verify"

verify_scene._parse_task(user_input)
   ├→ _simple_parse() 失败 (正则不匹配)
   │     ↓
   │  _llm_parse()
   │     ↓
   │  llm_service.chat(messages)
   │     ↓
   │  self.client.messages_create(params)
   │     ↓
   │  MockLLMClient.messages_create(params)  ← Mock 客户端
   │     ↓
   │  检测请求类型 (parse_task)
   │     ↓
   │  _mock_parse_task()                ← 使用正则提取
   │     ↓
   └─→ 返回模拟 JSON: {"module": "模块A", "goal": null}
```

## 关键代码

### LLMService（统一接口）

`src/services/llm_service.py:43-68`
```python
def chat(self, messages, temperature, max_tokens, **kwargs):
    """调用 LLM 进行对话"""
    params = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        **kwargs
    }

    # ← 关键：调用 client 的 messages_create 方法
    # client 可能是 ClaudeLLMClient 或 MockLLMClient
    return self.client.messages_create(params)
```

### ClaudeLLMClient（真实 API）

`src/llm_client.py:202-235`
```python
class ClaudeLLMClient(LLMClient):
    def messages_create(self, params: Dict) -> Any:
        """发送消息到 Claude API"""
        # ← 直接调用 Anthropic SDK
        return self.client.messages.create(**params)
        # 返回真实 API 响应对象
```

### MockLLMClient（模拟）

`src/llm_client.py:29-187`
```python
class MockLLMClient(LLMClient):
    def messages_create(self, params: Dict) -> Any:
        """发送 Mock 消息请求"""
        # ← 检测请求类型
        if "分类" in content and "类别" in content:
            # classify 请求
            return self._classify_by_keywords(...)
        elif "解析为 EDA" in content:
            # parse_task 请求
            return self._mock_parse_task(...)
        else:
            # 其他请求
            return MockResponse(content)
```

## 为什么要写 Mock？

1. **开发/测试便利**
   - 不需要每次都调用真实 API
   - 快速、可预测、无成本
   - CI/CD 环境可用

2. **演示功能**
   - 可以展示系统如何工作
   - 不需要用户有 API Key

3. **优雅降级**
   - 如果没有 API Key，系统仍可运行
   - 给用户清晰的提示

## 生产环境建议

### 选项1：强制使用真实 LLM

修改 `config.py`：
```python
class Config:
    # 生产环境强制使用真实 LLM
    LLM_PROVIDER: str = os.getenv("EDA_LLM_PROVIDER", "claude")  # 默认 claude
```

### 选项2：添加警告

修改 `main.py`：
```python
# 验证配置
if not Config.validate():
    if Config.LLM_PROVIDER != "mock":
        print(f"[主程序] ⚠️  LLM_PROVIDER={Config.LLM_PROVIDER} 但 API Key 未设置")
        print(f"[主程序] ⚠️  回退到 mock 模式继续运行")
        Config.LLM_PROVIDER = "mock"
```

## 总结

- ✅ **真实 LLM 会自动工作**：只要有 API Key，系统就调用真实 API
- ✅ **Mock 只是后备**：没有 Key 时用，确保系统可运行
- ✅ **不需要修改代码**：LLMService 统一了接口
- ⚠️ **生产环境建议**：明确设置 `--llm claude` 或 `--llm qwen`

**核心逻辑**：
```
if 有 API Key:
    使用真实 Claude/Qwen API (真正的 AI)
else:
    使用 Mock LLM (基于规则)
```

这就像汽车的"燃油模式"和"电动模式"，系统会根据是否有电自动选择，但两个模式都要实现。
