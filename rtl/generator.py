# backend/rtl/generator.py

from rtl.modules.top import generate_top
from rtl.modules.decoder import generate_decoder
from rtl.modules.arbiter import generate_arbiter

from rtl.modules.bank import generate_bank
from rtl.modules.pipeline import generate_pipeline
from rtl.modules.power_ctrl import generate_power_ctrl
def generate_rtl(plan: dict, params: dict) -> str:

    rtl_parts = []

    rtl_parts.append(generate_top(plan, params))
    rtl_parts.append(generate_decoder(plan, params))
    rtl_parts.append(generate_arbiter(plan, params))
    rtl_parts.append(generate_bank(plan, params))   # ⭐ NEW
    rtl_parts.append(generate_pipeline(plan, params))
    rtl_parts.append(generate_power_ctrl(plan, params))
    return "\n\n".join(rtl_parts)