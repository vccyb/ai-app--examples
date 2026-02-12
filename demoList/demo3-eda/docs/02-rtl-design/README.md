# 02 - RTL设计阶段 (RTL Design)

## 阶段目标

使用硬件描述语言 (Verilog/SystemVerilog) 实现规格定义的功能，形成可综合的RTL代码。

## 输入

| 输入项 | 来源 |
|--------|------|
| 规格书 | 上一阶段输出 |
| 时钟复位策略 | 架构设计 |
| 编码规范 | 项目标准 |

## 关键输出件

| 输出文件 | 说明 | 位置 |
|----------|------|------|
| **RTL源代码** | 可综合的HDL代码 | `design/rtl/` |
| **代码覆盖率报告** | 行/分支/状态机覆盖率 | `reports/coverage/` |
| **代码检查报告** | Lint检查结果 | `reports/lint/` |
| **设计文档** | 模块说明、时序图 | `docs/rtl-design/` |

## RTL设计原则

### 1. 命名规范
```systemverilog
// 信号命名: <功能>_<级别>_<信号>
module uart_tx (
    input  wire        clk,          // 时钟
    input  wire        rst_n,        // 低电平复位
    input  wire        tx_start,     // 发送启动
    input  wire [7:0]  tx_data,      // 发送数据
    output reg         tx            // TX引脚
);
```

### 2. 时钟复位策略
```systemverilog
// 推荐使用异步复位、同步释放
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        tx_state <= IDLE;
    else
        tx_state <= tx_next_state;
end
```

### 3. 状态机编码
```systemverilog
// 使用one-hot编码，利于综合工具优化
typedef enum logic [2:0] {
    IDLE     = 3'b001,
    START    = 3'b010,
    DATA     = 3'b100
} state_t;
```

## 代码检查工具

| 工具 | 功能 | 开源/商业 |
|------|------|----------|
| **Verilator** | Lint + 仿真 | 开源 |
| **SpyGlass** | Lint + CDC检查 | 商业 |
| **Verilator-coverage** | 代码覆盖率 | 开源 |

## 核心指标

| 指标 | 目标 | 说明 |
|------|------|------|
| 代码行数 | - | 预估规模 |
| 模块数量 | - | 复杂度评估 |
| FIFO深度 | 16/32/64 | 缓存设计 |
| 状态机数量 | - | 控制逻辑复杂度 |

## 示例模块结构

```
design/rtl/
├── uart_top.sv              #顶层模块
├── uart_tx.sv              #发送模块
├── uart_rx.sv              #接收模块
├── uart_regs.sv            #寄存器组
└── fifo_sync.sv            #同步FIFO
```

## 质量检查清单

- [ ] 无锁存器 (latch) 产生
- [ ] 无组合逻辑环路
- [ ] 复位策略统一
- [ ] 时钟域清晰 (无混频)
- [ ] 命名符合规范
- [ ] 注释覆盖率 >80%
- [ ] Lint检查无error

---

`★ Insight ─────────────────────────────────────`
1. **可综合性是关键**: RTL代码必须能被综合工具转换为门级网表，避免使用不可综合语法 (如 `initial`, `delay #10`)
2. **时序收敛从RTL开始**: 合理的流水线设计和关键路径优化能显著减少后端迭代
3. **代码复用**: 使用参数化设计 (parameter) 提高代码复用性，如FIFO深度可配置
`─────────────────────────────────────────────────`
