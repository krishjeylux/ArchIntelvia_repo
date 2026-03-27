# backend/rtl/modules/power_ctrl.py

def generate_power_ctrl(plan: dict, params: dict) -> str:

    if not params.get("LOW_POWER_MODE", False):
        return "// Low power disabled"

    return """
module power_ctrl (
    input clk,
    input enable,
    output gated_clk
);

    assign gated_clk = clk & enable;  // simple clock gating

endmodule
"""