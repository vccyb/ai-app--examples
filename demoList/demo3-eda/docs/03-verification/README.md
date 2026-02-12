# 03 - 功能验证阶段 (Verification)

## 阶段目标

验证RTL设计是否满足规格要求，发现并修复功能缺陷。这是设计流程中**最耗时**的阶段 (约占60-70%时间)。

## 输入

| 输入项 | 来源 |
|--------|------|
| RTL代码 | 上一阶段输出 |
| 规格书 | 验证依据 |
| 验证计划 | 测试策略 |

## 关键输出件

| 输出文件 | 说明 | 位置 |
|----------|------|------|
| **测试平台** | Testbench代码 | `design/tb/` |
| **测试用例** | Testcase集合 | `design/tb/tests/` |
| **波形文件** | 仿真波形 | `sim/wave/` |
| **覆盖率报告** | 功能/代码覆盖率 | `reports/coverage/` |
| **回归测试报告** | 自动化测试结果 | `reports/regression/` |

## 验证层次

```
┌─────────────────────────────────────┐
│        系统级验证 (System)          │
├─────────────────────────────────────┤
│        模块级验证 (Unit)            │
├─────────────────────────────────────┤
│        随机验证 (Random)            │
└─────────────────────────────────────┘
```

## 验证方法学

### 1. UVM (Universal Verification Methodology)

```systemverilog
// UVM基础结构
class uart_test extends uvm_test;
    `uvm_component_utils(uart_test)

    uart_env env;
    uart_sequence seq;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        env = uart_env::type_id::create("env", this);
    endfunction

    task run_phase(uvm_phase phase);
        seq = uart_sequence::type_id::create("seq");
        seq.start(env.agent.sequencer);
    endtask
endclass
```

### 2. 验证组件

| 组件 | 作用 |
|------|------|
| **Generator** | 生成随机激励 |
| **Driver** | 驱动DUT信号 |
| **Monitor** | 监控DUT行为 |
| **Scoreboard** | 比对预期与实际结果 |
| **Coverage** | 收集覆盖率数据 |

## 覆盖率指标

| 覆盖率类型 | 目标 | 说明 |
|------------|------|------|
| **代码覆盖率** | 100% | 行、分支、表达式、状态机 |
| **功能覆盖率** | 100% | 规格/验证计划所有feature |
| **断言覆盖率** | 100% | 时序属性检查 |

### 覆盖率计算

```
总覆盖率 = 代码覆盖率 × 0.4 + 功能覆盖率 × 0.6

目标: 总覆盖率 ≥ 95%
```

## 验证工具

| 工具 | 类型 | 说明 |
|------|------|------|
| **VCS** | 商业 | Synopsys仿真器 |
| **QuestaSim** | 商业 | Mentor Graphics |
| **Verilator** | 开源 | 开源Verilog仿真器 |
| **Icarus Verilog** | 开源 | 轻量级仿真器 |

## 示例验证环境

```
design/tb/
├── uart_tb_top.sv           # Testbench顶层
├── uart_if.sv               # 接口定义
├── uart_pkg.sv              # 包含所有component
├── tests/                   # 测试用例
│   ├── uart_base_test.sv
│   ├── uart smoke_test.sv
│   ├── uart_error_test.sv
│   └── uart_random_test.sv
└── scripts/                 # 仿真脚本
    └── run_sim.sh
```

## 典型验证流程

```bash
# 1. 编译RTL + Testbench
vcs -full64 -sverilog \
    -debug_pp \
    -cm line+tgl+branch+fsm+assert \
    rtl/uart_top.sv tb/uart_tb_top.sv

# 2. 运行仿真
./simv +UVM_TESTNAME=uart_smoke_test

# 3. 查看覆盖率
urg -dir simv.vdb

# 4. 查看波形
verdi -ssf wave.fsdb
```

## 质量检查清单

- [ ] 所有测试用例通过
- [ ] 代码覆盖率 ≥ 100% (行/分支)
- [ ] 功能覆盖率 = 100%
- [ ] 无已知bug
- [ ] 回归测试稳定
- [ ] 断言无violation

---

`★ Insight ─────────────────────────────────────`
1. **验证驱动开发**: 推荐先写testbench再写RTL，这样更早明确设计目标，减少返工
2. **断言是关键**: SVA (SystemVerilog Assertions) 能实时检查协议违规，比事后看波形高效10倍
3. **回归测试自动化**: 每次RTL修改后自动跑所有用例，确保新功能不破坏旧功能 (CI/CD理念)
`─────────────────────────────────────────────────`
