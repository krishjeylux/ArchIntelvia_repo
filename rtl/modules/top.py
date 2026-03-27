def generate_top(plan: dict, params: dict) -> str:

    banks = plan["num_banks"]
    pipe_depth = plan["pipeline_stages"]

    pipeline_regs = "\n".join([
        f"reg [DATA_WIDTH-1:0] pipe_reg_{i};"
        for i in range(pipe_depth)
    ])

    pipeline_logic = ""

    if pipe_depth > 0:
        pipeline_logic += "always @(posedge clk) begin\n"
        pipeline_logic += "    pipe_reg_0 <= bank_rdata[bank_id];\n"

        for i in range(1, pipe_depth):
            pipeline_logic += f"    pipe_reg_{i} <= pipe_reg_{i-1};\n"

        pipeline_logic += "end\n"

        final_output = f"pipe_reg_{pipe_depth-1}"
    else:
        final_output = "bank_rdata[bank_id]"

    return f"""
module memory_controller #(
    parameter DATA_WIDTH = {params['DATA_WIDTH']},
    parameter ADDR_WIDTH = {params['ADDR_WIDTH']}
)(
    input clk,
    input rst,
    input we,
    input [ADDR_WIDTH-1:0] addr,
    input [DATA_WIDTH-1:0] wdata,
    output [DATA_WIDTH-1:0] rdata
);

    wire [{plan['bank_address_bits']-1}:0] bank_id;
    wire [{plan['local_address_bits']-1}:0] local_addr;

    wire [DATA_WIDTH-1:0] bank_rdata [{banks-1}:0];

    {pipeline_regs}

    decoder u_decoder (
        .addr(addr),
        .bank_id(bank_id),
        .local_addr(local_addr)
    );

    genvar i;
    generate
        for (i = 0; i < {banks}; i = i + 1) begin : BANKS

            bank u_bank (
                .clk(clk),
                .we(we && (bank_id == i)),
                .addr(local_addr),
                .wdata(wdata),
                .rdata(bank_rdata[i])
            );

        end
    endgenerate

    {pipeline_logic}

    assign rdata = {final_output};

endmodule
"""