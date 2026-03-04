"""
EDA 工具 - 模拟 Innovas 进程命令

这些工具模拟 EDA 工具（如 Innovas）的命令行接口，
通过简单的命令操作来完成电路设计任务。

所有工具执行结果都会持久化保存。
"""
from typing import Dict, List
from datetime import datetime

# 导入持久化存储
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from storage.project_store import project_store
from storage.result_store import result_store

# 模拟的 EDA 项目存储（内存缓存）
_projects: Dict[str, Dict] = {}
_components: List[Dict] = []
_connections: List[Dict] = []


def tool(name: str, description: str, schema: Dict):
    """工具装饰器"""
    def decorator(func):
        func._tool_name = name
        func._tool_description = description
        func._tool_schema = schema
        return func
    return decorator


@tool(
    "eda_create_project",
    "创建新的 EDA 设计项目。初始化项目目录和配置文件。",
    {"name": str}
)
async def eda_create_project(args: Dict) -> Dict:
    """创建项目"""
    name = args['name']

    if name in _projects:
        return {
            "status": "error",
            "error": f"项目 '{name}' 已存在"
        }

    project = {
        "project_id": name,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "components": [],
        "connections": [],
        "simulations": []
    }
    _projects[name] = project

    # 持久化项目数据
    project_store.save_project(project)

    result = {
        "status": "success",
        "message": f"项目 '{name}' 已创建",
        "project": name,
        "project_id": name,
        "path": f"./workspace/{name}"
    }

    # 持久化工具执行结果
    result_store.save_result(
        tool_name="eda_create_project",
        inputs=args,
        outputs=result,
        project_id=name
    )

    return result


@tool(
    "eda_add_component",
    "向项目添加元件。支持电阻、电容、电感、二极管、晶体管、LED、电源等。",
    {
        "project": str,
        "type": str,
        "name": str,
        "value": str
    }
)
async def eda_add_component(args: Dict) -> Dict:
    """添加元件"""
    project = args['project']
    comp_type = args['type'].lower()
    name = args['name']
    value = args.get('value', '')

    if project not in _projects:
        return {
            "status": "error",
            "error": f"项目 '{project}' 不存在"
        }

    # 检查元件名是否已存在
    for comp in _components:
        if comp.get('project') == project and comp.get('name') == name:
            return {
                "status": "error",
                "error": f"元件 '{name}' 在项目 '{project}' 中已存在"
            }

    component = {
        "project": project,
        "type": comp_type,
        "name": name,
        "value": value,
        "pins": _get_pin_count(comp_type)
    }
    _components.append(component)
    _projects[project]['components'].append(component)

    # 持久化项目数据
    project_store.save_project(_projects[project])

    type_names = {
        "resistor": "电阻", "capacitor": "电容", "inductor": "电感",
        "diode": "二极管", "led": "LED", "npn": "NPN晶体管",
        "pnp": "PNP晶体管", "vcc": "VCC", "gnd": "GND",
        "voltage_source": "电压源"
    }

    result = {
        "status": "success",
        "message": f"已添加 {type_names.get(comp_type, comp_type)} {name}",
        "component": name,
        "type": comp_type,
        "type_cn": type_names.get(comp_type, comp_type),
        "value": value,
        "pins": component['pins'],
        "project": project
    }

    # 持久化工具执行结果
    result_store.save_result(
        tool_name="eda_add_component",
        inputs=args,
        outputs=result,
        project_id=project
    )

    return result


@tool(
    "eda_connect",
    "连接两个元件的引脚。建立电气连接。",
    {
        "project": str,
        "from": str,
        "to": str
    }
)
async def eda_connect(args: Dict) -> Dict:
    """连接引脚"""
    project = args['project']
    from_pin = args['from']
    to_pin = args['to']

    if project not in _projects:
        return {
            "status": "error",
            "error": f"项目 '{project}' 不存在"
        }

    # 解析引脚连接
    connection = {
        "project": project,
        "from": from_pin,
        "to": to_pin
    }
    _connections.append(connection)
    _projects[project]['connections'].append(connection)

    # 持久化项目数据
    project_store.save_project(_projects[project])

    result = {
        "status": "success",
        "message": f"{from_pin} → {to_pin}",
        "connection": f"{from_pin} → {to_pin}"
    }

    # 持久化工具执行结果
    result_store.save_result(
        tool_name="eda_connect",
        inputs=args,
        outputs=result,
        project_id=project
    )

    return result


@tool(
    "eda_simulate",
    "运行电路仿真。执行直流分析、交流分析或瞬态分析。",
    {
        "project": str,
        "type": str
    }
)
async def eda_simulate(args: Dict) -> Dict:
    """运行仿真"""
    project = args['project']
    sim_type = args.get('type', 'dc').lower()

    if project not in _projects:
        return {
            "status": "error",
            "error": f"项目 '{project}' 不存在"
        }

    # 模拟仿真结果
    sim_results = {
        "dc": "直流工作点分析完成",
        "ac": "交流频率分析完成 (1Hz - 1MHz)",
        "tran": "瞬态分析完成 (0 - 10ms)"
    }

    result = {
        "status": "success",
        "message": sim_results.get(sim_type, "仿真完成"),
        "project": project,
        "type": sim_type,
        "results": f"仿真结果已保存到 {project}/simulation/{sim_type}.txt"
    }
    _projects[project]['simulations'].append(result)

    # 持久化项目数据
    project_store.save_project(_projects[project])

    # 持久化工具执行结果
    result_store.save_result(
        tool_name="eda_simulate",
        inputs=args,
        outputs=result,
        project_id=project
    )

    return result


@tool(
    "eda_export",
    "导出设计文件。支持网表、BOM、PCB 等格式。",
    {
        "project": str,
        "format": str
    }
)
async def eda_export(args: Dict) -> Dict:
    """导出文件"""
    project = args['project']
    fmt = args.get('format', 'netlist').lower()

    if project not in _projects:
        return {
            "status": "error",
            "error": f"项目 '{project}' 不存在"
        }

    format_names = {
        "netlist": "SPICE 网表",
        "bom": "物料清单",
        "pcb": "PCB 设计文件"
    }

    result = {
        "status": "success",
        "message": f"{format_names.get(fmt, fmt)} 已导出",
        "project": project,
        "format": fmt,
        "file": f"{project}/export/{project}.{fmt}"
    }

    # 持久化工具执行结果
    result_store.save_result(
        tool_name="eda_export",
        inputs=args,
        outputs=result,
        project_id=project
    )

    return result


def _get_pin_count(comp_type: str) -> int:
    """获取元件引脚数"""
    pins = {
        "resistor": 2, "capacitor": 2, "inductor": 2,
        "diode": 2, "led": 2,
        "npn": 3, "pnp": 3,  # B, C, E
        "vcc": 1, "gnd": 1,
        "voltage_source": 2
    }
    return pins.get(comp_type, 2)


def get_eda_tool_definitions() -> List[Dict]:
    """获取所有 EDA 工具定义"""
    tools = [
        eda_create_project,
        eda_add_component,
        eda_connect,
        eda_simulate,
        eda_export
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
