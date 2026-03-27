# backend/rtl/modules/decoder.py

def generate_decoder(plan: dict, params: dict) -> str:

    bank_bits = plan["bank_address_bits"]
    local_bits = plan["local_address_bits"]

    return f"""
module decoder (
    input [{params['ADDR_WIDTH']-1}:0] addr,
    output [{bank_bits-1}:0] bank_id,
    output [{local_bits-1}:0] local_addr
);

    assign bank_id = addr[{params['ADDR_WIDTH']-1}:{params['ADDR_WIDTH']-bank_bits}];
    assign local_addr = addr[{local_bits-1}:0];

endmodule
"""