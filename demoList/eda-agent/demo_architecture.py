"""完整的交互式场景选择演示

按照你的理解：
1. 启动时列出所有场景
2. 用户主动选择场景
3. 在场景内输入任务
4. 场景调用服务完成任务
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def demo():
    print("=" * 70)
    print("交互式 EDA Agent - 简化架构演示")
    print("=" * 70)

    print("\n架构流程：")
    print("  1. 用户启动系统")
    print("  2. 显示场景菜单（固定场景列表）")
    print("  3. 用户选择场景（输入数字）")
    print("  4. 进入场景，输入任务")
    print("  5. 场景调用服务完成任务")

    print("\n" + "─" * 70)

    # 模拟场景菜单
    print("可用场景：")
    print("  1. verify - 验证模块是否达到设计目标")
    print("  2. report - 生成和导出设计报告")
    print()

    # 模拟用户选择
    print("\n[用户] 1")
    print("[系统] 已选择场景: verify")

    # 模拟用户输入任务
    print("\n" + "─" * 70)
    print("进入 verify 场景")
    print("─" * 70)

    print("\n请输入任务描述：")
    print("[用户] 验证模块A的时序是否小于10ns")

    print("\n" + "=" * 70)
    print("[系统] 正在处理...")

    print("\n" + "─" * 70)
    print("场景处理流程（简化版）")
    print("─" * 70)

    print("""
步骤 1：调用 RAG 服务
  → rag_service.get_specification("模块A")
  → 返回：{timing: {typical: "10ns", max: "100MHz"}}

步骤 2：调用 EDA 服务
  → eda_service.simulate("模块A", parameters={})
  → 返回：{timing: "10.5ns", power: "50mW", area: "1000um²"}

步骤 3：比较结果
  → 目标：< 10ns
  → 实际：10.5ns
  → 结论：FAIL（未达标）

步骤 4：保存结果
  → state_service.save({...})
    """)

    print("\n" + "=" * 70)
    print("[系统] 处理完成！")
    print("结果：FAIL - 实际 10.5ns 未达目标 10ns")

    print("\n" + "=" * 70)
    print("对比之前的架构")
    print("=" * 70)

    print("""
之前的架构（复杂）：
  用户输入 → LLM 预测场景 → 解析任务 → 执行
  问题：LLM 要猜测用户意图，解析逻辑复杂

现在的架构（简化）：
  用户选择场景 → 输入任务 → LLM 规划步骤 → 调用服务 → 完成
  优势：清晰、可控、LLM 专注于任务规划
    """)


if __name__ == "__main__":
    demo()
