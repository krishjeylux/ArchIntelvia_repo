# backend/test_planner.py

from planner.planner import generate_architecture_plan
from rtl.generator import generate_rtl


def main():

    # 🔹 STEP 1 — User Input Parameters
    params = {
        
        "BANKS": 8,
    "PIPELINE_DEPTH": 4,
    "LOW_POWER_MODE": False,
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 10
        
    }

    print("\n=== INPUT PARAMETERS ===\n", params)

    # 🔹 STEP 2 — Generate Architecture Plan
    # (This now includes: DSE → Optimization → User Decisions)
    architecture_plan, final_params = generate_architecture_plan(params)

    print("\n=== FINAL ARCHITECTURE PLAN ===\n", architecture_plan)

    # 🔹 STEP 3 — Generate RTL + Testbench
    

    rtl_code = generate_rtl(architecture_plan, final_params)

    print("\n[✓] RTL and Testbench successfully generated!")

    print("\n📁 Check 'output/' folder for files:")
    print("   - memory_controller.v")
    print("   - tb_memory_controller.v")


if __name__ == "__main__":
    main()