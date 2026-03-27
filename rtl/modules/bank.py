from rtl.template_engine import render_template


def generate_bank(plan, params):

    banks = plan["num_banks"]
    local_addr = plan["local_address_bits"]

    rtl = []

    for i in range(banks):
        context = {
            "bank_id": i,
            "DATA_WIDTH": params["DATA_WIDTH"],
            "LOCAL_ADDR_WIDTH": local_addr
        }

        code = render_template("bank.v.j2", context)
        rtl.append(code)

    return "\n\n".join(rtl)