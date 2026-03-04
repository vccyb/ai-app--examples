#!/usr/bin/env python3
"""
EDA 工具调用脚本
"""
import sys
import asyncio
sys.path.insert(0, str(__file__).replace('/.claude/skills/eda-skill/scripts/invoke_tool.py', '')))

from tools.eda_tools import get_eda_tool_definitions

# 导出工具定义
if __name__ == '__main__':
    tools = get_eda_tool_definitions()
    for tool in tools:
        print(f"Tool: {tool['name']}")
