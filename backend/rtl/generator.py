# backend/rtl/generator.py

import os

from rtl.modules.top import generate_top
from rtl.modules.decoder import generate_decoder
from rtl.modules.arbiter import generate_arbiter
from rtl.modules.bank import generate_bank
from rtl.modules.pipeline import generate_pipeline
from rtl.modules.power_ctrl import generate_power_ctrl
from rtl.testbench import generate_testbench


def generate_rtl(plan: dict, params: dict) -> str:

    # 🔹 Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    rtl_parts = []

    # 🔹 Generate RTL modules
    rtl_parts.append(generate_top(plan, params))
    rtl_parts.append(generate_decoder(plan, params))
    rtl_parts.append(generate_arbiter(plan, params))
    rtl_parts.append(generate_bank(plan, params))
    rtl_parts.append(generate_pipeline(plan, params))
    rtl_parts.append(generate_power_ctrl(plan, params))

    # 🔹 Combine RTL
    rtl_code = "\n\n".join(rtl_parts)

    # 🔹 Save RTL
    with open("output/memory_controller.v", "w") as f:
        f.write(rtl_code)

    # 🔥 Generate Testbench (separate, clean)
    tb_code = generate_testbench(params)

    with open("output/tb_memory_controller.v", "w") as f:
        f.write(tb_code)

    print("[✓] RTL + Testbench generated in /output")

    return rtl_code