# 07 - 物理验证阶段 (Physical Verification)

## 阶段目标

确保版图符合制造工艺规则，与网表功能一致，无电气可靠性问题。这是**流片前最后的守门员**。

## 物理验证三大支柱

```
┌─────────────────────────────────────────────────────────┐
│          1. DRC (Design Rule Check)                     │
│          设计规则检查 - 确保可制造性                     │
├─────────────────────────────────────────────────────────┤
│          2. LVS (Layout vs Schematic)                   │
│          版图原理图一致性 - 确保功能正确                 │
├─────────────────────────────────────────────────────────┤
│          3. ERC (Electrical Rule Check)                 │
│          电气规则检查 - 确保电气可靠性                   │
└─────────────────────────────────────────────────────────┘
```

## 输入

| 输入项 | 来源 | 说明 |
|--------|------|------|
| GDSII | P&R阶段 | 最终版图 |
| 网表 | P&R阶段 | 门级网表 |
| 工艺规则文件 | 晶圆厂 | DRC规则 |
| 器件规则文件 | 晶圆厂 | LVS规则 |
| SPICE模型 | 晶圆厂 | 器件电学参数 |

## 关键输出件

| 输出文件 | 说明 | 位置 |
|----------|------|------|
| **DRC报告** | 规则违例列表 | `reports/drc_final.rpt` |
| **LVS报告** | 一致性检查结果 | `reports/lvs_final.rpt` |
| **ERC报告** | 电气检查结果 | `reports/erc_final.rpt` |
| **ANT报告** | 天线效应报告 | `reports/antenna.rpt` |
| **密度图** | 金属密度分析 | `reports/density_map.png` |

## 物理验证工具

| 工具 | 厂商 | 说明 |
|------|------|------|
| **Calibre** | Siemens (Mentor) | 业界标准 |
| **PVS** | Synopsys | 高性能验证 |
| **ICV** | Cadence | 物理验证系统 |
| **KLayout** | 开源 | 开源GDS查看器+DRC |

## 1. DRC (Design Rule Check)

### DRC规则分类

| 规则类别 | 检查项 | 示例规则 |
|----------|--------|----------|
| **最小间距** | 同层图形间距 | Metal1 spacing ≥ 0.09μm |
| **最小宽度** | 线宽下限 | Metal1 width ≥ 0.09μm |
| **重叠包围** | 层间覆盖 | Poly over Contact ≥ 0.05μm |
| **密度** | 金属填充密度 | Metal1 density 30-70% |
| **天线效应** | 长距离电荷积累 | Antenna ratio ≤ 1000:1 |
| **ESD** | 静电保护 | ESD结构必须存在 |
| **Latchup** | 闩锁效应 | Guard ring必须完整 |

### Calibre DRC脚本示例

```rulefile
# 07-physical-verification/drc_rules.rule

# === 基本规则 ===
# Metal1最小间距
SPACE M1 0.09

# Metal1最小宽度
WIDTH M1 0.09

# Via1包围
ENC V1 M1 0.05
ENC V1 M2 0.05

# === 密度规则 ===
# Metal1密度检查
DENSITY CHECK_LAYER M1
DENSITY WINDOW 100 100
DENSITY VALUE 0.3 0.7

# === 天线规则 ===
# Metal1到Gate的天线比
ANTENNA GATE M1 1000

# === 可制造性规则 ===
# 酸蚀宽度检查 (避免细长结构)
WIDTH M1 0.09 LENGTH 0.5
```

### 运行DRC

```bash
# 使用Calibre运行DRC
calibre -drc \
    -hier \
    -turbo \
    drc_rules.rule \
    outputs/uart.gds \
    reports/drc_final.rpt

# 使用KLayout查看DRC结果
klayout outputs/uart.gds \
    -r drc_markers.lym \
    -m reports/drc_final.rpt
```

### 常见DRC违例及修复

| 违例类型 | 原因 | 修复方法 |
|----------|------|----------|
| **Min Spacing** | 线距太近 | 增加间距、调整布线 |
| **Min Width** | 线太细 | 加宽金属 |
| **Density** | 密度超标 | 添加金属填充 (Metal Fill) |
| **Antenna** | 长线连Gate | 插入跳线 (Jump) 或Diode |
| **Notch** | 凹陷太深 | 填充凹陷区域 |

---

## 2. LVS (Layout vs Schematic)

### LVS流程

```
┌────────────────────────────────────────────────────┐
│  1. 版图提取 (Layout Extraction)                   │
│     └─ 从GDS提取电路图 → SPICE网表                 │
├────────────────────────────────────────────────────┤
│  2. 网表对比 (Netlist Comparison)                  │
│     ├─ 拓扑结构比较 (连接关系)                      │
│     ├─ 器件参数比较 (W/L等)                         │
│     └─ 端口匹配检查                                 │
├────────────────────────────────────────────────────┤
│  3. 报告生成 (Report Generation)                   │
│     └─ 通过/失败 + 错误高亮                         │
└────────────────────────────────────────────────────┘
```

### LVS检查项

| 检查类别 | 说明 | 失败示例 |
|----------|------|----------|
| **拓扑匹配** | 连接关系一致 | 短路、开路、器件缺失 |
| **器件匹配** | 类型、尺寸一致 | NMOS/PMOS反了、W/L不匹配 |
| **端口匹配** | 输入输出对应 | Pin名不匹配 |
| **电源/地** | VDD/VSS连接 | 断电、短路 |

### Calibre LVS脚本示例

