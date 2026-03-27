from planner.optimizer import optimize_parameters

params = {
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 10,
    "BANKS": 2,
    "PIPELINE_DEPTH": 0
}

result = optimize_parameters(params)

print("\n=== OPTIMIZATION RESULT ===\n")
print(result)