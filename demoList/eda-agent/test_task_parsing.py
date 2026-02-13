#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试任务解析功能"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scenes.verify import VerifyScene
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.eda_service import EDAService
from services.state_service import StateService


def test_task_parsing():
    """测试任务解析功能"""
    print("=" * 70)
    print("测试任务解析功能")
    print("=" * 70)

    # 创建服务
    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    # 创建验证场景
    verify_scene = VerifyScene(services)

    # 测试用例
    test_cases = [
        {
            "input": "验证模块A的时序是否<10ns",
            "description": "标准格式（应该被简单解析）"
        },
        {
            "input": "帮我检查一下模块A",
            "description": "模糊输入（需要 LLM 解析）"
        },
        {
            "input": "查询模块B的设计规范",
            "description": "查询规范（没有目标值）"
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}/{len(test_cases)}: {case['description']}")
        print("-" * 70)

        user_input = case["input"]
        print(f"用户输入: {user_input}")

        # 解析任务
        task = verify_scene._parse_task(user_input)

        if task:
            print(f"\n✓ 解析成功：")
            print(f"   模块: {task.get('module')}")
            print(f"   指标: {task.get('goal')}")
        else:
            print(f"\n✗ 解析失败")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_task_parsing()
