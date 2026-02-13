"""Controller - 交互控制器

负责：
- 场景执行流程控制
- 处理用户交互（确认、输入、迭代）
- 消息显示和格式化
"""
from typing import Dict, Optional, Generator


class Controller:
    """交互控制器

    协调场景执行和用户交互
    """

    def __init__(self, input_func=None, output_func=None):
        """初始化控制器

        Args:
            input_func: 输入函数（用于测试），默认使用 input
            output_func: 输出函数（用于测试），默认使用 print
        """
        self.input_func = input_func or input
        self.output_func = output_func or print

    def execute_scene(
        self,
        scene_generator: Generator[Dict, None, None],
        auto_confirm: bool = False
    ) -> Dict:
        """执行场景并处理交互

        Args:
            scene_generator: 场景生成器（yield 消息字典）
            auto_confirm: 是否自动确认（用于测试）

        Returns:
            场景执行的最终结果
        """
        result = {"status": "UNKNOWN"}

        try:
            while True:
                # 获取下一个消息
                message = next(scene_generator)

                # 处理不同类型的消息
                msg_type = message.get("type")

                if msg_type == "info":
                    self._handle_info_message(message)

                elif msg_type == "plan":
                    should_continue = self._handle_plan_message(message, auto_confirm)
                    if not should_continue:
                        result = {"status": "CANCELED", "reason": "用户取消执行"}
                        break

                elif msg_type == "step_result":
                    self._handle_step_result_message(message)

                elif msg_type == "ask":
                    response = self._handle_ask_message(message, auto_confirm)
                    # 将响应发送回场景
                    # 这里需要场景能够接收响应，简化版本暂时跳过
                    scene_generator.send(response)

                elif msg_type == "done":
                    result = self._handle_done_message(message)
                    break

                elif msg_type == "error":
                    result = self._handle_error_message(message)
                    break

        except StopIteration:
            # 场景正常结束
            pass
        except Exception as e:
            result = {
                "status": "ERROR",
                "message": f"执行出错：{str(e)}"
            }
            self.output_func(f"\n[错误] {str(e)}")

        return result

    # ========================================================================
    # 消息处理方法
    # ========================================================================

    def _handle_info_message(self, message: Dict) -> None:
        """处理信息消息"""
        content = message.get("content", "")
        self.output_func(f"\n{content}")

    def _handle_plan_message(self, message: Dict, auto_confirm: bool) -> bool:
        """处理计划消息

        Returns:
            是否继续执行
        """
        content = message.get("content", {})
        steps = content.get("steps", [])
        need_confirm = content.get("need_confirm", True)

        # 显示计划
        self.output_func("\n生成的执行计划：")
        for step in steps:
            step_num = step.get("step", "?")
            action = step.get("action", "")
            description = step.get("description", "")
            self.output_func(f"  {step_num}. {action}: {description}")

        # 如果需要确认
        if need_confirm and not auto_confirm:
            self.output_func("\n系统: 确认执行以上计划？(y/n/修改)")
            user_input = self.input_func("你： ").strip().lower()

            if user_input in ['n', 'no', '否']:
                return False
            elif user_input not in ['y', 'yes', '是', '']:
                self.output_func("检测到输入'修改'，暂不支持该功能，使用默认计划")

        return True

    def _handle_step_result_message(self, message: Dict) -> None:
        """处理步骤结果消息"""
        step = message.get("step", "?")
        result = message.get("result", {})
        status = message.get("status", "SUCCESS")

        status_icon = "✓" if status == "SUCCESS" else "✗"
        self.output_func(f"\n[执行] 步骤{step}: {status_icon}")

        # 格式化显示结果
        if isinstance(result, dict):
            for key, value in result.items():
                self.output_func(f"  {key}: {value}")
        else:
            self.output_func(f"  结果: {result}")

    def _handle_ask_message(self, message: Dict, auto_confirm: bool = False) -> str:
        """处理询问消息

        Args:
            message: 消息字典
            auto_confirm: 是否自动确认

        Returns:
            用户响应
        """
        content = message.get("content", {})
        question = content.get("question", "")
        options = content.get("options", [])

        # 显示问题
        self.output_func(f"\n系统: {question}")

        if options:
            self.output_func(f"选项: {', '.join(options)}")

        # 如果自动确认，返回第一个选项或默认值
        if auto_confirm:
            if options:
                self.output_func(f"[自动确认] 选择: {options[0]}")
                return options[0]
            else:
                self.output_func("[自动确认] 跳过")
                return ""

        # 获取用户输入
        user_input = self.input_func("你： ").strip()
        return user_input

    def _handle_done_message(self, message: Dict) -> Dict:
        """处理完成消息"""
        summary = message.get("content", {})
        scene_name = message.get("scene", "unknown")

        self.output_func(f"\n系统: {scene_name} 执行完成！")

        # 显示总结
        if summary:
            self.output_func("总结：")
            if isinstance(summary, dict):
                for key, value in summary.items():
                    self.output_func(f"  {key}: {value}")
            else:
                self.output_func(f"  {summary}")

        return {
            "status": "DONE",
            "scene": scene_name,
            "summary": summary
        }

    def _handle_error_message(self, message: Dict) -> Dict:
        """处理错误消息"""
        error_msg = message.get("content", "未知错误")
        scene_name = message.get("scene", "unknown")

        self.output_func(f"\n[错误] {scene_name}: {error_msg}")

        return {
            "status": "ERROR",
            "scene": scene_name,
            "message": error_msg
        }


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Controller 测试")
    print("=" * 70)

    # 创建一个测试场景生成器
    def test_scene():
        """测试场景生成器"""
        yield {
            "type": "info",
            "content": "开始执行测试场景"
        }

        yield {
            "type": "plan",
            "content": {
                "steps": [
                    {"step": 1, "action": "步骤A", "description": "描述A"},
                    {"step": 2, "action": "步骤B", "description": "描述B"}
                ],
                "need_confirm": True
            }
        }

        yield {
            "type": "step_result",
            "step": 1,
            "result": {"key": "value"},
            "status": "SUCCESS"
        }

        yield {
            "type": "done",
            "content": {"result": "success"}
        }

    # 创建控制器
    controller = Controller()

    # 测试执行（自动确认模式）
    print("\n测试1：执行场景（自动确认）")
    result = controller.execute_scene(test_scene(), auto_confirm=True)
    print(f"\n最终结果: {result}")

    print("\n测试完成")
