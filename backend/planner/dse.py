import copy


def generate_design_variants(params: dict):

    variants = []

    # 🔹 Explore BANKS
    for banks in [2, 4, 8]:
        p = copy.deepcopy(params)
        p["BANKS"] = banks
        variants.append(p)

    # 🔹 Explore PIPELINE
    for depth in [0, 1, 2]:
        p = copy.deepcopy(params)
        p["PIPELINE_DEPTH"] = depth
        variants.append(p)

    return variants
def evaluate_design(params: dict):

    banks = params["BANKS"]
    pipeline = params.get("PIPELINE_DEPTH", 0)

    # 🔹 Performance score
    performance = banks * (1 + 0.2 * pipeline)

    # 🔹 Area cost
    area = banks * 10 + pipeline * 2

    # 🔹 Power cost
    power = banks * 5 + pipeline * 1

    return {
        "params": params,
        "performance": performance,
        "area": area,
        "power": power
    }

def run_dse(params: dict):

    variants = generate_design_variants(params)

    results = []

    for v in variants:
        score = evaluate_design(v)
        results.append(score)

    return results

def rank_designs(results, objective="performance"):

    if objective == "performance":
        return sorted(results, key=lambda x: -x["performance"])

    if objective == "area":
        return sorted(results, key=lambda x: x["area"])

    if objective == "power":
        return sorted(results, key=lambda x: x["power"])

    return results
def print_dse_results(results):

    print("\n=== DESIGN SPACE EXPLORATION ===\n")

    for r in results:
        print(f"Params: {r['params']}")
        print(f"  Performance: {r['performance']}")
        print(f"  Area       : {r['area']}")
        print(f"  Power      : {r['power']}")
        print()
