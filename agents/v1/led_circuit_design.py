#!/usr/bin/env python3
"""
LED电路设计并提交测试的自动化脚本
"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from tools.eda_tools import (
    eda_create_project,
    eda_add_component,
    eda_connect,
    eda_simulate,
    eda_export
)
from tools.himaqa_tools import (
    himaqa_upload_netlist,
    himaqa_notify_manager
)


async def main():
    """主流程"""
    print("=" * 70)
    print("LED电路设计与测试提交流程")
    print("=" * 70)

    # Step 1: 创建EDA项目
    print("\n📋 步骤1: 创建EDA项目")
    project_args = {
        'name': 'LED电路',
        'description': '一个简单的LED照明电路，包含LED、限流电阻和5V直流电源'
    }
    project_result = await eda_create_project(project_args)
    print(f"✓ {project_result['message']}")
    project_name = project_result['project']

    # Step 2: 添加元件
    print("\n📦 步骤2: 添加电子元件")

    # 添加LED
    led_result = await eda_add_component({
        'project': project_name,
        'type': 'LED',
        'name': 'D1',
        'value': 'red'
    })
    print(f"✓ {led_result['message']}")

    # 添加限流电阻
    resistor_result = await eda_add_component({
        'project': project_name,
        'type': 'resistor',
        'name': 'R1',
        'value': '330Ω'
    })
    print(f"✓ {resistor_result['message']}")

    # 添加5V电源
    vcc_result = await eda_add_component({
        'project': project_name,
        'type': 'voltage_source',
        'name': 'V1',
        'value': '5V'
    })
    print(f"✓ {vcc_result['message']}")

    # 添加开关
    switch_result = await eda_add_component({
        'project': project_name,
        'type': 'switch',
        'name': 'S1',
        'value': ''
    })
    print(f"✓ {switch_result['message']}")

    # Step 3: 连接电路
    print("\n🔌 步骤3: 连接电路")

    # V1正极 -> S1
    conn1 = await eda_connect({
        'project': project_name,
        'from': 'V1.1',
        'to': 'S1.1'
    })
    print(f"✓ {conn1['message']}")

    # S1 -> R1
    conn2 = await eda_connect({
        'project': project_name,
        'from': 'S1.2',
        'to': 'R1.1'
    })
    print(f"✓ {conn2['message']}")

    # R1 -> D1阳极
    conn3 = await eda_connect({
        'project': project_name,
        'from': 'R1.2',
        'to': 'D1.1'
    })
    print(f"✓ {conn3['message']}")

    # D1阴极 -> V1负极
    conn4 = await eda_connect({
        'project': project_name,
        'from': 'D1.2',
        'to': 'V1.2'
    })
    print(f"✓ {conn4['message']}")

    # Step 4: 运行仿真
    print("\n⚡ 步骤4: 运行电路仿真")
    sim_result = await eda_simulate({
        'project': project_name,
        'type': 'dc'
    })
    print(f"✓ {sim_result['message']}")

    # Step 5: 导出网表
    print("\n📄 步骤5: 导出网表文件")
    export_result = await eda_export({
        'project': project_name,
        'format': 'netlist',
        'output_path': f'./workspace/{project_name}/export/{project_name}.net'
    })
    print(f"✓ {export_result['message']}")
    netlist_file = export_result['file']

    # Step 6: 上传网表到HimaQA平台
    print("\n📤 步骤6: 上传网表到HimaQA平台")
    upload_result = await himaqa_upload_netlist({
        'project': project_name,
        'netlist_file': netlist_file
    })
    print(f"✓ {upload_result['message']}")
    upload_id = upload_result['upload_id']

    # Step 7: 通知张经理
    print("\n📧 步骤7: 通知张经理进行测试")
    notify_result = await himaqa_notify_manager({
        'project': project_name,
        'manager': '张经理',
        'message': f'项目 {project_name} 的网表已上传，请安排测试。'
    })
    print(f"✓ {notify_result['message']}")

    # 总结
    print("\n" + "=" * 70)
    print("✅ LED电路设计完成并已提交给张经理测试")
    print("=" * 70)
    print(f"项目名称: {project_name}")
    print(f"上传ID: {upload_id}")
    print(f"通知状态: 已发送给张经理")
    print(f"电路元件: LED(D1), 电阻(R1:330Ω), 电源(V1:5V), 开关(S1)")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
