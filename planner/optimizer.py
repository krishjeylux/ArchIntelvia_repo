import math

from rag.retriever import retrieve_context
from llm.llm_client import call_llm
from llm.prompts import PARAM_OPT_PROMPT
from llm.json_utils import safe_json_parse


# =========================
# 🔧 HELPER FUNCTIONS
# =========================

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


def sanitize_result(result, original_params):
    optimized = result.get("optimized_params", {})

    # Fill missing keys
    for key in original_params:
        if key not in optimized:
            optimized[key] = original_params[key]

    # Remove extra keys
    optimized = {k: optimized[k] for k in original_params}

    result["optimized_params"] = optimized

    # 🔥 Ensure new fields exist
    result.setdefault("analysis", {})
    result.setdefault("tradeoff", "Not specified")

    return result


def enforce_optimizer_constraints(result, original_params):
    optimized = result.get("optimized_params", {})

    banks = optimized.get("BANKS", original_params["BANKS"])
    addr_width = optimized.get("ADDR_WIDTH", original_params["ADDR_WIDTH"])

    # 🔒 Rule 1 — BANKS must be power of 2
    if not is_power_of_two(banks):
        print("[WARN] Invalid BANKS → reverting")
        optimized["BANKS"] = original_params["BANKS"]

    # 🔒 Rule 2 — Address feasibility
    bank_bits = int(math.log2(optimized["BANKS"]))

    if addr_width <= bank_bits:
        print("[WARN] Invalid ADDR_WIDTH for BANKS → reverting")
        optimized["BANKS"] = original_params["BANKS"]

    result["optimized_params"] = optimized
    return result


def rebuild_changes(result, original_params):
    changes = []

    for key in original_params:
        old = original_params[key]
        new = result["optimized_params"].get(key, old)

        if old != new:
            changes.append({
                "parameter": key,
                "from": old,
                "to": new,
                "reason": "Auto-detected change"
            })

    result["changes"] = changes

    if changes:
        result["recommendation"] = "optimized"
    else:
        result["recommendation"] = "no_change"

    return result


# =========================
# 🚀 MAIN FUNCTION
# =========================

def optimize_parameters(params: dict) -> dict:

    # 🔹 STEP 1 — RAG context
    context = retrieve_context(params)

    # 🔹 STEP 2 — Build prompt
    prompt = PARAM_OPT_PROMPT.format(
        context=context,
        params=params
    )

    # 🔹 STEP 3 — Call LLM
    response = call_llm(prompt)

    print("\n[DEBUG] LLM RAW RESPONSE:\n", response)

    # 🔹 STEP 4 — Parse response
    print("\n[DEBUG] Using NEW PARSER")
    result = safe_json_parse(response)

    if result is None:
        print("[ERROR] Failed to parse LLM response")
        return {
            "user_params": params,
            "optimized_params": params,
            "changes": [],
            "recommendation": "no_change"
        }

    # 🔹 STEP 5 — Sanitize output
    result = sanitize_result(result, params)

    # 🔹 STEP 6 — Enforce constraints
    result = enforce_optimizer_constraints(result, params)

    # 🔹 STEP 7 — Rebuild changes (final truth)
    result = rebuild_changes(result, params)

    return result