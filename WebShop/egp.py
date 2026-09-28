from llm import egp_llm
from langchain_core.messages import SystemMessage, HumanMessage
from schema import TASK_TYPE, get_schema

with open("./ee_prompt.txt", 'r') as f:
    EE_PROMPT = f.read()
with open("./pg_prompt.txt", 'r') as f:
    PG_PROMPT = f.read()

def call_llm(prompt):
    message = [
        SystemMessage(content="Follow the syntax of the example closely while taking actions."),
        HumanMessage(content=prompt)
    ]
    return egp_llm(message)

def extract_evidence(instruction, trajectory):
    prompt = EE_PROMPT.replace("<INSTRUCTION>", instruction).replace("<TRAJECTORY>", trajectory)
    return call_llm(prompt)

def match_schema(evidence):
    schema = get_schema(TASK_TYPE)
    schema_text = ""
    for i, entry in enumerate(schema):
        schema_text += f"Entry {i+1}: When [{entry[0]}] and [{entry[1]}], then [{entry[2]}] is applicable.\n"
    prompt = PG_PROMPT.replace("<EVIDENCE>", evidence).replace("<SCHEMA>", schema_text)
    return call_llm(prompt)

def build_progress_context(instruction, trajectory):
    evidence = extract_evidence(instruction, trajectory)
    matched = match_schema(evidence)
    context = f"""[Evidence-grounded progress context]
{evidence}

{matched}"""
    return context
