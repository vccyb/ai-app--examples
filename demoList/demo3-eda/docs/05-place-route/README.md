# 05 - 布局布线阶段 (Place & Route)

## 阶段目标

将门级网表转换为物理版图 (GDSII)，完成标准单元放置、互连布线，确保时序、DRC、LVS全部通过。

## 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 门级网表 | 综合阶段 | .v格式 |
| 时序约束 | 综合后SDC | .sdc格式 |
| **工艺库** | 晶圆厂 | LEF/LIB/QRC Techfile |
| **IP核** | 第三方/自研 | 模块级版图 |

## 关键输出件

| 输出文件 | 说明 | 位置 |
|----------|------|------|
| **GDSII** | 最终版图数据 | `outputs/uart.gds` |
| **SPEF** | 寄生参数信息 | `outputs/uart.spef` |
| **SDF** | 延迟信息 | `outputs/uart.sdf` |
| **DEF** | 设计交换格式 | `outputs/uart.def` |
| **时序报告** | P&R后时序 | `reports/timing_final.rpt` |
| **DRC报告** | 设计规则检查 | `reports/drc.rpt` |
| **LVS报告** | 版图与原理图一致性 | `reports/lvs.rpt` |

## P&R流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 数据准备 (Data Setup)                                │
│     └─ 读入网表、库、floorplan定义                      │
├─────────────────────────────────────────────────────────┤
│  2. 布局规划 (Floorplanning)                             │
│     └─ 定义核心区域、放置宏单元、电源规划               │
├─────────────────────────────────────────────────────────┤
│  3. 放置 (Placement)                                    │
│     └─ 标准单元物理放置、时序驱动放置                  │
├─────────────────────────────────────────────────────────┤
│  4. 时钟树综合 (CTS)                                     │
│     └─ 构建平衡的时钟网络、skew最小化                   │
├─────────────────────────────────────────────────────────┤
│  5. 布线 (Routing)                                      │
│     ├─ 全局布线 (Global Route)                          │
│     ├─ 详细布线 (Detail Route)                          │
│     └─ 修复DRC违例                                      │
├─────────────────────────────────────────────────────────┤
│  6. 优化与签收 (Optimization & Signoff)                 │
│     └─ 时序优化、功耗优化、DRC/LVS签收                  │
└─────────────────────────────────────────────────────────┘
```

## P&R工具

| 工具 | 厂商 | 说明 |
|------|------|------|
| **ICC2** | Synopsys | 物理设计主流工具 |
| **Innovus** | Cadence | 高容量P&R |
| **Titan** | Synopsys | 高性能设计 |
| **OpenROAD** | 开源 | 完整开源P&R流程 |

## OpenROAD脚本示例

```tcl
# 05-place-route/pnr_script.tcl

# 1. 读入设计
read_liberty sky130_fd_sc_hd__tt_025C_1v80.lib
read_verilog netlist/uart_netlist.v
link_design uart_top

# 2. Floorplan
initialize_floorplan \
    -site unit \
    -die_size 200 200 \
    -core_utilization 0.7

# 放置电源网络
add_rings -nets {VDD VSS} -type core_rings \
    -layer {top M1 bottom M1 left M2 right M2} \
    -width 1.0 -spacing 0.5

# 3. 放置
place_pins -random
global_placement \
    -timing_driven \
    -density 0.7

# 4. 时钟树综合
create_clock -name clk -period 10 [get_ports clk]
clock_tree_synthesis -root_buf CLKBUF_X3 \
    -buf_list CLKBUF_X3,CLKBUF_X2

# 5. 布线
detailed_route -guide reports/route.guide

# 6. 时序分析
report_checks -path_delay max -format full > reports/setup.rpt
report_checks -path_delay min -format full > reports/hold.rpt

# 7. DRC/LVS
run_drc > reports/drc.rpt
run_lvs > reports/lvs.rpt

