# test_rtl.py

from planner.planner import generate_architecture_plan
from rtl.generator import generate_rtl

params = {
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 10,
    "BANKS": 4,
    "PIPELINE_DEPTH": 2,
    "LOW_POWER_MODE": True
}

plan = generate_architecture_plan(params)

rtl_code = generate_rtl(plan, params)

print("\n=== GENERATED RTL ===\n")
print(rtl_code)