```rulefile
# 07-physical-verification/lvs_rules.rule

# === 器件识别 ===
DEVICE MOS NMOS 3
DEVICE MOS PMOS 3
DEVICE RES R 2
DEVICE CAP C 2

# === 连接规则 ===
CONNECT VDD M1
CONNECT VSS M1

# === 端口定义 ===
PORT clk
PORT rst_n
PORT data_in
PORT data_out

# === 电源识别 ===
POWER VDD
GROUND VSS
```

### 运行LVS

```bash
# 提取版图网表
calibre -spice lvs_rules.rule outputs/uart.gds -o layout_extract.sp

# 比对网表
calibre -lvs \
    -hier \
    lvs_rules.rule \
    layout_extract.sp \
    netlist/uart_netlist.v \
    reports/lvs_final.rpt
```

### LVS错误类型

| 错误类型 | 说明 | 示例 |
|----------|------|------|
| **Short** | 短路 | VDD与VSS短路 |
| **Open** | 开路 | 信号线断开 |
| **Device Mismatch** | 器件不匹配 | 提取出NMOS但应为PMOS |
| **Pin Mismatch** | 引脚不匹配 | Pin名大小写不一致 |
| **Subcircuit Mismatch** | 子电路不匹配 | 模块实例化错误 |

---

## 3. ERC (Electrical Rule Check)

### ERC检查项

| 检查类别 | 说明 | 失败后果 |
|----------|------|----------|
| **电源完整性** | IR Drop、EM | 供电不足、可靠性问题 |
| **信号完整性** | Crosstalk、Noise | 时序违例、功能错误 |
| **ESD保护** | 静电放电保护 | 芯片损坏 |
| **Latchup** | 闩锁效应 | 芯片烧毁 |
| **电迁移 (EM)** | 电流密度 | 金属线断裂 |
| **天线效应** | 制造过程电荷积累 | 栅氧击穿 |

### ERC规则示例

```tcl
# 07-physical-verification/erc_rules.tcl

# IR Drop检查
set_max_ir_drop 0.05 ; # 5% VDD

# 电流密度检查 (电迁移)
set_max_current_density 0.5e-6 ; # 0.5 μA/μm

# ESD检查
check_esd -all_pins

# Latchup检查
check_latchup -guard_ring_required

# 天线效应
check_antenna -ratio 1000:1
```

---

## 天线效应修复

### 原理

制造过程中，金属线会积累电荷。如果长金属线直接连到Gate，电荷可能击穿栅氧。

### 修复方法

```tcl
# 方法1: 插入跳线 (Layer Jump)
# 从M1跳到M2，在M2层继续布线
route_antenna_fix \
    -from_layer M1 \
    -to_layer M2 \
    -max_length 500

# 方法2: 插入反偏二极管 (Diode)
# 提供电荷泄放路径
insert_antenna_diode \
    -cell ANTENNA_DIODE \
    -threshold_ratio 1000
```

---

## 密度填充 (Metal Fill)

### 为什么需要填充

- 化学机械抛光 (CMP) 要求金属密度均匀
- 密度过高/过低会导致表面不平整

### 填充策略

```tcl
# 使用Calibre Fill工具
calibre -fill \
    -layer M1 \
    -target_density 0.5 \
    -min_spacing 0.09 \
    -min_width 0.09 \
    -window_size 100

# 填充类型:
# 1. Floating Fill (浮空填充) - 最常用
# 2. Grounded Fill (接地填充) - 需要考虑ESD
```

---

## 物理验证报告示例

```bash
# DRC报告摘要
====================================
DRC Summary Report
====================================
Total DRC Checks:    1523
Violations Found:    0
Status:              PASS
====================================

# LVS报告摘要
====================================
LVS Summary Report
====================================
Topology Match:      YES
Device Match:        YES
Pin Match:           YES
Power/Ground:        VERIFIED
Status:              PASS
====================================

# ERC报告摘要
====================================
ERC Summary Report
====================================
IR Drop:             3.2% (PASS)
EM Violations:       0 (PASS)
Antenna Violations:  0 (PASS)
ESD Protection:      COMPLETE (PASS)
Status:              PASS
====================================
```

---

## 质量检查清单

### DRC检查清单

- [ ] 0个DRC错误
- [ ] 金属密度在30-70%范围
- [ ] 天线效应已修复
- [ ] ESD结构完整
- [ ] 填充不会导致短路

### LVS检查清单

- [ ] 拓扑100%匹配
- [ ] 器件参数匹配
- [ ] Pin数量匹配
- [ ] 电源/地连接正确
- [ ] 无short/open

### ERC检查清单

- [ ] IR Drop < 5%
- [ ] 无电迁移违例
- [ ] 天线效应已消除
- [ ] ESD保护完整
- [ ] Latchup防护完备

---

## 签收标准

物理验证签收必须满足:

```
✓ DRC = 0 Errors
✓ LVS = PASS
✓ ERC = PASS
✓ 所有Corner时序收敛
✓ 可制造性评估通过
✓ 可靠性评估通过
```

只有满足以上条件，才能**流片 (Tapeout)**。

---

`★ Insight ─────────────────────────────────────`
1. **DRC/LVS是流片的硬性门槛**: 任何DRC/LVS错误都可能导致芯片制造失败或功能异常
2. **天线效应常被忽视**: 小设计 (如FPGA) 容易被忽略，但在ASIC设计中必须严格检查
3. **填充需谨慎**: 金属填充可能导致新的DRC问题 (间距) 或寄生电容增加，影响时序
`─────────────────────────────────────────────────`
