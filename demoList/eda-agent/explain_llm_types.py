#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对比真实 LLM 和 Mock LLM 的行为"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from llm_client import create_llm_client


def test_real_llm():
    """测试真实 LLM 客户端"""
    print("=" * 70)
    print("真实 LLM 客户端测试（Claude）")
    print("=" * 70)

    try:
        # 创建真实 Claude 客户端
        client = create_llm_client(
            "claude",
            api_key="test_key",  # 只是为了测试，真实调用会失败
            model="claude-sonnet-4-5"
        )

        print(f"\n✓ 成功创建 Claude 客户端")
        print(f"   类型: {type(client).__name__}")
        print(f"   模型: {client.model}")

        # 测试消息创建
        print(f"\n真实 LLM 调用方式：")
        print(f"   client.messages_create(params)")
        print(f"   → 调用 Anthropic SDK")
        print(f"   → 返回真实 API 响应对象")
        print(f"   → 包含 content, stop_reason, model 等字段")

    except Exception as e:
        print(f"\n✗ 创建失败：{e}")


def test_mock_llm():
    """测试 Mock LLM 客户端"""
    print("\n" + "=" * 70)
    print("Mock LLM 客户端测试")
    print("=" * 70)

    # 创建 Mock 客户端
    client = create_llm_client("mock", model="mock-model")

    print(f"\n✓ 成功创建 Mock 客户端")
    print(f"   类型: {type(client).__name__}")
    print(f"   模型: {client.model}")

    # 测试消息创建
    print(f"\nMock LLM 调用方式：")
    print(f"   client.messages_create(params)")
    print(f"   → 使用规则和关键词匹配")
    print(f"   → 返回模拟的响应（字符串或 MockResponse）")
    print(f"   → 不调用真实 API")

    # 测试分类
    print(f"\n测试分类功能：")
    messages = [{"role": "user", "content": "请将'帮我检查模块A'分类到这些类别之一：verify, report"}]

    response = client.messages_create({"messages": messages})
    print(f"   输入: 帮我检查模块A")
    print(f"   响应: {response}")

    if hasattr(response, 'content'):
        print(f"   分类结果: {response.content}")


def explain_difference():
    """解释两种 LLM 的区别"""
    print("\n" + "=" * 70)
    print("真实 LLM vs Mock LLM 对比")
    print("=" * 70)

    print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│                        真实 LLM (Claude/Qwen)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 启动方式：                                                      │
│   python3 main.py --llm claude    或    python3 main.py --llm qwen    │
│                                                                 │
│ 工作流程：                                                        │
│   1. LLMService.chat(messages)                                       │
│   2. ClaudeLLMClient.messages_create(params)                             │
│   3. client.messages.create(**params)  ← Anthropic/Qwen SDK           │
│   4. 发送 HTTP 请求到真实 API                                      │
│   5. 返回真实 AI 响应                                            │
│                                                                 │
│ 优势：                                                           │
│   ✓ 真正的 AI 理解能力                                            │
│   ✓ 可以处理复杂的语义和上下文                                       │
│   ✓ 结果更准确                                                     │
│                                                                 │
│ 劣势：                                                           │
│   ✗ 需要 API Key                                                   │
│   ✗ 需要 Internet 连接                                              │
│   ✗ 有 API 调用成本                                                 │
│   ✗ 响应速度慢（几秒）                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        Mock LLM (本地模拟)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 启动方式：                                                    │
│   python3 main.py --llm mock  (默认)                            │
│                                                                 │
│ 工作流程：                                                       │
│   1. LLMService.chat(messages)                                     │
│   2. MockLLMClient.messages_create(params)                             │
│   3. 使用规则匹配（关键词、正则）                                │
│   4. 返回模拟响应（JSON 字符串或 MockResponse）                     │
│   - classify: 基于 category_keywords 字典匹配                          │
│   - parse_task: 基于正则表达式提取                               │
│                                                                 │
│ 优势：                                                           │
│   ✓ 无需 API Key                                                   │
│   ✓ 无需 Internet 连接                                              │
│   ✓ 无 API 调用成本                                                 │
│   ✓ 响应速度快（毫秒级）                                            │
│   ✓ 可预测、可调试                                                 │
│                                                                 │
│ 劣势：                                                           │
│   ✗ 只能基于预定义规则                                             │
│   ✗ 无法真正理解语义                                                 │
│   ✗ 复杂输入可能识别错误                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        代码流程                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                 │
│  用户输入 "帮我检查模块A"                                        │
│       ↓                                                         │
│  scene_manager.route(user_input)                                      │
│       ↓                                                         │
│  关键词匹配失败 (score < 0.3)                                      │
│       ↓                                                         │
│  llm_service.classify(text=user_input, categories=["verify", "report"])      │
│       ↓                                                         │
│  ┌────────────┴────────────┐                                     │
│  ↓             ↓              │                                     │
│  真实 LLM      Mock LLM      │                                     │
│  ↓             ↓              │                                     │
│  Claude API     关键词匹配      │                                     │
│  返回 "verify"  返回 "verify"    │                                     │
│  ↓             ↓              │                                     │
│  verify_scene.run()        │                                     │
│       ↓                │                                     │
│  _parse_task(user_input)   │                                     │
│       ↓                │                                     │
│  ┌────────────┴────────────┐                                     │
│  ↓             ↓              │                                     │
│  真实 LLM      Mock LLM      │                                     │
│  ↓             ↓              │                                     │
│  _simple_parse()   _simple_parse()   │                                     │
│  (正则提取)     (正则提取)      │                                     │
│  ↓             ↓              │                                     │
│  成功          失败          │                                     │
│  ↓             ↓              │                                     │
│  返回 task     ↓              │                                     │
│               调用 LLM      │                                     │
│               _llm_parse()   │                                     │
│               ↓              │                                     │
│  Claude API     │                                     │
│  返回 JSON      │                                     │
│  ↓              │                                     │
│  解析成功       │                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

总结：
  真实 LLM：真正的 AI，准确但需要 API Key 和网络
  Mock LLM：基于规则的模拟，快速但能力有限

使用建议：
  - 开发/测试：用 Mock LLM (默认)
  - 生产环境：用真实 LLM (claude/qwen)
  - 演示/调试：用 Mock LLM (可预测、快速)
    """)


if __name__ == "__main__":
    test_mock_llm()
    test_real_llm()
    explain_difference()
