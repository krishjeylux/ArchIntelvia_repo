import json
import ast
import re


def safe_json_parse(text):

    # ✅ Case 1 — already dict
    if isinstance(text, dict):
        return text

    # ✅ Extract JSON block if wrapped in markdown
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group()
    except:
        pass

    # ✅ Fix Python-style booleans
    text = text.replace("True", "true").replace("False", "false")

    # ✅ Try JSON
    try:
        return json.loads(text)
    except:
        pass

    # ✅ Try Python dict
    try:
        return ast.literal_eval(text)
    except:
        pass

    return None