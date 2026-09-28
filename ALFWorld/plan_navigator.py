from llm import egp_llm
from langchain_core.messages import HumanMessage
from task_schema import render_schema

def load_prompt(path):
    with open(path, 'r') as f:
        return f.read()

EE_PROMPT = load_prompt('./prompts/ee_prompt.txt')
PG_PROMPT = load_prompt('./prompts/pg_prompt.txt')

def extract_evidence(trajectory):
    prompt = EE_PROMPT.format(trajectory=trajectory)
    return egp_llm([HumanMessage(content=prompt)], replace_newline=False)

def match_schema(evidence, schema_entries):
    prompt = PG_PROMPT.format(evidence=evidence, schema_entries=schema_entries)
    return egp_llm([HumanMessage(content=prompt)], replace_newline=False)

def build_context(evidence, schema_result):
    context = "[Progress context]\n"
    context += evidence + "\n"
    context += "[Schema grounding]\n" + schema_result + "\n"
    context += "Use this grounded context to choose your next action. Do not claim progress that the evidence does not support."
    return context

def deliberately_think(trial_control, trajectory):
    task_type = trial_control.get_task_type()
    schema_entries = render_schema(task_type)
    evidence = extract_evidence(trajectory)
    schema_result = match_schema(evidence, schema_entries)
    return build_context(evidence, schema_result)
