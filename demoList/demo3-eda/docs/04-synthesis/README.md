# 04 - 综合阶段 (Synthesis)

## 阶段目标

将RTL代码转换为门级网表 (Gate-level Netlist)，映射到目标工艺库，优化面积、时序、功耗。

## 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| RTL代码 | 验证通过 | 功能正确的设计 |
| **工艺库** | 晶圆厂 | .lib / .db格式 |
| **约束文件** | 设计规格 | SDC格式 |
| **UPF文件** | (可选) | 电源管理规范 |

## 关键输出件

| 输出文件 | 说明 | 位置 |
|----------|------|------|
| **门级网表** | 综合后的门级描述 | `reports/netlist.v` |
| **时序报告** | Setup/Hold slack | `reports/timing.rpt` |
| **面积报告** | 门数、单元面积 | `reports/area.rpt` |
| **功耗报告** | 动态/静态功耗 | `reports/power.rpt` |
| **约束检查报告** | 约束完整性 | `reports/constraints.rpt` |

## 综合流程

```
RTL代码 → 工艺映射 → 逻辑优化 → 门级网表
   ↓         ↓           ↓           ↓
 约束     标准单元    面积/时序    时序收敛
```

## 综合工具

| 工具 | 厂商 | 说明 |
|------|------|------|
| **Design Compiler** | Synopsys | 工业界标准 |
| **Genus** | Cadence | 高容量综合 |
| **RTL Compiler** | Synopsys | 物理感知综合 |
| **Yosys** | 开源 | 开源综合工具 |

## SDC约束示例

```tcl
# 01-synthesis/constraints.sdc

# 时钟定义
create_clock -name clk -period 10 [get_ports clk]

# 时钟不确定性 (skew + jitter)
set_clock_uncertainty 1.0 [get_clocks clk]

# 输入延迟
set_input_delay 2.0 -clock clk [all_inputs]

# 输出延迟
set_output_delay 2.0 -clock clk [all_outputs]

# 输入驱动强度
set_driving_cell -lib_cell INVX1 [all_inputs]

# 输出负载
set_load 0.1 [all_outputs]

# 时钟转换时间
set_clock_transition 0.5 [get_clocks clk]

# 不要优化的常量信号
set_dont_touch_network [get_ports clk]
set_dont_touch_network [get_ports rst_n]
```

## 综合脚本示例 (DC)

```tcl
# 01-synthesis/run_synthesis.tcl

# 1. 设置
set_app_var target_library "sky130_fd_sc_hd__tt_025C_1v80.lib"
set_app_var link_library "* $target_library"

# 2. 读入设计
read_verilog rtl/uart_top.v
current_design uart_top
link

# 3. 约束
source constraints/constraints.sdc

# 4. 编译
compile_ultra -timing_high_effort

# 5. 报告
report_timing > reports/timing.rpt
report_area > reports/area.rpt
report_power > reports/power.rpt
report_constraints > reports/constraints.rpt

# 6. 输出
write -format verilog -hierarchy -output netlist/uart_netlist.v
write_sdc -version 2.1 constraints/post_synth.sdc
```

## 核心指标

| 指标类别 | 关键指标 | 目标示例 |
|----------|----------|----------|
| **时序** | WNS (Worst Negative Slack) | ≥ 0 |
|  | TNS (Total Negative Slack) | = 0 |
| **面积** | 总门数 | < 10K gates |
|  | 标准单元面积 | < 5000 μm² |
| **功耗** | 总功耗 | < 5mW |
|  | 漏电功耗占比 | < 20% |
| **设计规则** | 最大转换时间 | < 0.5ns |
|  | 最大电容 | < 0.5pF |
| **综合质量** | 运行时间 | < 1 hour |
|  | 收敛迭代次数 | < 3 |

## 时序分析基础

### Setup Time Check (建立时间)

```
数据到达时间 < 时钟周期 - 建立时间要求

Launch Edge → Capture Edge
     ↓              ↓
  数据路径      时钟路径
     ↓              ↓
 T_launch     T_capture
     +              +
   T_comb       T_clk_skew
     ↓              ↓
  T_data_arrive   T_clk_arrive

要求: T_data_arrive ≤ T_clk_arrive - T_setup
```

### Hold Time Check (保持时间)

```
数据到达时间 > 保持时间要求

同一时钟边沿
     ↓
  数据路径必须保持稳定至少T_hold时间

要求: T_data_arrive ≥ T_clk_arrive + T_hold
```

## 综合优化策略

| 策略 | 面积 | 时序 | 功耗 | 适用场景 |
|------|------|------|------|----------|
| **Timing-driven** | ↑ | ↑↑ | → | 关键路径优化 |
| **Area-driven** | ↑↑ | → | ↓ | 面积敏感设计 |
| **Power-driven** | ↑ | ↓ | ↑↑ | 低功耗设计 |
| **Physical-aware** | ↑ | ↑ | ↑ | 时序收敛困难时 |

## 常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Setup违例 | 组合逻辑太长 | 增加流水级、使用更强单元 |
| Hold违例 | 数据路径太短 | 插入buffer、调整单元 |
| 面积超标 | 逻辑过于复杂 | 共享逻辑、资源复用 |
| 功耗超标 | 翻转率太高 | 门控时钟、操作数隔离 |

## 质量检查清单

- [ ] 时序收敛 (WNS ≥ 0, TNS = 0)
- [ ] 无约束违例
- [ ] 无设计规则违例
- [ ] 网表与RTL功能一致 (形式验证)
- [ ] 面积在目标范围内
- [ ] 功耗在预算内

---

`★ Insight ─────────────────────────────────────`
1. **约束是综合的灵魂**: 完整准确的SDC约束直接决定综合质量，缺失约束会导致假性时序收敛
2. **物理感知综合**: 现代综合工具需要预估物理信息 (如线负载模型) 才能准确预测时序
3. **增量综合**: RTL小改动时只重综合修改部分，显著减少运行时间
`─────────────────────────────────────────────────`
