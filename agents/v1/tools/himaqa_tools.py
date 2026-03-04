"""
HimaQA 平台工具（模拟实现）

提供网表管理、测试流程等功能的模拟实现
"""
from typing import Dict, List
from datetime import datetime
import json


def tool(name: str, description: str, schema: Dict):
    """工具装饰器"""
    def decorator(func):
        func._tool_name = name
        func._tool_description = description
        func._tool_schema = schema
        return func
    return decorator


@tool(
    "himaqa_upload_netlist",
    "上传网表文件到 HimaQA 平台。将 EDA 导出的网表文件上传到测试平台。",
    {"project": str, "netlist_file": str}
)
async def himaqa_upload_netlist(args: Dict) -> Dict:
    """
    上传网表到平台（模拟）

    Args:
        project: 项目名称
        netlist_file: 网表文件路径

    Returns:
        上传结果
    """
    project = args['project']
    netlist_file = args['netlist_file']

    # 模拟上传
    upload_id = f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "status": "success",
        "message": f"网表文件已上传到 HimaQA 平台",
        "upload_id": upload_id,
        "project": project,
        "file": netlist_file,
        "platform": "HimaQA",
        "uploaded_at": datetime.now().isoformat()
    }


@tool(
    "himaqa_notify_manager",
    "通知测试经理有新的网表需要测试。发送通知给指定的测试经理。",
    {"project": str, "manager": str, "message": str}
)
async def himaqa_notify_manager(args: Dict) -> Dict:
    """
    通知测试经理（模拟）

    Args:
        project: 项目名称
        manager: 测试经理姓名
        message: 通知消息

    Returns:
        通知结果
    """
    project = args['project']
    manager = args.get('manager', '测试经理')
    message = args.get('message', f'项目 {project} 的网表已上传，请安排测试。')

    # 模拟通知
    notification_id = f"notif_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "status": "success",
        "message": f"已通知测试经理 {manager}",
        "notification_id": notification_id,
        "project": project,
        "manager": manager,
        "notified_at": datetime.now().isoformat()
    }


@tool(
    "himaqa_query_history",
    "查询 HimaQA 平台上的历史网表记录。获取用户之前提交的网表历史和状态。",
    {"project": str, "limit": int}
)
async def himaqa_query_history(args: Dict) -> Dict:
    """
    查询历史记录（模拟）

    Args:
        project: 项目名称（可选）
        limit: 返回记录数量限制

    Returns:
        历史记录列表
    """
    project = args.get('project', '')
    limit = args.get('limit', 10)

    # 模拟历史数据
    mock_history = [
        {
            "upload_id": "upload_20260301120000",
            "project": "led_circuit_v1",
            "file": "led_circuit_v1.net",
            "status": "completed",
            "uploaded_at": "2026-03-01T12:00:00"
        },
        {
            "upload_id": "upload_20260302150000",
            "project": "amplifier_design",
            "file": "amplifier.net",
            "status": "testing",
            "uploaded_at": "2026-03-02T15:00:00"
        },
        {
            "upload_id": "upload_20260303100000",
            "project": "led_circuit_v2",
            "file": "led_circuit_v2.net",
            "status": "pending",
            "uploaded_at": "2026-03-03T10:00:00"
        }
    ]

    # 如果指定了项目，过滤结果
    if project:
        filtered = [h for h in mock_history if h['project'] == project]
    else:
        filtered = mock_history

    # 应用限制
    results = filtered[:limit]

    return {
        "status": "success",
        "message": f"找到 {len(results)} 条历史记录",
        "count": len(results),
        "history": results
    }


@tool(
    "himaqa_get_report",
    "获取网表的测试报告。从 HimaQA 平台下载指定网表的测试结果报告。",
    {"upload_id": str}
)
async def himaqa_get_report(args: Dict) -> Dict:
    """
    获取测试报告（模拟）

    Args:
        upload_id: 上传ID

    Returns:
        测试报告
    """
    upload_id = args['upload_id']

    # 模拟测试报告
    mock_report = {
        "upload_id": upload_id,
        "test_status": "passed",
        "test_date": datetime.now().isoformat(),
        "summary": {
            "total_tests": 15,
            "passed": 14,
            "failed": 1,
            "warnings": 2
        },
        "details": [
            {
                "test_name": "电气规则检查",
                "status": "passed",
                "duration": "0.5s"
            },
            {
                "test_name": "网表语法验证",
                "status": "passed",
                "duration": "0.3s"
            },
            {
                "test_name": "设计规则检查",
                "status": "passed",
                "duration": "1.2s"
            }
        ],
        "report_file": f"report_{upload_id}.pdf"
    }

    return {
        "status": "success",
        "message": f"已获取测试报告",
        "report": mock_report
    }


def get_himaqa_tool_definitions() -> List[Dict]:
    """获取所有 HimaQA 工具定义"""
    tools = [
        himaqa_upload_netlist,
        himaqa_notify_manager,
        himaqa_query_history,
        himaqa_get_report
    ]

    tool_definitions = []
    for tool_func in tools:
        schema = tool_func._tool_schema

        properties = {}
        required = []
        for param_name, _ in schema.items():
            properties[param_name] = {
                "type": "string",
                "description": f"{param_name} 参数"
            }
            required.append(param_name)

        tool_definitions.append({
            "name": tool_func._tool_name,
            "description": tool_func._tool_description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        })

    return tool_definitions
