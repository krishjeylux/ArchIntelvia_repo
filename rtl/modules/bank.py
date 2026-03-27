# backend/rtl/modules/bank.py

def generate_bank(plan: dict, params: dict) -> str:

    return f"""
module bank #(
    parameter DATA_WIDTH = {params['DATA_WIDTH']},
    parameter ADDR_WIDTH = {plan['local_address_bits']}
)(
    input clk,
    input we,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    output reg [DATA_WIDTH-1:0] rdata
);

    reg [DATA_WIDTH-1:0] mem [0:(1<<ADDR_WIDTH)-1];

    always @(posedge clk) begin
        if (we)
            mem[addr] <= wdata;

        rdata <= mem[addr];
    end

endmodule
"""