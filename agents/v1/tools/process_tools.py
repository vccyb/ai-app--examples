"""
进程管理工具

使用 asyncio.subprocess 创建真实的子进程
简化版本：不涉及 EDA 工具，演示基本的进程管理功能
"""
import asyncio
from typing import Dict, List

# 进程注册表（存储所有活动进程）
_process_registry: Dict[str, asyncio.subprocess.Process] = {}


# 简化的工具装饰器（替代 claude-agent-sdk 的 @tool）
def tool(name: str, description: str, schema: Dict):
    """
    工具装饰器（简化版本）

    Args:
        name: 工具名称
        description: 工具描述
        schema: 参数 schema
    """
    def decorator(func):
        func._tool_name = name
        func._tool_description = description
        func._tool_schema = schema
        return func
    return decorator


def get_tool_definitions() -> List[Dict]:
    """
    获取所有工具的定义（用于 Anthropic API）

    Returns:
        工具定义列表，格式符合 Anthropic API 要求
    """
    tools = [
        start_process,
        stop_process,
        list_processes,
        get_process_status
    ]

    tool_definitions = []
    for tool_func in tools:
        schema = tool_func._tool_schema

        # 转换参数格式为 Anthropic API 格式
        properties = {}
        required = []
        for param_name, param_type in schema.items():
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


@tool(
    "start_process",
    "启动一个新的子进程。支持任意命令行工具，如 sleep、python、cat 等。",
    {
        "name": str,
        "command": str,
        "working_dir": str
    }
)
async def start_process(args: Dict) -> Dict:
    """
    启动新的子进程

    示例:
    - 启动 sleep 进程: name="sleep1", command="sleep 60", working_dir="/tmp"
    - 启动 Python 脚本: name="script1", command="python script.py", working_dir="/home/user"

    Args:
        name: 进程的唯一标识符
        command: 要执行的命令
        working_dir: 工作目录

    Returns:
        包含状态和进程信息的字典
    """
    name = args['name']
    command = args['command']
    working_dir = args['working_dir']

    # 检查进程是否已存在
    if name in _process_registry:
        return {
            "status": "error",
            "error": f"进程 '{name}' 已存在"
        }

    try:
        # 使用 asyncio.subprocess 创建进程
        process = await asyncio.create_subprocess_shell(
            command,
            cwd=working_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 注册进程
        _process_registry[name] = process

        return {
            "status": "success",
            "message": f"进程 '{name}' 启动成功",
            "process_name": name,
            "pid": process.pid,
            "working_dir": working_dir,
            "command": command
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "process_name": name
        }


@tool(
    "stop_process",
    "停止一个正在运行的进程",
    {
        "name": str
    }
)
async def stop_process(args: Dict) -> Dict:
    """
    停止指定进程

    Args:
        name: 要停止的进程名称

    Returns:
        包含状态信息的字典
    """
    name = args['name']

    if name not in _process_registry:
        return {
            "status": "error",
            "error": f"进程 '{name}' 不存在"
        }

    try:
        process = _process_registry[name]

        # 优雅终止
        process.terminate()

        # 等待进程结束（最多 5 秒）
        try:
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            # 如果优雅终止失败，强制杀死
            process.kill()
            await process.wait()

        # 从注册表中移除
        del _process_registry[name]

        return {
            "status": "success",
            "message": f"进程 '{name}' 已停止"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "process_name": name
        }


@tool(
    "list_processes",
    "列出所有管理的进程及其状态",
    {}
)
async def list_processes(args: Dict) -> Dict:
    """
    列出所有进程

    Returns:
        包含所有进程信息的字典
    """
    processes = []
    for name, process in _process_registry.items():
        processes.append({
            "name": name,
            "pid": process.pid,
            "status": "running" if process.returncode is None else "exited"
        })

    return {
        "status": "success",
        "processes": processes,
        "total": len(processes)
    }


@tool(
    "get_process_status",
    "获取指定进程的详细状态",
    {
        "name": str
    }
)
async def get_process_status(args: Dict) -> Dict:
    """
    获取进程状态

    Args:
        name: 进程名称

    Returns:
        包含详细进程状态的字典
    """
    name = args['name']

    if name not in _process_registry:
        return {
            "status": "error",
            "error": f"进程 '{name}' 不存在"
        }

    process = _process_registry[name]

    return {
        "status": "success",
        "process": {
            "name": name,
            "pid": process.pid,
            "running": process.returncode is None,
            "returncode": process.returncode
        }
    }
