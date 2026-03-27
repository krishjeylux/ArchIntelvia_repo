# backend/rtl/modules/arbiter.py

def generate_arbiter(plan: dict, params: dict) -> str:

    banks = plan["num_banks"]

    return f"""
module arbiter (
    input clk,
    input rst,
    input [{banks-1}:0] req,
    output reg [{banks-1}:0] grant
);

    reg [{banks-1}:0] pointer;
    integer i;

    always @(posedge clk) begin
        if (rst) begin
            grant <= 0;
            pointer <= 1;  // start with first priority
        end else begin
            grant <= 0;

            // rotate priority
            for (i = 0; i < {banks}; i = i + 1) begin
                if (req[(i + pointer) % {banks}]) begin
                    grant[(i + pointer) % {banks}] <= 1;
                    pointer <= (i + pointer + 1) % {banks};
                    disable for;
                end
            end
        end
    end

endmodule
"""