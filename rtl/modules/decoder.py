from rtl.template_engine import render_template


def generate_decoder(plan, params):

    context = {
        "ADDR_WIDTH": params["ADDR_WIDTH"],
        "bank_bits": plan["bank_address_bits"],
        "local_bits": plan["local_address_bits"]
    }

    return render_template("decoder.v.j2", context)