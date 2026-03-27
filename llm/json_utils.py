import json
import re
import ast


def extract_json_block(text: str) -> str:
    """
    Extract first JSON-like block from text
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def safe_json_parse(text: str):
    """
    Robust parser:
    1. Extract JSON
    2. Try json.loads
    3. Fallback to ast.literal_eval
    """
    try:
        cleaned = extract_json_block(text)

        # Attempt strict JSON
        return json.loads(cleaned)

    except:
        try:
            # Fallback: Python dict → JSON
            return ast.literal_eval(cleaned)
        except:
            return None