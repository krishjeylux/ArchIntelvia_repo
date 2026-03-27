# backend/test_planner.py

from planner.planner import generate_architecture_plan
from rtl.generator import generate_rtl


def main():

    # 🔹 STEP 1 — User Input Parameters
    params = {
        "DATA_WIDTH": 32,
        "ADDR_WIDTH": 10,
        "BANKS": 2,
        "PIPELINE_DEPTH": 0,
        "LOW_POWER_MODE": False
    }

    print("\n=== INPUT PARAMETERS ===\n", params)

    # 🔹 STEP 2 — Generate Architecture Plan
    # (This now includes: DSE → Optimization → User Decisions)
    architecture_plan = generate_architecture_plan(params)

    print("\n=== FINAL ARCHITECTURE PLAN ===\n", architecture_plan)

    # 🔹 STEP 3 — Generate RTL + Testbench
    rtl_code = generate_rtl(architecture_plan, params)

    print("\n[✓] RTL and Testbench successfully generated!")

    print("\n📁 Check 'output/' folder for files:")
    print("   - memory_controller.v")
    print("   - tb_memory_controller.v")


if __name__ == "__main__":
    main()