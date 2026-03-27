# backend/planner/planner.py

import json
from llm.llm_client import call_llm
from llm.prompts import ARCH_PLAN_PROMPT
from llm.schemas import ARCH_PLAN_SCHEMA
from llm.parser import safe_parse
from planner.validator import compute_address_split, enforce_constraints


def generate_architecture_plan(params: dict, context: str = "") -> dict:

    # Step 1: Get LLM output
    prompt = ARCH_PLAN_PROMPT.format(
        params=json.dumps(params),
        context=context
    )

    raw_output = call_llm(prompt)

    validated = safe_parse(raw_output, ARCH_PLAN_SCHEMA)

    # 🔥 Step 2: FORCE CORRECT VALUES (CRITICAL)
    split = compute_address_split(params)

    validated["bank_address_bits"] = split["bank_address_bits"]
    validated["local_address_bits"] = split["local_address_bits"]

    # 🔥 Also enforce num_banks (don’t trust LLM)
    validated["num_banks"] = params["BANKS"]

    # 🔥 enforce pipeline stages
    validated["pipeline_stages"] = params.get("PIPELINE_DEPTH", 0)
    final_plan = enforce_constraints(validated, params)
    return final_plan