"""Test True LLM Plan Scene"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scenes.true_llm_plan_scene import TrueLLMPlanScene
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.eda_service import EDAService
from services.state_service import StateService


def test():
    print("=" * 70)
    print("Test True LLM Plan Scene")
    print("=" * 70)

    # Create services
    services = {}
    services["llm"] = LLMService(client_type="mock")
    services["rag"] = RAGService()
    services["eda"] = EDAService()
    services["state"] = StateService()

    # Create scene
    scene = TrueLLMPlanScene(services)

    # Test cases
    test_cases = [
        "Verify if Module A timing is less than 10ns",
        "Query Module B design specifications",
        "Optimize Module C power consumption"
    ]

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}/{len(test_cases)}: {test_input}")
        print("=" * 70)

        for msg in scene.run(test_input):
            msg_type = msg.get("type")
            content = msg.get("content")

            if msg_type == "info":
                print("\n" + content)
            elif msg_type == "plan":
                print("\nGenerated Execution Plan:")
                steps = content.get("steps", [])
                for j, step in enumerate(steps, 1):
                    print("  " + str(j) + ". " + step.get("action", ""))
                    if "params" in step:
                        print("     Params: " + str(step.get("params", {})))
            elif msg_type == "step_result":
                step_num = msg.get("step", "?")
                result = msg.get("result", {})
                status = msg.get("status", "")
                icon = "OK" if status == "SUCCESS" else "FAIL"
                print("\n  Step " + str(step_num) + " Result: " + icon)
                print("  " + str(result))
            elif msg_type == "done":
                content_dict = msg.get("content", {})
                summary = content_dict.get("summary", "Done")
                print("\n" + summary)

        print("\n" + "=" * 70)


if __name__ == "__main__":
    test()
