#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LLM 意图识别功能演示

展示当关键词匹配失败时，LLM 如何自动识别用户意图并路由到正确的场景
"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scene_manager import SceneManager
from controller import Controller
from scenes.verify import VerifyScene
from scenes.report import ReportScene
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.eda_service import EDAService
from services.state_service import StateService


def demo():
    """演示 LLM 意图识别"""
    print("\n" + "=" * 70)
    print("LLM 意图识别功能演示".center(70))
    print("=" * 70)

    print("\n这个演示展示了系统如何处理模糊的用户输入：")
    print("1. 当关键词匹配分数 < 0.3 时，系统自动调用 LLM 进行意图识别")
    print("2. LLM 分析用户输入，预测应该使用的场景")
    print("3. 系统将请求路由到 LLM 预测的场景")
    print("\n" + "-" * 70)

    # 创建服务
    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    # 创建场景管理器并注册场景
    manager = SceneManager(services)
    manager.register_scene(VerifyScene(services))
    manager.register_scene(ReportScene(services))

    # 创建控制器
    controller = Controller()

    # 演示用例
    demo_cases = [
        {
            "input": "帮我检查一下模块A",
            "description": "模糊的验证请求（没有明确目标和指标）",
            "expected": "verify"
        },
        {
            "input": "给我生成一份总结",
            "description": "模糊的报告请求（使用了非关键词'总结'）",
            "expected": "report"
        },
        {
            "input": "看看模块B怎么样",
            "description": "非常模糊的请求（没有明确动作）",
            "expected": "verify 或 report"
        }
    ]

    for i, case in enumerate(demo_cases, 1):
        print(f"\n演示 {i}/{len(demo_cases)}: {case['description']}")
        print("=" * 70)

        user_input = case["input"]
        expected = case["expected"]

        print(f"\n用户输入: {user_input}")
        print(f"预期路由到: {expected}")

        # 执行路由
        print("\n系统处理流程：")
        print("-" * 70)

        scene = manager.route(user_input)

        if scene:
            print(f"\n✓ 成功路由到场景: {scene.name}")
            print(f"   场景描述: {scene.description}")

            # 如果路由正确
            if expected in scene.name or (expected == "verify 或 report" and scene.name in ["verify", "report"]):
                print(f"   ✓ 路由正确")
            else:
                print(f"   ✗ 路由可能不正确（预期：{expected}）")
        else:
            print(f"\n✗ 未能路由到任何场景")

        print()

    # 总结
    print("\n" + "=" * 70)
    print("演示总结".center(70))
    print("=" * 70)
    print("\n关键优势：")
    print("✓ 不需要用户使用精确的关键词")
    print("✓ 系统可以理解自然的表达方式")
    print("✓ 当关键词匹配失败时，LLM 作为后备方案")
    print("✓ 降低用户使用门槛，提升体验")
    print("\n提示：")
    print("- 使用真实 LLM（Claude/Qwen）时，意图识别会更准确")
    print("- 当前使用 Mock LLM，基于简单的关键词匹配")
    print("- 可以通过设置环境变量切换到真实 LLM")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo()
