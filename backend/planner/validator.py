# backend/planner/validator.py
import math

def compute_address_split(params: dict) -> dict:
    banks = params["BANKS"]
    addr_width = params["ADDR_WIDTH"]

    # Check power of 2
    if (banks & (banks - 1)) != 0:
        raise ValueError("BANKS must be a power of 2")

    bank_bits = int(math.log2(banks))
    local_bits = addr_width - bank_bits

    if local_bits <= 0:
        raise ValueError("Invalid address split")

    return {
        "bank_address_bits": bank_bits,
        "local_address_bits": local_bits
    }
def validate_plan(plan: dict) -> dict:
    """
    Apply engineering sanity checks
    """

    # Example rules

    if plan["num_banks"] <= 0:
        raise ValueError("Invalid number of banks")

    if plan["pipeline_stages"] < 0:
        raise ValueError("Invalid pipeline stages")

    if plan["arbiter_type"] not in ["round_robin", "priority"]:
        raise ValueError("Invalid arbiter type")

    return plan

def enforce_constraints(plan: dict, params: dict) -> dict:
    """
    Ensure architecture correctness
    """

    # Address consistency check
    if plan["bank_address_bits"] + plan["local_address_bits"] != params["ADDR_WIDTH"]:
        raise ValueError("Address split mismatch")

    # Bank consistency
    if plan["num_banks"] != params["BANKS"]:
        raise ValueError("Bank count mismatch")

    # Pipeline consistency
    if plan["pipeline_stages"] != params.get("PIPELINE_DEPTH", 0):
        raise ValueError("Pipeline mismatch")

    return plan