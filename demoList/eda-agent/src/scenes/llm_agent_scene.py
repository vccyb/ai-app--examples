"""基于 LLM 规划的场景框架

每个场景的执行流程：
1. 用户输入任务描述
2. LLM 分析任务，生成执行步骤
3. 场景按步骤调用服务
4. 返回结果
"""
from typing import Dict, List, Optional, Generator
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class LLMAgentScene(BaseScene):
    """基于 LLM 规划的智能场景

    场景不预定义执行逻辑，而是让 LLM 为每个任务生成执行计划
    """

    def __init__(self, services: Dict):
        super().__init__(
            name="llm_agent",
            description="智能场景 - LLM 生成执行计划",
            keywords=[],
            services=services
        )

    def match(self, user_input: str) -> float:
        """不需要匹配，因为用户主动选择场景"""
        return 0.0

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        """执行场景

        Args:
            user_input: 用户在场景内的任务输入

        Yields:
            执行过程中的消息
        """
        yield self._create_info_message(f"\n[{self.name.upper()}] 场景启动")

        # 步骤1：LLM 分析任务，生成执行计划
        yield self._create_info_message(f"[{self.name}] 正在分析任务...")

        plan = self._generate_execution_plan(user_input)

        if not plan:
            yield self._create_error_message("无法生成执行计划")
            return

        yield self._create_plan_message(
            plan.get("steps", []),
            need_confirm=True
        )

        # 步骤2：执行计划
        yield self._create_info_message(f"\n[{self.name}] 正在执行计划...")

        results = []
        for i, step in enumerate(plan.get("steps", []), 1):
            yield self._create_info_message(f"\n执行步骤 {i}/{len(plan['steps'])}")

            result = yield from self._execute_step(step, user_input)
            results.append(result)

            status = result.get("status", "UNKNOWN")
            yield self._create_step_result_message(
                step=i,
                result=result,
                status=status
            )

        # 步骤3：完成
        yield self._create_done_message({
            "summary": f"执行完成，共 {len(results)} 个步骤",
            "results": results
        })

    def _generate_execution_plan(self, user_input: str) -> Optional[Dict]:
        """使用 LLM 生成执行计划

        Args:
            user_input: 用户任务描述

        Returns:
            执行计划字典，包含 steps 列表
        """
        if not self.llm_service:
            return None

        # 构建 prompt，让 LLM 生成执行计划
        prompt = f"""你是一个 EDA（电子设计自动化）助手。

用户的任务：{user_input}

请分析这个任务，并生成详细的执行步骤。

可用服务：
- rag_service: 查询知识库，获取模块规范和设计信息
- eda_service: 运行仿真，获取实际指标（时序、功耗、面积）
- state_service: 保存数据和结果

请生成执行计划，返回 JSON 格式：
{{
  "reasoning": "分析过程，说明为什么需要这些步骤",
  "steps": [
    {{"action": "查询规范", "service": "rag_service", "params": {{"module": "模块A"}}},
    {{"action": "运行仿真", "service": "eda_service", "params": {{"module": "模块A", "parameters": {{"timing": "typical"}}}},
    {{"action": "比较结果", "params": {{"target": "<10ns", "actual": "{{仿真结果中的 timing 值}}"}}}
  ]
}}

注意：
1. action 应该是具体的动作（查询、仿真、比较、保存等）
2. 如果需要调用服务，明确指定 service 和 params
3. 步骤应该逻辑清晰，可按顺序执行

只返回 JSON，不要其他内容。"""

        messages = [{"role": "user", "content": prompt}]

        try:
            response = self.llm_service.chat(messages, temperature=0.5)
            response_text = self.llm_service._extract_response_text(response)

            import json
            plan = json.loads(response_text)

            # 验证 plan 格式
            if "steps" in plan and isinstance(plan["steps"], list):
                return plan

            return None

        except Exception as e:
            print(f"[{self.name}] LLM 计划生成失败: {str(e)}")
            return None

    def _execute_step(self, step: Dict, user_input: str) -> Generator[Dict, None, None]:
        """执行单个步骤

        Args:
            step: 步骤字典
            user_input: 用户原始输入

        Yields:
            步骤执行结果

        Returns:
            步骤执行结果字典
        """
        action = step.get("action", "")
        service_name = step.get("service", "")
        params = step.get("params", {})

        yield self._create_info_message(f"  动作: {action}")

        # 根据服务名称调用相应服务
        if service_name == "rag_service" and self.rag_service:
            result = self._call_rag_service(params)
        elif service_name == "eda_service" and self.eda_service:
            result = self._call_eda_service(params)
        elif service_name == "state_service" and self.state_service:
            result = self._call_state_service(params)
        else:
            # 没有指定服务，返回成功
            result = {"status": "SUCCESS", "message": f"完成动作: {action}"}

        yield self._create_info_message(f"  结果: {result}")

        return result

    def _call_rag_service(self, params: Dict) -> Dict:
        """调用 RAG 服务"""
        try:
            module = params.get("module")
            spec = self.rag_service.get_specification(module)
            return {
                "status": "SUCCESS",
                "service": "rag",
                "result": spec
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "service": "rag",
                "error": str(e)
            }

    def _call_eda_service(self, params: Dict) -> Dict:
        """调用 EDA 服务"""
        try:
            module = params.get("module")
            parameters = params.get("parameters", {})

            sim_result = self.eda_service.simulate(module, parameters)
            return {
                "status": "SUCCESS",
                "service": "eda",
                "result": sim_result
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "service": "eda",
                "error": str(e)
            }

    def _call_state_service(self, params: Dict) -> Dict:
        """调用 State 服务"""
        try:
            self.state_service.save(params)
            return {
                "status": "SUCCESS",
                "service": "state",
                "saved": params
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "service": "state",
                "error": str(e)
            }


# ============================================================================
# 测试
# ============================================================================

if __name__ == "__main__":
    from services.llm_service import LLMService
    from services.rag_service import RAGService
    from services.eda_service import EDAService
    from services.state_service import StateService

    # 创建服务
    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    # 创建场景
    scene = LLMAgentScene(services)

    # 测试执行
    print("=" * 70)
    print("测试 LLM 规划场景")
    print("=" * 70)

    test_input = "验证模块A的时序是否小于10ns"
    print(f"\n用户输入: {test_input}")

    for message in scene.run(test_input):
        msg_type = message.get("type")
        content = message.get("content")

        if msg_type == "info":
            print(f"\n{content}")
        elif msg_type == "plan":
            print(f"\n生成的执行计划：")
            steps = content.get("steps", [])
            for i, step in enumerate(steps, 1):
                print(f"  {i}. {step}")
        elif msg_type == "step_result":
            step = message.get("step")
            result = message.get("result")
            status = message.get("status")
            icon = "✓" if status == "SUCCESS" else "✗"
            print(f"\n步骤 {step} 结果: {icon}")
            print(f"  {result}")
        elif msg_type == "done":
            print(f"\n{content}")

    print("\n" + "=" * 70)
