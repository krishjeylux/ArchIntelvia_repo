from rtl.template_engine import render_template


def generate_arbiter(plan, params):

    context = {
        "num_banks": plan["num_banks"],
        "pipeline_depth": params.get("PIPELINE_DEPTH", 0)
    }

    return render_template("arbiter.v.j2", context)