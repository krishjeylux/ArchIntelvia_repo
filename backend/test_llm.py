from llm.llm_client import call_llm
from llm.prompts import PARAM_OPT_PROMPT
from llm.schemas import PARAM_OPT_SCHEMA
from llm.parser import safe_parse
import json

prompt = PARAM_OPT_PROMPT.format(
    user_input=json.dumps({
        "DATA_WIDTH": 32,
        "ADDR_WIDTH": 10,
        "BANKS": 4
    }),
    context="- Do NOT change parameters unless strongly justified- Preserve user intent unless clearly suboptimal"
)

raw_response = call_llm(prompt)

validated = safe_parse(raw_response, PARAM_OPT_SCHEMA)

print(validated)