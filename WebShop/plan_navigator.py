from llm import think_llm
from langchain_core.messages import SystemMessage, HumanMessage
from egp import build_progress_context

with open("./think_prompt.txt", 'r') as f:
    THINK_PROMPT = f.read()

def deliberately_think(trial_control, trajectory):
    ins = trial_control.ins
    keywords = trial_control.keywords
    obs = trial_control.current_context
    context = build_progress_context(ins, trajectory)
    prompt = THINK_PROMPT.replace("<INSTRUCTION>", ins).replace("<KEYWORDS>", keywords).replace("<OBSERVATION>", obs).replace("<CONTEXT>", context)
    message = [
        SystemMessage(content="Follow the syntax of the example closely while taking actions."),
        HumanMessage(content=prompt)
    ]
    thought = think_llm(message)
    return thought
