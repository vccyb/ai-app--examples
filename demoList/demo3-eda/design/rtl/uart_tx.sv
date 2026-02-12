// =============================================================================
// UART发送模块
// 功能: 将并行数据转换为串行UART协议数据流
// 作者: [Your Name]
// 日期: 2025-01-15
// =============================================================================

module uart_tx #(
    parameter CLKS_PER_BIT = 868  // 50MHz / 115200 * 16 = 6944 (采样), 不使用过采样则为 434
) (
    input  wire        clk,          // 系统时钟
    input  wire        rst_n,        // 低电平复位
    input  wire        tx_start,     // 发送启动信号
    input  wire [7:0]  tx_data,      // 待发送数据
    output reg         tx,           // UART TX引脚
    output reg         tx_busy       // 发送忙标志
);

    // -------------------------------------------------------------------------
    // 状态机定义
    // -------------------------------------------------------------------------
    typedef enum logic [2:0] {
        IDLE    = 3'b000,  // 空闲状态
        START   = 3'b001,  // 发送起始位
        DATA    = 3'b010,  // 发送数据位
        STOP    = 3'b011,  // 发送停止位
        DONE    = 3'b100   // 发送完成
    } state_t;

    state_t state, next_state;

    // -------------------------------------------------------------------------
    // 数据路径
    // -------------------------------------------------------------------------
    reg [15:0] clk_count;       // 时钟计数器
    reg [2:0]  bit_index;       // 当前发送的位索引
    reg [7:0]  tx_data_reg;     // 数据寄存器

    // -------------------------------------------------------------------------
    // 状态机时序逻辑
    // -------------------------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
        end else begin
            state <= next_state;
        end
    end

    // -------------------------------------------------------------------------
    // 状态机组合逻辑
    // -------------------------------------------------------------------------
    always_comb begin
        next_state = state;  // 默认保持当前状态

        case (state)
            IDLE: begin
                if (tx_start)
                    next_state = START;
            end

            START: begin
                if (clk_count == CLKS_PER_BIT - 1)
                    next_state = DATA;
            end

            DATA: begin
                if (clk_count == CLKS_PER_BIT - 1 && bit_index == 7)
                    next_state = STOP;
            end

            STOP: begin
                if (clk_count == CLKS_PER_BIT - 1)
                    next_state = DONE;
            end

            DONE: begin
                next_state = IDLE;
            end

            default: begin
                next_state = IDLE;
            end
        endcase
    end

    // -------------------------------------------------------------------------
    // 时钟计数器
    // -------------------------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            clk_count <= 0;
        end else begin
            case (state)
                IDLE, DONE: begin
                    clk_count <= 0;
                end

                START, DATA, STOP: begin
                    if (clk_count == CLKS_PER_BIT - 1)
                        clk_count <= 0;
                    else
                        clk_count <= clk_count + 1;
                end

                default: begin
                    clk_count <= 0;
                end
            endcase
        end
    end

    // -------------------------------------------------------------------------
    // 位索引计数器
    // -------------------------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bit_index <= 0;
        end else begin
            if (state == DATA && clk_count == CLKS_PER_BIT - 1)
                bit_index <= bit_index + 1;
            else if (state != DATA)
                bit_index <= 0;
        end
    end

    // -------------------------------------------------------------------------
    // 数据寄存器
    // -------------------------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_data_reg <= 8'h00;
        end else begin
            if (state == IDLE && tx_start)
                tx_data_reg <= tx_data;
        end
    end

    // -------------------------------------------------------------------------
    // UART TX输出逻辑
    // -------------------------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx <= 1'b1;  // UART空闲时为高电平
        end else begin
            case (state)
                IDLE, DONE: begin
                    tx <= 1'b1;
                end

                START: begin
                    tx <= 1'b0;  // 起始位为低
                end

                DATA: begin
                    tx <= tx_data_reg[bit_index];
                end

                STOP: begin
                    tx <= 1'b1;  // 停止位为高
                end

                default: begin
                    tx <= 1'b1;
                end
            endcase
        end
    end

    // -------------------------------------------------------------------------
    // 忙标志逻辑
    // -------------------------------------------------------------------------
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_busy <= 1'b0;
        end else begin
            case (state)
                IDLE: begin
                    tx_busy <= tx_start;
                end
                default: begin
                    tx_busy <= 1'b1;
                end
            endcase
        end
    end

    // -------------------------------------------------------------------------
    // 断言 (用于验证)
    // -------------------------------------------------------------------------
    `ifdef FORMAL
        // 复位后TX应为高
        assert property (@(posedge clk) !rst_n |=> ##1 tx == 1'b1)
            else $error("Reset assertion failed");

        // 在IDLE状态下TX应保持高电平
        assert property (@(posedge clk) state == IDLE |-> tx == 1'b1)
            else $error("TX should be high in IDLE");
    `endif

endmodule

// =============================================================================
// 波形说明
// =============================================================================
//
// 空闲     起始位   D0      D1      ...    D7      停止位   空闲
//  _____     \_____/~~~~~~~\_______/_______/     \_______/
//        |     |       |       |       |             |
//        |<--->|<----->|       |       |             |
//         起始  1位时间  数据位  1位时间  ...       停止位
//
// 每个"位时间" = CLKS_PER_BIT 个时钟周期
//
// =============================================================================
