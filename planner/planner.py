import json
from llm.llm_client import call_llm
from llm.prompts import ARCH_PLAN_PROMPT
from llm.schemas import ARCH_PLAN_SCHEMA
from llm.parser import safe_parse
from planner.validator import compute_address_split, enforce_constraints
from rag.retriever import retrieve_context


def generate_architecture_plan(params: dict) -> dict:

    # 🔥 STEP 1 — Build query for RAG
    query = f"""
    Memory controller design with:
    DATA_WIDTH={params.get("DATA_WIDTH")}
    ADDR_WIDTH={params.get("ADDR_WIDTH")}
    BANKS={params.get("BANKS")}
    PIPELINE_DEPTH={params.get("PIPELINE_DEPTH")}
    LOW_POWER_MODE={params.get("LOW_POWER_MODE")}
    """

    # 🔥 STEP 2 — Retrieve context
    context = retrieve_context(params)

    # Debug (optional)
    print("\n=== RAG CONTEXT ===\n", context)

    # 🔥 STEP 3 — LLM call with context
    prompt = ARCH_PLAN_PROMPT.format(
        params=json.dumps(params),
        context=context
    )

    raw_output = call_llm(prompt)

    validated = safe_parse(raw_output, ARCH_PLAN_SCHEMA)

    # 🔥 STEP 4 — Deterministic corrections
    split = compute_address_split(params)

    validated["bank_address_bits"] = split["bank_address_bits"]
    validated["local_address_bits"] = split["local_address_bits"]

    validated["num_banks"] = params["BANKS"]
    validated["pipeline_stages"] = params.get("PIPELINE_DEPTH", 0)

    # 🔥 STEP 5 — Enforce constraints
    final_plan = enforce_constraints(validated, params)

    return final_plan