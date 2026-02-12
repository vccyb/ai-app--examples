# 06 - 时序分析阶段 (Timing Analysis)

## 阶段目标

验证设计在所有工艺角 (PVT Corner) 下满足时序要求，确保芯片在目标频率下稳定工作。

## 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 门级网表 | P&R阶段 | 包含寄生参数 |
| SDF文件 | P&R阶段 | 标准延迟格式 |
| SPEF文件 | P&R阶段 | 寄生参数RC |
| SDC约束 | 综合/P&R | 时序约束 |
| **工艺库** | 晶圆厂 | 不同PVT角 |

## 关键输出件

| 输出文件 | 说明 | 位置 |
|----------|------|------|
| **时序报告** | Setup/Hold分析 | `reports/signoff_timing.rpt` |
| **时序图** | 关键路径可视化 | `reports/timing_graph.png` |
| **时钟报告** | 时钟质量分析 | `reports/clock_quality.rpt` |
| **SI报告** | 信号完整性分析 | `reports/signal_integrity.rpt` |
| **OCV报告** | 片上偏差分析 | `reports/ocv.rpt` |

## 时序分析类型

```
┌────────────────────────────────────────────────────┐
│           STA (Static Timing Analysis)            │
│     静态时序分析 - 无需仿真，分析所有路径           │
├────────────────────────────────────────────────────┤
│  1. Setup Check (建立时间检查)                     │
│     └─ Max Path Analysis (最大延迟分析)            │
├────────────────────────────────────────────────────┤
│  2. Hold Check (保持时间检查)                      │
│     └─ Min Path Analysis (最小延迟分析)            │
├────────────────────────────────────────────────────┤
│  3. Recovery/Removal Check                        │
│     └─ 异步复位/置位时序检查                       │
└────────────────────────────────────────────────────┘
```

## PVT工艺角 (Process, Voltage, Temperature)

| 角名称 | 工艺 | 电压 | 温度 | 说明 |
|--------|------|------|------|------|
| **TT** | Typical | 1.0V | 25°C | 典型工作条件 |
| **SS** | Slow | 0.9V | 125°C | 最慢角 (Setup检查) |
| **FF** | Fast | 1.1V | -40°C | 最快角 (Hold检查) |
| **SF** | Slow-Fast | 0.9V | -40°C | 混合角 |
| **FS** | Fast-Slow | 1.1V | 125°C | 混合角 |

### 时序分析Corner配置

```tcl
# Setup检查使用最慢角 (SS, 1.0V, 125°C)
set_timing_derate -early 1.0 -cell_delay -net_delay
set_timing_derate -late 1.1 -cell_delay -net_delay

read_liberty slow_ss_1v0_125c.lib

# Hold检查使用最快角 (FF, 1.1V, -40°C)
read_liberty fast_ff_1v1_m40c.lib
```

## 时序路径分析

### 关键时序参数

```tcl
# 时序路径组成
Launch Edge → Capture Edge
     ↓
  时钟路径 (Clock Path)
  {
    Clock Source
    → Clock Tree
    → Clock Pin (of Capture FF)
  }
  ↓
  数据路径 (Data Path)
  {
    Launch FF CK→Q
    → Combinational Logic
    → Setup/Hold Time (of Capture FF)
  }
  ↓
  时序检查
```

### Setup时序方程

```
Required Time = Period + T_capture - T_setup - T_skew
Arrival Time = T_launch + T_clk_to_q + T_comb

Slack = Required Time - Arrival Time

要求: Slack ≥ 0
```

### Hold时序方程

```
Required Time = T_capture + T_hold + T_skew
Arrival Time = T_launch + T_clk_to_q + T_comb_min

Slack = Arrival Time - Required Time

要求: Slack ≥ 0
```

## 时序分析工具

| 工具 | 厂商 | 说明 |
|------|------|------|
| **PrimeTime** | Synopsys | 业界标准 |
| **Tempus** | Cadence | 高性能STA |
| **OpenSTA** | 开源 | 开源时序分析工具 |

## OpenSTA脚本示例

