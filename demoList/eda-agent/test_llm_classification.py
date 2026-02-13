#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 LLM 意图识别功能"""
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scene_manager import SceneManager
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.eda_service import EDAService
from services.state_service import StateService


def test_llm_classification():
    """测试 LLM 分类功能"""
    print("=" * 70)
    print("测试 LLM 意图识别功能")
    print("=" * 70)

    # 创建服务
    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    # 创建场景管理器（不注册具体场景，只测试分类）
    manager = SceneManager(services)

    # 测试用例
    test_cases = [
        ("验证模块A的时序是否<10ns", "verify"),
        ("生成设计验证报告", "report"),
        ("优化模块B的功耗", "verify"),  # 优化也会归类到验证
        ("导出仿真结果", "report"),
        ("测试模块C", "verify"),
    ]

    print("\n测试关键词匹配：")
    print("-" * 70)

    llm_service = services["llm"]
    scene_names = ["verify", "report"]

    for text, expected in test_cases:
        try:
            result = llm_service.classify(
                text=text,
                categories=scene_names
            )

            predicted = result.get("category", "unknown")
            confidence = result.get("confidence", 0.0)
            status = "✓" if predicted == expected else "✗"

            print(f"\n{status} 输入: {text}")
            print(f"   预期: {expected}, 预测: {predicted}, 置信度: {confidence:.2f}")

        except Exception as e:
            print(f"\n✗ 输入: {text}")
            print(f"   错误: {str(e)}")

    print("\n" + "=" * 70)


def test_scene_routing():
    """测试场景路由功能"""
    print("\n" + "=" * 70)
    print("测试场景路由功能")
    print("=" * 70)

    from scenes.verify import VerifyScene
    from scenes.report import ReportScene

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

    # 测试用例
    test_cases = [
        "验证模块A的时序是否<10ns",
        "生成设计验证报告",
        "帮我看看模块B",
        "导出结果",
    ]

    print("\n测试场景路由：")
    print("-" * 70)

    for text in test_cases:
        scene = manager.route(text)
        scene_name = scene.name if scene else "None"
        print(f"\n输入: {text}")
        print(f"   路由到: {scene_name}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_llm_classification()
    test_scene_routing()
    print("\n测试完成！")
