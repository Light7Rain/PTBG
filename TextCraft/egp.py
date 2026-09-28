from langchain_core.messages import SystemMessage,HumanMessage
from llm import react_llm
from utils import get_info

with open("./ee_prompt.txt",'r') as f:
    EE_PROMPT=f.read()
with open("./pg_prompt.txt",'r') as f:
    PG_PROMPT=f.read()
with open("./decision_prompt.txt",'r') as f:
    DECISION_PROMPT=f.read()

def extract_evidence(env_history,inventory):
    commands,target=get_info(env_history.start_obs)
    prompt=EE_PROMPT.replace("<TARGET>",target).replace("<RECIPES>",commands).replace("<INVENTORY>",inventory)
    message=[
        SystemMessage(content="Follow the syntax of the examples closely when taking actions."),
        HumanMessage(content=prompt)
    ]
    response=react_llm(message).strip()
    parts=response.split("##")
    env_evidence=parts[0].replace("[Environment evidence]:","").strip()
    agent_evidence=parts[1].replace("[Agent state evidence]:","").strip() if len(parts)>1 else ""
    return env_evidence,agent_evidence

def match_schema(env_evidence,agent_evidence,schema):
    entries="\n".join([f"{i}. {e}" for i,e in enumerate(schema)])
    prompt=PG_PROMPT.replace("<ENV_EVIDENCE>",env_evidence).replace("<AGENT_EVIDENCE>",agent_evidence).replace("<ENTRIES>",entries)
    message=[
        SystemMessage(content="Follow the syntax of the examples closely when taking actions."),
        HumanMessage(content=prompt)
    ]
    response=react_llm(message).strip()
    if "no reliable match" in response:
        return None
    for ch in response:
        if ch.isdigit():
            idx=int(ch)
            if 0<=idx<len(schema):
                return schema[idx]
    return None

def build_context(env_evidence,agent_evidence,matched):
    context=f"[Environment evidence]\n{env_evidence}\n\n[Agent state evidence]\n{agent_evidence}\n\n[Schema grounding result]\n"
    if matched is not None:
        context+=f"when [{matched[0]}] and [{matched[1]}], the action [{matched[2]}] is applicable"
    else:
        context+="no schema entry is reliably supported; choose the next action based on the evidence above"
    return context

def decide(env_history,context):
    prompt=DECISION_PROMPT.replace("<TRAJECTORY>",env_history.human_message).replace("<CONTEXT>",context)
    message=[
        SystemMessage(content="Follow the syntax of the examples closely when taking actions."),
        HumanMessage(content=prompt)
    ]
    return react_llm(message).strip()
