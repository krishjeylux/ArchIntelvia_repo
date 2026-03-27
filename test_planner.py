from planner.planner import generate_architecture_plan

params = {
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 2,
    "BANKS": 4   # impossible split
}

plan = generate_architecture_plan(params)

print("\n=== FINAL PLAN ===")
print(plan)