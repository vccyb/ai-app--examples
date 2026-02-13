#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实 LLM 调用演示"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def demo_real_llm_parse():
    """演示真实 LLM 如何处理任务解析"""
    print("=" * 70)
    print("真实 LLM 任务解析演示")
    print("=" * 70)

    from services.llm_service import LLMService

    print("\n场景1: 使用真实 Claude API（如果有 API Key）")
    print("-" * 70)

    # 尝试创建真实 Claude 客户端
    try:
        llm_service = LLMService(
            client_type="claude",
            model="claude-sonnet-4-5",
            api_key=os.getenv("ANTHROPIC_API_KEY")  # 从环境变量读取
        )

        print("✓ 成功创建 Claude LLM 服务")
        print(f"   客户端类型: {llm_service.client_type}")

        # 测试任务解析
        user_input = "验证模块A的时序是否小于10纳秒"
        print(f"\n用户输入: {user_input}")

        prompt = f"""请将以下用户输入解析为 EDA 验证任务。

用户输入：{user_input}

请返回 JSON 格式：
{{
  "module": "模块名称（如：模块A、模块B、模块C）",
  "goal": {{
    "metric": "指标名称（timing/power/area）",
    "operator": "比较符（<, <=, >, >=, ==）",
    "value": "目标值（如：10ns, 50mW, 1000um²）"
  }}
}}"""

        messages = [{"role": "user", "content": prompt}]

        print("\n调用 Claude API...")
        response = llm_service.chat(messages, temperature=0.3)

        print("\n收到 Claude API 响应:")
        print(f"   响应类型: {type(response)}")

        if hasattr(response, 'content'):
            print(f"   内容类型: {type(response.content)}")

            if isinstance(response.content, list) and len(response.content) > 0:
                first_block = response.content[0]
                if hasattr(first_block, 'text'):
                    print(f"   解析结果:")
                    print(f"   {first_block.text}")
                    import json
                    try:
                        parsed = json.loads(first_block.text)
                        print(f"\n   ✓ 成功解析为 JSON:")
                        print(f"      模块: {parsed.get('module')}")
                        print(f"      目标: {parsed.get('goal')}")

                    except:
                        print(f"\n   ✗ 不是有效的 JSON 格式")

    except ValueError as e:
        print(f"\n✗ 无法创建 Claude 客户端: {e}")
        print(f"   原因: ANTHROPIC_API_KEY 环境变量未设置")

    print("\n" + "=" * 70)
    print("关键区别：")
    print("=" * 70)
    print("""
真实 LLM 调用流程：
  1. verify._llm_parse(user_input)
     ↓
  2. llm_service.chat(messages)
     ↓
  3. llm_service.client.messages_create(params)
     ↓
  4. ClaudeLLMClient.messages_create(params)
     ↓
  5. client.messages.create(**params)  ← Anthropic SDK
     ↓
  6. HTTP POST https://api.anthropic.com/v1/messages
     ↓
  7. 返回真实 AI 响应对象

Mock LLM 调用流程：
  1. verify._llm_parse(user_input)
     ↓
  2. llm_service.chat(messages)
     ↓
  3. llm_service.client.messages_create(params)
     ↓
  4. MockLLMClient.messages_create(params)
     ↓
  5. 检测请求类型（classify 还是 parse_task）
     ↓
  6. 使用规则匹配：
     - classify: category_keywords 字典匹配
     - parse_task: 正则表达式提取
     ↓
  7. 返回模拟字符串或 MockResponse

关键点：
  - 真实 LLM 返回的是对象，content 是数组
  - Mock LLM 返回的是字符串或 MockResponse
  - llm_service._extract_response_text() 会自动处理这两种情况
    """)


if __name__ == "__main__":
    demo_real_llm_parse()
