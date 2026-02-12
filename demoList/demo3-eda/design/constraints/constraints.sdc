# =============================================================================
# UART控制器SDC约束文件
# 目标工艺: SkyWater 130nm (sky130_fd_sc_hd)
# 时钟频率: 50MHz (20ns周期)
# =============================================================================

# -----------------------------------------------------------------------------
# 时钟定义
# -----------------------------------------------------------------------------

# 创建主时钟
create_clock -name clk \
    -period 20.000 \
    -waveform {0.000 10.000} \
    [get_ports clk]

# 时钟不确定性 (Setup + Hold)
# 考虑时钟skew、jitter、OCV (On-Chip Variation)
set_clock_uncertainty -setup 1.000 [get_clocks clk]
set_clock_uncertainty -hold  0.500 [get_clocks clk]

# 时钟转换时间 (上升/下降沿)
set_clock_transition 0.500 [get_clocks clk]
set_clock_transition 0.500 [get_clocks clk]

# 时钟延迟 (理想情况, P&R后会更新)
set_clock_latency 0.500 [get_clocks clk]

# -----------------------------------------------------------------------------
# 输入延迟
# -----------------------------------------------------------------------------

# APB总线输入延迟
# 假设外部寄存器Tco = 2ns, 走线延迟 = 1ns
set_input_delay -clock clk \
    -max 3.000 \
    [get_ports paddr*]

set_input_delay -clock clk \
    -max 3.000 \
    [get_ports pwdata*]

set_input_delay -clock clk \
    -max 3.000 \
    [get_ports pwrite]

set_input_delay -clock clk \
    -max 3.000 \
    [get_ports psel*]

set_input_delay -clock clk \
    -max 3.000 \
    [get_ports penable]

# UART RX输入延迟
# 假设外部设备延迟 = 5ns
set_input_delay -clock clk \
    -max 5.000 \
    [get_ports uart_rx]

# 最小输入延迟
set_input_delay -clock clk \
    -min 1.000 \
    [get_ports paddr*]

set_input_delay -clock clk \
    -min 1.000 \
    [get_ports pwdata*]

set_input_delay -clock clk \
    -min 1.000 \
    [get_ports pwrite]

set_input_delay -clock clk \
    -min 1.000 \
    [get_ports psel*]

set_input_delay -clock clk \
    -min 1.000 \
    [get_ports penable]

set_input_delay -clock clk \
    -min 2.000 \
    [get_ports uart_rx]

# -----------------------------------------------------------------------------
# 输出延迟
# -----------------------------------------------------------------------------

# APB总线输出延迟
# 假设下一级寄存器Setup = 2ns, 走线 = 1ns
set_output_delay -clock clk \
    -max 3.000 \
    [get_ports prdata*]

# UART TX输出延迟
set_output_delay -clock clk \
    -max 5.000 \
    [get_ports uart_tx]

set_output_delay -clock clk \
    -max 5.000 \
    [get_ports uart_rts]

# 中断输出延迟
set_output_delay -clock clk \
    -max 3.000 \
    [get_ports intr_*]

# 最小输出延迟
set_output_delay -clock clk \
    -min 1.000 \
    [get_ports prdata*]

set_output_delay -clock clk \
    -min 2.000 \
    [get_ports uart_tx]

set_output_delay -clock clk \
    -min 2.000 \
    [get_ports uart_rts]

set_output_delay -clock clk \
    -min 1.000 \
    [get_ports intr_*]

# -----------------------------------------------------------------------------
# 驱动强度
# -----------------------------------------------------------------------------

# 输入端口驱动强度 (假设外部驱动为INVX1)
set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports paddr*]

set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports pwdata*]

set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports pwrite]

set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports psel*]

set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports penable]

set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports uart_rx]

set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports uart_cts]

set_driving_cell -lib_cell INVX1 \
    -pin Y \
    [get_ports rst_n]

# -----------------------------------------------------------------------------
# 负载
# -----------------------------------------------------------------------------

# 输出端口负载 (假设负载电容为0.1pF)
set_load 0.1 [get_ports prdata*]
set_load 0.1 [get_ports uart_tx]
set_load 0.1 [get_ports uart_rts]
set_load 0.1 [get_ports intr_*]

# -----------------------------------------------------------------------------
# 不要优化的网络
# -----------------------------------------------------------------------------

# 保护时钟和复位网络
set_dont_touch_network [get_ports clk]
set_dont_touch_network [get_ports rst_n]

# -----------------------------------------------------------------------------
# 时钟组 (如果有多时钟)
# -----------------------------------------------------------------------------

# 如果有多个时钟域, 需要定义时钟组关系
# 例如:
# set_clock_groups -asynchronous -group {clk} -group {clk_2x}

# -----------------------------------------------------------------------------
# 时序例外
# -----------------------------------------------------------------------------

# 多周期路径 (如果某个模块需要多个周期完成)
# set_multicycle_path 2 -setup -from [get_cells slow_reg*] -to [get_cells fast_reg*]
# set_multicycle_path 1 -hold -from [get_cells slow_reg*] -to [get_cells fast_reg*]

# 虚假路径 (跨时钟域、测试逻辑、复位同步器)
# set_false_path -from [get_ports test_mode*] -to [all_registers]
# set_false_path -from [get_cells reset_sync*] -to [all_registers]

# 最大/最小延迟约束 (异步接口)
# set_max_delay 10.0 -from [get_ports async_data*] -to [all_registers]
# set_min_delay 1.0 -from [get_ports async_data*] -to [all_registers]

# -----------------------------------------------------------------------------
# 设计规则约束
# -----------------------------------------------------------------------------

# 最大转换时间 (防止信号上升/下降沿过缓)
set_max_transition 0.500 [current_design]

# 最大电容 (防止负载过重)
set_max_capacitance 0.500 [current_design]

# 最大扇出 (防止驱动能力不足)
set_max_fanout 16 [current_design]

# -----------------------------------------------------------------------------
# 权重 (用于综合优化)
# -----------------------------------------------------------------------------

# 设置关键路径权重
# set_weight [get_paths -from [get_ports data_in*]] 10

# -----------------------------------------------------------------------------
# 禁用Timing Check (如果有)
# -----------------------------------------------------------------------------

# 某些特殊路径可能需要禁用时序检查
# set_disable_timing [get_cells async_fifo*]

# =============================================================================
# SDC文件说明
# =============================================================================
#
# 1. 时钟不确定性 (Clock Uncertainty):
#    - Setup不确定性 = skew + jitter + OCV
#    - Hold不确定性 = skew + OCV
#    - 通常设置为周期的5-10%
#
# 2. 输入/输出延迟:
#    - Max延迟: 用于Setup检查
#    - Min延迟: 用于Hold检查
#    - 计算公式见上方注释
#
# 3. 驱动强度与负载:
#    - 驱动强度影响输出转换时间
#    - 负载影响RC延迟
#
# 4. 时序例外:
#    - False Path: 不需要满足时序的路径
#    - Multicycle Path: 需要多个周期的路径
#    - 谨慎使用, 过多可能导致时序收敛假象
#
# 5. 设计规则约束:
#    - 转换时间、电容、扇出限制
#    - 违反这些约束会影响信号完整性
#
# =============================================================================
