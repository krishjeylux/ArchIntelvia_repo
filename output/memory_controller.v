
module memory_controller #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 10
)(
    input clk,
    input rst,
    input we,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    output [DATA_WIDTH-1:0] rdata
);

    wire [1:0] bank_id;
    wire [7:0] local_addr;

    wire [DATA_WIDTH-1:0] bank_rdata [3:0];

    

    decoder u_decoder (
        .addr(addr),
        .bank_id(bank_id),
        .local_addr(local_addr)
    );

    genvar i;
    generate
        for (i = 0; i < 4; i = i + 1) begin : BANKS

            bank u_bank (
                .clk(clk),
                .we(we && (bank_id == i)),
                .addr(local_addr),
                .wdata(wdata),
                .rdata(bank_rdata[i])
            );

        end
    endgenerate

    

    assign rdata = bank_rdata[bank_id];

endmodule



module decoder (
    input [9:0] addr,
    output [1:0] bank_id,
    output [7:0] local_addr
);

    assign bank_id = addr[9:8];
    assign local_addr = addr[7:0];

endmodule



module arbiter (
    input clk,
    input rst,
    input [3:0] req,
    output reg [3:0] grant
);

    reg [3:0] pointer;
    integer i;

    always @(posedge clk) begin
        if (rst) begin
            grant <= 0;
            pointer <= 1;  // start with first priority
        end else begin
            grant <= 0;

            // rotate priority
            for (i = 0; i < 4; i = i + 1) begin
                if (req[(i + pointer) % 4]) begin
                    grant[(i + pointer) % 4] <= 1;
                    pointer <= (i + pointer + 1) % 4;
                    disable for;
                end
            end
        end
    end

endmodule


module bank #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 
)(
    input clk,
    input rst,
    input we,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    output reg [DATA_WIDTH-1:0] rdata
);

    reg [DATA_WIDTH-1:0] mem [0:(1<<ADDR_WIDTH)-1];

    always @(posedge clk) begin
        if (we) begin
            mem[addr] <= wdata;
        end
        rdata <= mem[addr];
    end

endmodule

module bank #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 
)(
    input clk,
    input rst,
    input we,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    output reg [DATA_WIDTH-1:0] rdata
);

    reg [DATA_WIDTH-1:0] mem [0:(1<<ADDR_WIDTH)-1];

    always @(posedge clk) begin
        if (we) begin
            mem[addr] <= wdata;
        end
        rdata <= mem[addr];
    end

endmodule

module bank #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 
)(
    input clk,
    input rst,
    input we,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    output reg [DATA_WIDTH-1:0] rdata
);

    reg [DATA_WIDTH-1:0] mem [0:(1<<ADDR_WIDTH)-1];

    always @(posedge clk) begin
        if (we) begin
            mem[addr] <= wdata;
        end
        rdata <= mem[addr];
    end

endmodule

module bank #(
    parameter DATA_WIDTH = 32,
    parameter ADDR_WIDTH = 
)(
    input clk,
    input rst,
    input we,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    output reg [DATA_WIDTH-1:0] rdata
);

    reg [DATA_WIDTH-1:0] mem [0:(1<<ADDR_WIDTH)-1];

    always @(posedge clk) begin
        if (we) begin
            mem[addr] <= wdata;
        end
        rdata <= mem[addr];
    end

endmodule

// No pipeline

// Low power disabled