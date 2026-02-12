# 快速开始指南

欢迎来到数字芯片设计流程学习项目！本指南将帮助你快速上手。

## 📚 学习路径

```
第1阶段: 理论学习 (1-2周)
  └─ 阅读 docs/ 下各阶段文档

第2阶段: 工具实践 (2-4周)
  └─ 使用开源工具完成小型设计

第3阶段: 完整流程 (1-2个月)
  └─ 从规格到流片的完整项目
```

## 🎯 第一周学习计划

### Day 1-2: 理解整体流程
- [ ] 阅读 `README.md` - 了解整体架构
- [ ] 阅读 `docs/01-specification/README.md` - 规格定义
- [ ] 思考: 为什么规格冻结如此重要?

### Day 3-4: RTL设计入门
- [ ] 阅读 `docs/02-rtl-design/README.md`
- [ ] 查看示例代码: `design/rtl/uart_tx.sv`
- [ ] 动手: 修改UART模块, 添加校验位

### Day 5-6: 验证基础
- [ ] 阅读 `docs/03-verification/README.md`
- [ ] 查看测试平台: `design/tb/uart_tb_top.sv`
- [ ] 运行仿真 (见下方工具安装)

### Day 7: 综合概念
- [ ] 阅读 `docs/04-synthesis/README.md`
- [ ] 理解SDC约束: `design/constraints/constraints.sdc`
- [ ] 思考: Setup和Hold的区别?

## 🛠️ 工具安装

### 选项1: 使用预配置Docker (推荐)

```bash
# 拉取EDA工具镜像
docker pull ghcr.io/chipsalliance/openlane:latest

# 运行容器
docker run -it -v $(pwd):/work openlane
```

### 选项2: 本地安装开源工具

```bash
# 1. Verilator (仿真+Lint)
sudo apt-get install verilator

# 2. Yosys (综合)
git clone https://github.com/YosysHQ/yosys.git
cd yosys
make
sudo make install

# 3. OpenROAD (P&R)
git clone https://github.com/The-OpenROAD-Project/OpenROAD.git
cd OpenROAD
mkdir build && cd build
cmake ..
make
sudo make install

# 4. OpenSTA (时序分析)
git clone https://github.com/The-OpenROAD-Project/OpenSTA.git
cd OpenSTA
mkdir build && cd build
cmake ..
make
sudo make install

# 5. KLayout (GDS查看器)
sudo apt-get install klayout
```

## 🚀 实践练习1: UART设计

### 目标
完成一个简化UART控制器, 理解完整设计流程。

### 步骤

#### 1. 规格定义 (30分钟)
```bash
# 编辑规格书
cd docs/01-specification/
vim spec_template.md

# 定义你的UART规格:
# - 波特率: 115200
# - 数据位: 8
# - 停止位: 1
# - FIFO: 8字节
```

#### 2. RTL设计 (2-3小时)
```bash
# 查看示例代码
cd design/rtl/
cat uart_tx.sv

# 动手练习:
# 1. 实现uart_rx模块 (接收端)
# 2. 实现uart_top顶层模块
# 3. 添加8字节FIFO
```

提示: RX模块需要检测起始位下降沿, 然后按波特率采样。

#### 3. 仿真验证 (1-2小时)
```bash
# 使用Verilator运行仿真
cd design/tb/
verilator -Wall --trace uart_tx.sv uart_tb_top.sv \
    --cc --exe uart_tb_main.cpp
make -C obj_dir -f Vuart_tb_top.mk Vuart_tb_top
./obj_dir/Vuart_tb_top

# 查看波形
gtkwave uart_tb_wave.vcd
```

期望输出:
```
[Test 1] Basic transmission test
[100ns] Sending byte: 0xA5
[50000ns] PASS: Received 0xA5 (expected 0xA5)
...
```

#### 4. 代码检查 (30分钟)
```bash
# Lint检查
verilator --lint-only -Wall design/rtl/*.sv

# 修复所有warning, 确保无error
```

#### 5. 综合 (1-2小时)
```bash
# 使用Yosys综合
cd design/
yosys -s scripts/synthesis.tcl

# 查看综合报告
cat reports/area.rpt
cat reports/timing.rpt
```

综合脚本示例 (`scripts/synthesis.tcl`):
```tcl
# 读入设计
read_verilog rtl/uart_top.v
hierarchy -check -top uart_top

# 综合技术映射
proc; opt; fsm; opt; memory; opt

# 报告
stat

# 输出网表
write_verilog netlist/uart_netlist.v
```

#### 6. 时序分析 (1小时)
```bash
# 使用OpenSTA
opensta scripts/sta.tcl

# 检查Setup/Hold时序
# 目标: WNS >= 0
```

## 📊 进阶练习

### 练习2: I2C控制器
- 理解I2C协议
- 实现Master模式
- 添加多从机支持

### 练习3: SPI控制器
- 理解SPI协议
- 实现可配置CPOL/CPHA
- 添加多通道支持

### 练习4: 定时器/计数器
- 实现可配置定时器
- 添加PWM输出
- 支持中断生成

## 🎓 学习资源

### 书籍推荐
1. **"数字集成电路设计与验证"** - 中文教材
2. **"Computer Architecture: A Quantitative Approach"** - 经典教材
3. **"Digital Design and Computer Architecture"** - 入门必读

### 在线课程
- **Coursera: VLSI CAD Part I: Logic** (免费)
- **edX: Circuits and Electronics** (MIT)
- **NPTEL: Digital VLSI Design** (印度理工)

### 开源项目
- **OpenHW Group**: RISC-V核心实现
- **PULP Platform: 平行超低功耗处理器
- **SkyWater PDK**: 开源PDK, 130nm工艺

## 💡 常见问题

### Q1: 没有FPGA板能学吗?
A: 可以! 本项目使用软件仿真, 不需要硬件。

### Q2: 需要多深掌握Verilog?
A: 基础即可 - 本项目代码量不大, 边学边用。

### Q3: 商业工具太贵怎么办?
A: 使用开源工具链 (Yosys+OpenROAD+OpenSTA), 功能足够学习使用。

### Q4: 需要什么背景?
A: 数字逻辑基础即可。如果有C/C++经验会更容易上手。

### Q5: 完成整个项目需要多久?
A:
- 快速过一遍: 2周
- 深入理解每个阶段: 2-3个月
- 完整实践项目: 6个月+

## 🏆 成果展示

完成学习后, 你将能够:

- ✅ 理解数字芯片设计的完整流程
- ✅ 独立完成小型数字模块设计
- ✅ 编写Testbench进行验证
- ✅ 阅读时序报告并优化设计
- ✅ 理解流片前各项检查的重要性

## 📝 下一步

1. **加入社区**:
   - Reddit: r/ASICdesign
   - GitHub: 搜索 "open source eda"

2. **进阶学习**:
   - 学习高级验证技术 (UVM)
   - 研究RISC-V处理器设计
   - 参与开源芯片项目

3. **职业发展**:
   - 数字IC设计工程师
   - 验证工程师
   - 后端设计工程师
   - FPGA工程师

---

`★ Insight ─────────────────────────────────────`
1. **实践驱动学习**: 光看文档不够, 必须动手写代码、跑仿真, 才能真正理解
2. **由简入繁**: 从UART这种简单协议入手, 再逐步学习复杂协议 (PCIe, DDR)
3. **工具链很重要**: 开源工具链虽然不如商业工具完善, 但足以学习核心概念
`─────────────────────────────────────────────────`

祝你学习愉快！ 🚀
