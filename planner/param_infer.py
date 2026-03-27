import json
from llm.llm_client import call_llm
from llm.json_utils import safe_json_parse
from llm.prompts import PARAM_INFER_PROMPT
from rag.retriever import retrieve_context


def infer_parameters(params: dict):

    original = params.copy()

    # 🔹 Step 1 — RAG context
    context = retrieve_context(params)

    # 🔹 Step 2 — Call LLM
    prompt = PARAM_INFER_PROMPT.format(
        params=json.dumps(params),
        context=context
    )

    response = call_llm(prompt)

    parsed = safe_json_parse(response)

    if parsed is None:
        print("[WARN] LLM inference failed, using defaults")
        return apply_defaults(params)

    inferred = parsed.get("inferred_params", {})

    # 🔹 Step 3 — Merge
    final = params.copy()

    for k, v in inferred.items():
        if k not in final:
            final[k] = v

    # 🔹 Step 4 — Fill remaining defaults
    final = apply_defaults(final)

    print_inference(original, final)

    return final


# -------------------------
# Defaults fallback
# -------------------------

def apply_defaults(params):

    defaults = {
        "DATA_WIDTH": 32,
        "ADDR_WIDTH": 10,
        "BANKS": 4,
        "PIPELINE_DEPTH": 1,
        "LOW_POWER_MODE": False
    }

    for k, v in defaults.items():
        if k not in params:
            params[k] = v

    return params


# -------------------------
# Debug print
# -------------------------

def print_inference(original, final):

    print("\n=== PARAMETER INFERENCE ===\n")

    for k in final:
        if k not in original:
            print(f"{k} = {final[k]} (inferred)")

    print()