# 8. 输出
write_gds outputs/uart.gds
write_def outputs/uart.def
write_spef outputs/uart.spef
write_sdf outputs/uart.sdf
```

## 核心指标

| 指标类别 | 关键指标 | 目值示例 |
|----------|----------|----------|
| **时序** | Setup WNS | ≥ 0 (建议 > 0.1ns余量) |
|  | Hold WNS | ≥ 0 (建议 > 0.05ns) |
|  | 时钟skew | < 50ps |
| **面积** | 核心利用率 | 60-80% |
|  | 总面积 | < 2mm² |
| **布线** | 布线拥塞 | < 5% |
|  | 走线长度 | 最小化 |
| **功耗** | IR Drop | < 5% VDD |
|  | EM (电迁移) | 无违例 |
| **DRC/LVS** | DRC错误数 | 0 |
|  | LVS | 匹配 |
| **信号完整性** | crosstalk | < 阈值 |
|  | 噪声 | 无违例 |

## 关键步骤详解

### Floorplanning (布局规划)

```tcl
# 定义core区域
create_floorplan \
    -core_utilization 0.7 \
    -core_aspect_ratio 1.0 \
    -site core

# 放置宏单元 (如SRAM)
place_cell macro_ram \
    -location {100 100} \
    -orientation R0

# 电源网络规划
create_power_ring \
    -nets {VDD VSS} \
    -layers {M1 M2} \
    -widths {1.0 1.0} \
    -spacings {0.5 0.5}

create_power_straps \
    -nets {VDD} \
    -layer M3 \
    -direction vertical \
    -width 0.5 \
    -pitch 10
```

### Clock Tree Synthesis (时钟树综合)

```tcl
# 时钟树目标
setCTSMode \
    -clkMaxLatency 500ps \
    -clkMaxSkew 50ps \
    -clkMaxSinkTran 100ps

# 时钟单元
setCTSModel \
    -bufCellBuf {CLKBUF_X1 CLKBUF_X2 CLKBUF_X3} \
    -invCellInv {CLKINV_X1 CLKINV_X2}

# CTS约束
setCTSMode \
    -routeTopPreferredLayer M3 \
    -routeBottomPreferredLayer M2 \
    -targetSkew 0.05

# 执行CTS
ccopt_design
```

### Timing Optimization (时序优化)

```tcl
# Setup优化
opt_design -setup -hold

# 修复setup违例
# 方法1: 插入buffer
insert_buffer [get_pins data_path/Q] BUFFX2

# 方法2: 单元升级
size_cell [get_cells U1] INVX4

# 方法3: 路径重构
refactor_design -incremental
```

## 寄生参数提取

```tcl
# 提取RC寄生参数
extract_rc

# 输出SPEF (Standard Parasitic Exchange Format)
write_parasitics -spef_file uart.spef

# SPEF示例片段
*NAME_MAP
*1 U1/A
*2 U2/Z
*500 net1

*RES
*1 *2 10.5

*CAP
*1 0.02
*2 0.03
```

## DRC检查项目

| DRC类别 | 检查项 | 示例 |
|---------|--------|------|
| **最小间距** | 不同层金属间距 | metal1 spacing ≥ 0.09μm |
| **最小宽度** | 金属线宽度 | metal1 width ≥ 0.09μm |
| **密度** | 金属密度要求 | metal1 density 30-70% |
| **天线效应** | 长距离金属积累 | max antenna ratio 1000:1 |
| **电迁移** | 电流密度 | max current 0.5mA/μm |

## 常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Setup违例 | 长互联延迟大 | 增加驱动、调整floorplan |
| Hold违例 | 短路径延迟小 | 插入buffer、调整单元尺寸 |
| DRC违例 | 布线空间不足 | 调整布线间距、扩宽core |
| IR Drop | 电源网络阻抗大 | 增加电源strap、加宽金属 |
| 拥塞 | 布线资源不足 | 调整floorplan、增加金属层 |

---

`★ Insight ─────────────────────────────────────`
1. **Floorplan决定成败**: 合理的floorplan能减少50%以上的时序违例和拥塞，宏单元位置尤为关键
2. **时钟是心脏**: CTS质量直接影响整个芯片的时序，skew过大需要大量buffer修复
3. **物理验证必不可少**: DRC/LVS不通过的版图无法制造，这是芯片能工作的最低要求
`─────────────────────────────────────────────────`
