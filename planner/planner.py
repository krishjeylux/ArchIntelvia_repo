import json
from llm.llm_client import call_llm
from llm.prompts import ARCH_PLAN_PROMPT
from llm.schemas import ARCH_PLAN_SCHEMA
from llm.parser import safe_parse
from planner.validator import compute_address_split, enforce_constraints
from rag.retriever import retrieve_context
from planner.optimizer import optimize_parameters
from planner.dse import run_dse, rank_designs
def handle_dse_selection(params):

    print("\n=== RUNNING DESIGN SPACE EXPLORATION ===\n")

    results = run_dse(params)

    # Rank by performance (default)
    ranked = rank_designs(results, objective="performance")

    top_designs = ranked[:3]

    print("Top Design Candidates:\n")

    for i, d in enumerate(top_designs):
        print(f"Option {i+1}:")
        print(f"  Params      : {d['params']}")
        print(f"  Performance : {d['performance']}")
        print(f"  Area        : {d['area']}")
        print(f"  Power       : {d['power']}")
        print()

    choice = input("Select design (1/2/3) or press Enter to skip: ").strip()

    if choice in ["1", "2", "3"]:
        selected = top_designs[int(choice)-1]["params"]
        print("\n[INFO] Using selected DSE configuration\n")
        return selected

    print("\n[INFO] Skipping DSE, using original params\n")
    return params
def handle_user_decision(opt_result, original_params):

    if opt_result.get("recommendation") == "no_change":
        return original_params

    print("\n=== OPTIMIZATION SUGGESTIONS ===\n")

    for change in opt_result["changes"]:
        print(f"{change['parameter']}: {change['from']} → {change['to']}")
        print(f"  Reason: {change['reason']}\n")

    # 🔥 NEW: Tradeoff display
    print("=== TRADEOFF ANALYSIS ===\n")

    analysis = opt_result.get("analysis", {})

    print("Performance :", analysis.get("performance", "N/A"))
    print("Area        :", analysis.get("area", "N/A"))
    print("Power       :", analysis.get("power", "N/A"))
    print("Complexity  :", analysis.get("complexity", "N/A"))

    print("\nTradeoff:", opt_result.get("tradeoff", "N/A"))

    choice = input("\nApply optimized parameters? (y/n): ").strip().lower()

    if choice == "y":
        print("\n[INFO] Using optimized parameters\n")
        return opt_result["optimized_params"]
    else:
        print("\n[INFO] Using original parameters\n")
        return original_params

def generate_architecture_plan(params: dict) -> dict:
    params = handle_dse_selection(params)
    # 🔥 STEP 0 — PARAM OPTIMIZATION
    opt_result = optimize_parameters(params)

    print("\n=== OPTIMIZATION RESULT ===\n", opt_result)

    # 🔥 STEP 0.5 — USER DECISION
    final_params = handle_user_decision(opt_result, params)

    # 🔥 STEP 1 — Build query for RAG
    query = f"""
    Memory controller design with:
    DATA_WIDTH={final_params.get("DATA_WIDTH")}
    ADDR_WIDTH={final_params.get("ADDR_WIDTH")}
    BANKS={final_params.get("BANKS")}
    PIPELINE_DEPTH={final_params.get("PIPELINE_DEPTH")}
    LOW_POWER_MODE={final_params.get("LOW_POWER_MODE")}
    """

    # 🔥 STEP 2 — Retrieve context
    context = retrieve_context(final_params)

    # Debug (optional)
    print("\n=== RAG CONTEXT ===\n", context)

    # 🔥 STEP 3 — LLM call with context
    prompt = ARCH_PLAN_PROMPT.format(
        params=json.dumps(final_params),
        context=context
    )

    raw_output = call_llm(prompt)

    from llm.json_utils import safe_json_parse

    parsed = safe_json_parse(raw_output)

    if parsed is None:
        raise ValueError("Failed to parse LLM architecture output")

    validated = parsed

    # 🔥 STEP 4 — Deterministic corrections
    split = compute_address_split(final_params)

    validated["bank_address_bits"] = split["bank_address_bits"]
    validated["local_address_bits"] = split["local_address_bits"]

    validated["num_banks"] = final_params["BANKS"]
    validated["pipeline_stages"] = final_params.get("PIPELINE_DEPTH", 0)

    # 🔥 STEP 5 — Enforce constraints
    final_plan = enforce_constraints(validated, final_params)

    return final_plan