"""Real LLM Planning Scene - English version to avoid encoding issues"""
from typing import Dict, Generator
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scenes.base import BaseScene


class TrueLLMPlanScene(BaseScene):
    """Real LLM Planning Scene

    LLM is responsible for:
    1. Analyze user task
    2. Generate execution plan with steps
    3. Scene executes steps by calling services
    """

    def __init__(self, services: Dict):
        super().__init__(
            name="llm_plan",
            description="LLM Planning Scene - LLM generates execution plan",
            keywords=[],
            services=services
        )

    def match(self, user_input: str) -> float:
        return 0.0

    def run(self, user_input: str) -> Generator[Dict, None, None]:
        yield self._create_info_message(f"\n[{self.name.upper()}] Scene Started")
        yield self._create_info_message(f"User Input: {user_input}")

        if self.llm_service:
            yield self._create_info_message("LLM Service Available")

            # Step 1: Generate execution plan
            yield self._create_info_message(f"[{self.name}] Generating Execution Plan...")

            plan = self._llm_generate_plan(user_input)

            if not plan:
                yield self._create_error_message("Failed to generate execution plan")
                return

            steps = plan.get("steps", [])
            reasoning = plan.get("reasoning", "")

            yield self._create_plan_message(steps, need_confirm=True)

            if reasoning:
                yield self._create_info_message(f"LLM Analysis: {reasoning}")

            # Step 2: Execute plan
            yield self._create_info_message(f"\n[{self.name}] Executing Plan ({len(steps)} steps)...")

            results = []
            for i, step in enumerate(steps, 1):
                yield self._create_info_message(f"\nStep {i}/{len(steps)}")
                result = yield from self._execute_step(step)
                results.append(result)

                status = result.get("status", "UNKNOWN")
                yield self._create_step_result_message(
                    step=i,
                    result=result,
                    status=status
                )

            # Step 3: Done
            yield self._create_done_message({
                "summary": f"Execution completed, {len(results)} steps",
                "results": results
            })

    def _llm_generate_plan(self, user_input: str) -> Dict:
        """Generate execution plan using LLM"""
        if not self.llm_service:
            return None

        # Use string concatenation to avoid f-string brace escaping issues
        prompt = """You are an EDA (Electronic Design Automation) expert.

User task: """ + user_input + """

Please analyze this task and generate detailed execution steps.

Available Services:
1. rag_service - Query knowledge base, get module specs
   - Method: get_specification(module)
   - Parameter: module (module name, e.g., "ModuleA")

2. eda_service - Run simulation, get actual metrics
   - Method: simulate(module, parameters)
   - Parameter: module (module name)
   - Parameter: parameters (simulation parameters)
   - Returns: actual metrics (timing, power, area)

3. state_service - Save data and results
   - Method: save(data)
   - Parameter: data (any data to save)

Please generate execution plan in JSON format:
{
  "reasoning": "Your analysis process, why these steps are needed",
  "steps": [
    {"action": "action name", "service": "service_name", "params": {"param": "value"}}
  ]
}

Requirements:
1. Each step must have 'action' field
2. If step calls service, must have 'service' and 'params' fields
3. Steps should be logical and clear
4. Return ONLY JSON, no other content"""

        messages = [{"role": "user", "content": prompt}]

        try:
            response = self.llm_service.chat(messages, temperature=0.5)
            response_text = self.llm_service._extract_response_text(response)

            import json
            plan = json.loads(response_text)

            # Validate plan format
            if "steps" in plan and isinstance(plan.get("steps"), list):
                return plan
            else:
                print(f"[{self.name}] LLM returned invalid format: {response_text[:200]}...")
                return None

        except Exception as e:
            print(f"[{self.name}] LLM plan generation failed: {str(e)}")
            return None

    def _execute_step(self, step: Dict) -> Generator:
        """Execute a single step"""
        action = step.get("action", "")
        service_name = step.get("service", "")
        params = step.get("params", {})

        yield self._create_info_message(f"  Action: {action}")

        # Route to appropriate service
        if service_name == "rag_service" and self.rag_service:
            result = yield from self._call_rag_service(params)
        elif service_name == "eda_service" and self.eda_service:
            result = yield from self._call_eda_service(params)
        elif service_name == "state_service" and self.state_service:
            result = yield from self._call_state_service(params)
        else:
            # No service specified, return success
            result = {"status": "SUCCESS", "message": f"Completed: {action}"}

        yield self._create_info_message(f"  Result: {result}")

        return result

    def _call_rag_service(self, params: Dict) -> Generator:
        """Call RAG service"""
        try:
            module = params.get("module")
            spec = self.rag_service.get_specification(module)
            yield self._create_info_message(f"  Specification for {module}: {spec}")
            yield self._create_step_result_message(
                step="RAG",
                result=spec,
                status="SUCCESS"
            )
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

    def _call_eda_service(self, params: Dict) -> Generator:
        """Call EDA service"""
        try:
            module = params.get("module")
            parameters = params.get("parameters", {})

            yield self._create_info_message(f"  Simulating {module}...")

            sim_result = self.eda_service.simulate(module, parameters)
            yield self._create_info_message(f"  Result: {sim_result}")

            yield self._create_step_result_message(
                step="EDA",
                result=sim_result,
                status="SUCCESS"
            )
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

    def _call_state_service(self, params: Dict) -> Generator:
        """Call State service"""
        try:
            yield self._create_info_message(f"  Saving data...")
            self.state_service.save(params)
            yield self._create_info_message(f"  Data saved")

            yield self._create_step_result_message(
                step="State",
                result=params,
                status="SUCCESS"
            )
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


# Test
if __name__ == "__main__":
    from services.llm_service import LLMService
    from services.rag_service import RAGService
    from services.eda_service import EDAService
    from services.state_service import StateService

    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    scene = TrueLLMPlanScene(services)

    print("=" * 70)
    print("Test Real LLM Plan Scene")
    print("=" * 70)

    for msg in scene.run("Verify if Module A timing is less than 10ns"):
        msg_type = msg.get("type")
        content = msg.get("content")

        if msg_type == "info":
            print(f"\n{content}")
        elif msg_type == "plan":
            print(f"\nGenerated Execution Plan:")
            steps = content.get("steps", [])
            for i, step in enumerate(steps, 1):
                print(f"  {i}. {step}")
        elif msg_type == "step_result":
            step = msg.get("step")
            result = msg.get("result")
            status = msg.get("status")
            icon = "OK" if status == "SUCCESS" else "FAIL"
            print(f"\nStep {step} Result: {icon}")
            print(f"  {result}")
        elif msg_type == "done":
            print(f"\n{content}")