```tcl
# 06-timing-analysis/run_sta.tcl

# 1. 读入设计
read_liberty sky130_fd_sc_hd__ss_n40C_1v60.lib
read_verilog netlist/uart_netlist.v
link_design uart_top

# 2. 读入约束
read_sdc constraints/post_route.sdc

# 3. 读入寄生参数
read_spef outputs/uart.spef

# 4. 读入延迟 (SDF可选)
read_sdf outputs/uart.sdf

# 5. 时序分析
update_timing

# 6. 报告
# Setup检查
report_checks -path_delay max \
    -format full \
    -max_paths 10 \
    > reports/setup.rpt

# Hold检查
report_checks -path_delay min \
    -format full \
    -max_paths 10 \
    > reports/hold.rpt

# 时钟质量
report_clock > reports/clocks.rpt

# 时钟交互
report_clock_interaction > reports/clock_interaction.rpt

# 生成时序图
write_graphviz reports/timing_graph.dot
exec dot -Tpng reports/timing_graph.dot -o reports/timing_graph.png

# 7. 时序总结
set setup_wns [get_attribute [get_timing_paths -max_paths 1 -slack_type max] slack]
set hold_wns [get_attribute [get_timing_paths -max_paths 1 -slack_type min] slack]

puts "=== Timing Summary ==="
puts "Setup WNS: $setup_wns ns"
puts "Hold WNS:  $hold_wns ns"

# 退出
exit
```

## 核心指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **WNS** | Worst Negative Slack | ≥ 0 (建议 > 0.1ns) |
| **TNS** | Total Negative Slack | = 0 |
| **Timing Violations** | 违例路径数量 | = 0 |
| **Clock Skew** | 时钟偏差 | < 目标周期的5% |
| **Clock Transition** | 时钟翻转时间 | < 100ps |
| **Critical Path Length** | 关键路径级数 | < 20级 |
| **OCV** | 片上变异 | 考虑10-20%余量 |

## 时序例外 (Timing Exceptions)

```tcl
# 1. 多周期路径 (Multicycle Path)
# 数据需要2个时钟周期才能稳定
set_multicycle_path 2 \
    -setup \
    -from [get_cells reg1*] \
    -to [get_cells reg2*]

set_multicycle_path 1 \
    -hold \
    -from [get_cells reg1*] \
    -to [get_cells reg2*]

# 2. 虚假路径 (False Path)
# 跨时钟域、复位逻辑、测试逻辑
set_false_path \
    -from [get_cells reset_sync*] \
    -to [get_pins *]

# 3. 最大延迟/最小延迟约束
set_max_delay 5.0 \
    -from [get_ports data_in*] \
    -to [get_registers data_reg*]

set_min_delay 0.5 \
    -from [get_ports data_in*] \
    -to [get_registers data_reg*]
```

## 时序优化策略

| 问题类型 | 优化方法 | 工具支持 |
|----------|----------|----------|
| **Setup违例** | 增加流水级 | 设计修改 |
|  | 单元升级 (Size up) | 综合工具 |
|  | 减少负载 (Split fanout) | P&R工具 |
|  | 调整floorplan | P&R工具 |
| **Hold违例** | 插入buffer | P&R工具 |
|  | 单元降级 (Size down) | 综合工具 |
|  | 增加线长 | P&R工具 |
|  | 调整单元摆放 | P&R工具 |

## 时序签收检查清单

- [ ] 所有Corner时序收敛
- [ ] Setup WNS ≥ 0 (所有Corner)
- [ ] Hold WNS ≥ 0 (所有Corner)
- [ ] 无Clock Domain Crossing问题 (或已处理)
- [ ] 异步复位Removal检查通过
- [ ] 信号完整性 (SI) 分析完成
- [ ] OCV (On-Chip Variation) 已考虑
- [ ] 时序报告已审查并存档

## 高级主题

### 1. CRPR (Clock Reconvergence Pessimism Removal)

```tcl
# 消除时钟路径悲观估计
set_crpr_mode true
```

### 2. Signal Integrity (SI) 分析

```tcl
# 考虑crosstalk对延迟的影响
enable_si_mode -analysis crosstalk

# 报告SI违例
report_si -violations > reports/si_violations.rpt
```

### 3. AOCV (Advanced OCV)

```tcl
# 精细化片上变异分析
set_aocv_model \
    -depth 5 \
    -variation 0.2 \
    -cell_type register
```

---

`★ Insight ─────────────────────────────────────`
1. **Corner分析必不可少**: 只分析TT角是不够的，必须覆盖SS/FF/SF/FS才能保证芯片在全温全压范围内工作
2. **时序例外需谨慎**: 过多的False Path/Multicycle Path可能导致真实时序问题被忽略，必须严格审查
3. **SI影响日益显著**: 在先进工艺 (7nm及以下)，crosstalk可能导致10-20%的延迟变化，必须考虑
`─────────────────────────────────────────────────`
