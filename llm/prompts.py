# backend/llm/prompts.py

PARAM_OPT_PROMPT = """
You are an expert hardware architect specializing in memory controller design.

Your task:
Analyze the given parameters and suggest improvements ONLY if they provide clear benefits.

Context:
{context}

User Parameters:
{params}

STRICT RULES:
- Do NOT introduce new parameters
- Do NOT remove parameters
- Do NOT make invalid configurations
- Only suggest meaningful improvements
- If unsure, DO NOT change anything

Focus on:
- Performance (parallelism, throughput)
- Latency (pipeline, access delay)
- Power efficiency (clock gating, low power modes)

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "user_params": {params},
  "optimized_params": {{}},
  "changes": [
    {{
      "parameter": "...",
      "from": ...,
      "to": ...,
      "reason": "..."
    }}
  ],
  "recommendation": "optimized" OR "no_change"
}}

If no improvement is needed:
- return same parameters
- set recommendation = "no_change"
"""

ARCH_PLAN_PROMPT = """
You are a hardware architect.

Given memory controller parameters:

{params}

And design knowledge:

{context}

Task:
Generate a high-level architecture plan.

Rules:
- Derive bank structure from BANKS
- Split address into bank bits + local address bits
- Choose appropriate arbiter
- Include pipeline stages based on PIPELINE_DEPTH
- Include power features if LOW_POWER_MODE is true
- Use the provided context as the primary source of truth
- Do not make assumptions beyond the context unless necessary

Output STRICT JSON:

{{
  "num_banks": integer,
  "bank_address_bits": integer,
  "local_address_bits": integer,
  "pipeline_stages": integer,
  "arbiter_type": "round_robin" OR "priority",
  "low_power_features": ["clock_gating"] OR [],
  "modules": ["top", "arbiter", "decoder", "bank_array", "pipeline"]
}}

IMPORTANT:
- Return ONLY JSON
- No explanation
"""
