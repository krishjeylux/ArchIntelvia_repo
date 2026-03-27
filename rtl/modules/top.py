from rtl.template_engine import render_template


def generate_top(plan, params):

    context = {
        "DATA_WIDTH": params["DATA_WIDTH"],
        "ADDR_WIDTH": params["ADDR_WIDTH"],
        "num_banks": plan["num_banks"],
        "bank_bits": plan["bank_address_bits"],
        "local_bits": plan["local_address_bits"]
    }

    return render_template("top.v.j2", context)