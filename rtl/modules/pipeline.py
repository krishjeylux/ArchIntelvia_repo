from rtl.template_engine import render_template


def generate_pipeline(plan, params):

    context = {
        "DATA_WIDTH": params["DATA_WIDTH"],
        "stages": plan.get("pipeline_stages", 0)
    }

    return render_template("pipeline.v.j2", context)