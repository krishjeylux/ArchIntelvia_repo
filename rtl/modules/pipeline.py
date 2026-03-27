# backend/rtl/modules/pipeline.py

def generate_pipeline(plan: dict, params: dict) -> str:

    depth = plan["pipeline_stages"]

    if depth == 0:
        return "// No pipeline"

    regs = "\n".join([
        f"reg [DATA_WIDTH-1:0] pipe_reg_{i};"
        for i in range(depth)
    ])

    logic = "always @(posedge clk) begin\n"
    logic += "    pipe_reg_0 <= in_data;\n"

    for i in range(1, depth):
        logic += f"    pipe_reg_{i} <= pipe_reg_{i-1};\n"

    logic += "end\n"

    return f"""
module pipeline (
    input clk,
    input [DATA_WIDTH-1:0] in_data,
    output [DATA_WIDTH-1:0] out_data
);

{regs}

{logic}

assign out_data = pipe_reg_{depth-1};

endmodule
"""