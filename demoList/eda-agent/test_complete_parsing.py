#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整测试任务解析功能（包括简单解析和 LLM 解析）"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scenes.verify import VerifyScene
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.eda_service import EDAService
from services.state_service import StateService


def test_complete_task_parsing():
    """完整测试任务解析功能"""
    print("=" * 70)
    print("完整测试任务解析功能（简单解析 + LLM 解析）")
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
            "description": "标准格式（简单解析应该成功）",
            "has_goal": True
        },
        {
            "input": "帮我检查一下模块A",
            "description": "模糊输入（简单解析失败，LLM 解析）",
            "has_goal": False
        },
        {
            "input": "查询模块B的设计规范",
            "description": "查询规范（简单解析成功）",
            "has_goal": False
        },
        {
            "input": "看看模块C的功耗情况",
            "description": "完全模糊的表述（LLM 解析）",
            "has_goal": False
        }
    ]

    success_count = 0
    total_count = len(test_cases)

    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"测试 {i}/{total_count}: {case['description']}")
        print('=' * 70)

        user_input = case["input"]
        print(f"用户输入: {user_input}")

        # 解析任务
        task = verify_scene._parse_task(user_input)

        if task:
            has_goal = task.get('goal') is not None
            expected_goal = case.get("has_goal", False)

            print(f"\n✓ 解析成功：")
            print(f"   模块: {task.get('module')}")
            print(f"   目标: {task.get('goal')}")

            # 验证是否与预期一致
            if has_goal == expected_goal:
                print(f"   ✓ 结果符合预期")
                success_count += 1
            else:
                print(f"   ⚠ 结果与预期不符（预期 has_goal={expected_goal}）")
        else:
            print(f"\n✗ 解析失败")

    # 总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print(f"通过：{success_count}/{total_count}")
    print(f"成功率：{success_count/total_count*100:.1f}%")

    if success_count == total_count:
        print("\n✓ 所有测试通过！")
    else:
        print(f"\n⚠ {total_count - success_count} 个测试失败")

    print("=" * 70)


if __name__ == "__main__":
    test_complete_task_parsing()
