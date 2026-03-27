from planner.dse import run_dse, rank_designs, print_dse_results

params = {
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 10,
    "BANKS": 2,
    "PIPELINE_DEPTH": 0
}

results = run_dse(params)

ranked = rank_designs(results, objective="performance")

print_dse_results(ranked[:5])