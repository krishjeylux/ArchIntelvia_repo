from planner.planner import generate_architecture_plan

params = {
   
    
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 10,
    "BANKS": 2,
    "PIPELINE_DEPTH": 0

}   # impossible split


plan = generate_architecture_plan(params)

print("\n=== FINAL PLAN ===")
print(plan)