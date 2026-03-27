# backend/llm/schemas.py

# -------------------------------
# PARAMETER OPTIMIZATION SCHEMA
# -------------------------------

PARAM_OPT_SCHEMA = {
    "type": "object",
    "properties": {
        "user_params": {"type": "object"},
        "optimized_params": {"type": "object"},
        "changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "parameter": {"type": "string"},
                    "from": {},
                    "to": {},
                    "reason": {"type": "string"}
                },
                "required": ["parameter", "from", "to", "reason"]
            }
        },
        "recommendation": {
            "type": "string",
            "enum": ["original", "optimized"]
        }
    },
    "required": ["user_params", "optimized_params", "changes", "recommendation"]
}


# -------------------------------
# ARCHITECTURE PLAN SCHEMA ⭐
# -------------------------------

ARCH_PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "num_banks": {"type": "integer"},
        "bank_address_bits": {"type": "integer"},
        "local_address_bits": {"type": "integer"},
        "pipeline_stages": {"type": "integer"},
        "arbiter_type": {"type": "string"},
        "low_power_features": {
            "type": "array",
            "items": {"type": "string"}
        },
        "modules": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [
        "num_banks",
        "bank_address_bits",
        "local_address_bits",
        "pipeline_stages",
        "arbiter_type",
        "modules"
    ]
}