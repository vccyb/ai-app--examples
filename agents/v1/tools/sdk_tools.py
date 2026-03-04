"""
Custom Tools for EDA and HimaQA - SDK Compliant

符合 Claude Agent SDK 标准的自定义工具实现
"""
from typing import Any, Dict
from claude_agent_sdk import tool, create_sdk_mcp_server
from storage.project_store import project_store
from storage.result_store import result_store


# EDA Tools
@tool(
    "eda_create_project",
    "创建一个新的EDA电路设计项目",
    {"name": str, "description": str}
)
async def eda_create_project(args: Dict[str, Any]) -> Dict[str, Any]:
    """创建EDA项目"""
    from tools.eda_tools import eda_create_project as impl
    impl_args = {
        "name": args.get("name", ""),
    }
    result = await impl(impl_args)

    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 创建项目: {result.get('project', '')}\n{result.get('message', '')}"
            }
        ]
    }


@tool(
    "eda_add_component",
    "向项目添加电子元件",
    {"project": str, "type": str, "value": str, "name": str}
)
async def eda_add_component(args: Dict[str, Any]) -> Dict[str, Any]:
    """添加电子元件"""
    from tools.eda_tools import eda_add_component as impl
    impl_args = {
        "project": args.get("project", ""),
        "type": args.get("type", ""),
        "name": args.get("name", ""),
        "value": args.get("value", ""),
    }
    result = await impl(impl_args)

    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"✓ 添加元件: {result.get('component', '')} "
                    f"({result.get('type_cn', result.get('type', ''))}) - {result.get('value', '')}\n"
                    f"{result.get('message', '')}"
                )
            }
        ]
    }


@tool(
    "eda_connect",
    "连接两个元件的引脚",
    {"project": str, "from_component": str, "from_pin": str, "to_component": str, "to_pin": str}
)
async def eda_connect(args: Dict[str, Any]) -> Dict[str, Any]:
    """连接元件引脚"""
    from tools.eda_tools import eda_connect as impl
    impl_args = {
        "project": args.get("project", ""),
        "from": f"{args.get('from_component', '')}.{args.get('from_pin', '')}",
        "to": f"{args.get('to_component', '')}.{args.get('to_pin', '')}",
    }
    result = await impl(impl_args)

    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 创建连接: {result.get('connection', '')}\n{result.get('message', '')}"
            }
        ]
    }


@tool(
    "eda_simulate",
    "运行电路仿真分析",
    {"project": str, "type": str}
)
async def eda_simulate(args: Dict[str, Any]) -> Dict[str, Any]:
    """运行电路仿真"""
    from tools.eda_tools import eda_simulate as impl
    impl_args = {
        "project": args.get("project", ""),
        "type": args.get("type", "dc"),
    }
    result = await impl(impl_args)
    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 仿真完成\n{result.get('message', '')}\n{result.get('results', '')}"
            }
        ]
    }


@tool(
    "eda_export",
    "导出项目文件",
    {"project": str, "format": str}
)
async def eda_export(args: Dict[str, Any]) -> Dict[str, Any]:
    """导出项目文件"""
    from tools.eda_tools import eda_export as impl
    impl_args = {
        "project": args.get("project", ""),
        "format": args.get("format", "netlist"),
    }
    result = await impl(impl_args)

    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 导出{str(result.get('format', '')).upper()}: {result.get('file', '')}\n{result.get('message', '')}"
            }
        ]
    }


# HimaQA Tools
@tool(
    "himaqa_upload_netlist",
    "上传网表文件到HimaQA平台",
    {"project": str, "netlist_file": str}
)
async def himaqa_upload_netlist(args: Dict[str, Any]) -> Dict[str, Any]:
    """上传网表到平台"""
    from tools.himaqa_tools import himaqa_upload_netlist as impl
    impl_args = {
        "project": args.get("project", ""),
        "netlist_file": args.get("netlist_file", ""),
    }
    result = await impl(impl_args)

    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 上传网表成功\n{result.get('message', '')}\n上传ID: {result.get('upload_id', '')}"
            }
        ]
    }


@tool(
    "himaqa_notify_manager",
    "通知测试经理有新的网表待测试",
    {"project": str, "manager": str, "message": str}
)
async def himaqa_notify_manager(args: Dict[str, Any]) -> Dict[str, Any]:
    """通知测试经理"""
    from tools.himaqa_tools import himaqa_notify_manager as impl
    impl_args = {
        "project": args.get("project", ""),
        "manager": args.get("manager", "测试经理"),
        "message": args.get("message", ""),
    }
    result = await impl(impl_args)

    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 已通知测试经理\n{result.get('message', '')}\n通知ID: {result.get('notification_id', '')}"
            }
        ]
    }


@tool(
    "himaqa_query_history",
    "查询历史网表和测试记录",
    {"project": str, "limit": int}
)
async def himaqa_query_history(args: Dict[str, Any]) -> Dict[str, Any]:
    """查询历史记录"""
    from tools.himaqa_tools import himaqa_query_history as impl
    impl_args = {
        "project": args.get("project", ""),
        "limit": args.get("limit", 10),
    }
    result = await impl(impl_args)

    history_summary = "\n".join([
        f"  - {item.get('upload_id', '')}: {item.get('project', '')} ({item.get('status', '')})"
        for item in result.get("history", [])
    ])
    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 历史记录\n{result.get('message', '')}\n{history_summary}"
            }
        ]
    }


@tool(
    "himaqa_get_report",
    "获取测试报告",
    {"upload_id": str}
)
async def himaqa_get_report(args: Dict[str, Any]) -> Dict[str, Any]:
    """获取测试报告"""
    from tools.himaqa_tools import himaqa_get_report as impl
    impl_args = {
        "upload_id": args.get("upload_id", ""),
    }
    result = await impl(impl_args)

    return {
        "content": [
            {
                "type": "text",
                "text": f"✓ 测试报告\n{result.get('message', '')}\n{result.get('report', {}).get('summary', {})}"
            }
        ]
    }


# Create MCP Servers
eda_tools_server = create_sdk_mcp_server(
    name="eda-tools",
    version="1.0.0",
    tools=[
        eda_create_project,
        eda_add_component,
        eda_connect,
        eda_simulate,
        eda_export,
    ]
)

himaqa_tools_server = create_sdk_mcp_server(
    name="himaqa-tools",
    version="1.0.0",
    tools=[
        himaqa_upload_netlist,
        himaqa_notify_manager,
        himaqa_query_history,
        himaqa_get_report,
    ]
)

__all__ = ["eda_tools_server", "himaqa_tools_server"]
