// =============================================================================
// UART发送模块测试平台
// 功能: 验证uart_tx模块的正确性
// =============================================================================

`timescale 1ns / 1ps

module uart_tb_top;

    // -------------------------------------------------------------------------
    // 时钟与复位生成
    // -------------------------------------------------------------------------
    logic clk;
    logic rst_n;

    parameter CLK_PERIOD = 20;  // 50MHz -> 20ns周期

    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    initial begin
        rst_n = 0;
        #100;
        rst_n = 1;
    end

    // -------------------------------------------------------------------------
    // DUT接口
    // -------------------------------------------------------------------------
    logic        tx_start;
    logic [7:0]  tx_data;
    logic        tx;
    logic        tx_busy;

    // 波特率参数: 115200 @ 50MHz
    // CLKS_PER_BIT = 50,000,000 / 115,200 = 434
    localparam CLKS_PER_BIT = 434;

    uart_tx #(
        .CLKS_PER_BIT(CLKS_PER_BIT)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .tx_start(tx_start),
        .tx_data(tx_data),
        .tx(tx),
        .tx_busy(tx_busy)
    );

    // -------------------------------------------------------------------------
    // UART监控: 采样TX信号并解析数据
    // -------------------------------------------------------------------------
    logic [7:0] rx_data;
    logic       rx_valid;

    int bit_timer;
    int bit_index;
    logic [7:0] shift_reg;

    always @(posedge clk) begin
        // 检测起始位 (下降沿)
        if (tx == 0 && bit_timer == 0) begin
            bit_timer = CLKS_PER_BIT / 2;  // 在位中间采样
            bit_index = 0;
            shift_reg = 0;
        end

        // 计时器递减
        if (bit_timer > 0) begin
            bit_timer = bit_timer - 1;
            if (bit_timer == 0) begin
                // 采样数据位
                if (bit_index > 0 && bit_index <= 8) begin
                    shift_reg[bit_index-1] = tx;
                end

                if (bit_index < 9) begin
                    bit_timer = CLKS_PER_BIT;
                    bit_index = bit_index + 1;
                end else begin
                    // 接收完成
                    rx_data = shift_reg;
                    rx_valid = 1;
                end
            end
        end else begin
            rx_valid = 0;
        end
    end

    // -------------------------------------------------------------------------
    // 测试任务
    // -------------------------------------------------------------------------
    task automatic send_byte(input logic [7:0] data);
        begin
            $display("[%0t] Sending byte: 0x%h", $time, data);

            // 等待DUT空闲
            wait(!tx_busy);
            @(posedge clk);

            // 启动发送
            tx_data = data;
            tx_start = 1;
            @(posedge clk);
            tx_start = 0;

            // 等待发送完成
            wait(!tx_busy);

            // 检查接收数据
            @(posedge clk);
            wait(rx_valid);
            if (rx_data == data) begin
                $display("[%0t] PASS: Received 0x%h (expected 0x%h)",
                         $time, rx_data, data);
            end else begin
                $error("[%0t] FAIL: Received 0x%h (expected 0x%h)",
                       $time, rx_data, data);
            end
        end
    endtask

    // -------------------------------------------------------------------------
    // 主测试流程
    // -------------------------------------------------------------------------
    initial begin
        $display("========================================");
        $display("UART TX Module Test");
        $display("========================================");

        // 初始化
        tx_start = 0;
        tx_data = 0;

        // 等待复位完成
        wait(rst_n);
        repeat(10) @(posedge clk);

        // ====================================
        // Test 1: 基本发送测试
        // ====================================
        $display("\n[Test 1] Basic transmission test");
        send_byte(8'hA5);  // 10100101 - 交替模式便于观察
        send_byte(8'h55);  // 01010101
        send_byte(8'h00);  // 全0
        send_byte(8'hFF);  // 全1

        // ====================================
        // Test 2: 连续发送测试
        // ====================================
        $display("\n[Test 2] Back-to-back transmission");
        for (int i = 0; i < 10; i++) begin
            send_byte(i);
        end

        // ====================================
        // Test 3: 随机数据测试
        // ====================================
        $display("\n[Test 3] Random data test");
        repeat(20) begin
            logic [7:0] rand_data;
            rand_data = $random();
            send_byte(rand_data);
        end

        // ====================================
        // Test 4: 忙信号测试
        // ====================================
        $display("\n[Test 4] Busy signal test");
        wait(!tx_busy);
        tx_data = 8'hAA;
        tx_start = 1;
        @(posedge clk);
        tx_start = 0;

        if (tx_busy) begin
            $display("[%0t] PASS: Busy signal asserted", $time);
        end else begin
            $error("[%0t] FAIL: Busy signal not asserted", $time);
        end

        wait(!tx_busy);
        if (!tx_busy) begin
            $display("[%0t] PASS: Busy signal de-asserted", $time);
        end else begin
            $error("[%0t] FAIL: Busy signal still asserted", $time);
        end

        // ====================================
        // 完成测试
        // ====================================
        repeat(100) @(posedge clk);
        $display("\n========================================");
        $display("All tests completed!");
        $display("========================================");
        $finish;
    end

    // -------------------------------------------------------------------------
    // 超时保护
    // -------------------------------------------------------------------------
    initial begin
        #10ms;  // 10ms超时
        $error("Timeout! Test hung.");
        $finish;
    end

    // -------------------------------------------------------------------------
    // 波形导出 (用于Verdi/GTKwave查看)
    // -------------------------------------------------------------------------
    initial begin
        $dumpfile("uart_tb_wave.vcd");
        $dumpvars(0, uart_tb_top);
    end

    // -------------------------------------------------------------------------
    // 覆盖率采样
    // -------------------------------------------------------------------------
    covergroup cg_uart_tx @(posedge clk);
        cp_state: coverpoint dut.state {
            bins idle = {0};
            bins start = {1};
            bins data = {2};
            bins stop = {3};
            bins done = {4};
        }

        cp_data: coverpoint tx_data {
            bins zeros = {8'h00};
            bins ones = {8'hFF};
            bins alternate = {8'h55, 8'hAA};
            bins others = default;
        }

        cross_state_data: cross cp_state, cp_data;
    endgroup

    cg_uart_tx cg = new();

endmodule

// =============================================================================
// 运行说明
// =============================================================================
//
// 使用Verilator运行:
//   verilator -Wall --cc --trace uart_tx.sv uart_tb_top.sv \
//     --exe testbench.cpp
//
// 使用ModelSim/QuestaSim运行:
//   vlog uart_tx.sv uart_tb_top.sv
//   vsim uart_tb_top
//   run -all
//
// 查看波形:
//   gtkwave uart_tb_wave.vcd
//
// =============================================================================
