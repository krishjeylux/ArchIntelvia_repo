from planner.planner import generate_architecture_plan

params = {
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 10,
    "BANKS": 4,
    "PIPELINE_DEPTH": 2,
    "LOW_POWER_MODE": True
}

plan = generate_architecture_plan(params)

print("\n=== FINAL PLAN ===")
print(plan)