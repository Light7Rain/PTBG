from env_history import EnvironmentHistory
from schema import CRAFT_SCHEMA
from egp import extract_evidence, match_schema, build_context, decide

def deliberate_think(env_history:EnvironmentHistory,env):
    inventory,_,_,_,_=env.step("inventory")
    env_evidence,agent_evidence=extract_evidence(env_history,inventory)
    matched=match_schema(env_evidence,agent_evidence,CRAFT_SCHEMA)
    context=build_context(env_evidence,agent_evidence,matched)
    rationale=decide(env_history,context)
    return rationale
