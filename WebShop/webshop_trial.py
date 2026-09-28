from env_history import EnvironmentHistory
from typing import Any, Dict, List, Tuple
from utils import *
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
sys.path.append(project_root)
from trial_control import TrialControl
from web_agent_site.envs import WebAgentTextEnv
from WebShop.plan_navigator import deliberately_think
from llm import react_llm

with open("./base_prompt_gpt.txt", 'r') as f:
    BASE_PROMPT = f.read()

def webshop_run(env, base_prompt:str,instruction:str,memory: List[str], to_print:bool) -> Tuple[EnvironmentHistory, bool]:
    if len(memory) > 3:
        env_history = EnvironmentHistory(base_prompt,instruction,memory[-3:], [])
    else:
        env_history = EnvironmentHistory(base_prompt,instruction ,memory, [])
    
    trial_control=TrialControl(instruction)
    keywords=react_llm(trial_control.generate_keywords_message(instruction))
    keywords=keywords.strip()
    keywords=keywords.replace(" and "," ")
    keywords=keywords.replace(" the "," ")
    keywords=keywords.replace(" for "," ")
    trial_control.set_keywords(keywords)
    action_search=f"search[{keywords}]"
    env_history.set_base_prompt(action_search)
    product_all, reward, done, _ = env.step(action_search)
    product_all=parse_observation(product_all)
    env_history.add("action",action_search)
    env_history.add("observation",product_all)
    products=trial_control.get_product_all(product_all,"")
    trial_control.update_obs(product_all)
    env_history.reset_message(products)
    message=env_history.create_message()
    current_item=""
    reward_now=0
    cur_step=0
    for _ in range(0,12):
        action=react_llm(message)
        action=parse_answer(action)
        if action.startswith("think"):
            thought=deliberately_think(trial_control,env_history.human_message)
            env_history.add_message(thought,"OK.\n")
            env_history.add("action", thought)
            env_history.add("observation","OK.\n")
            cur_step+=1
            message=env_history.create_message()
            trial_control.update_obs("OK.")    
            continue
        try:
            observation, reward, done, _ = env.step(action)
        except AssertionError:
            observation = 'Invalid action!'
        reward_now=reward
        if done:
            env_history.add("action",action)
            env_history.add("observation",observation)
            return env_history, reward_now
        observation=parse_observation(observation)
        trial_control.update_obs(observation)

        if trial_control.check_stage()==0:
            p=trial_control.get_product_all(observation,current_item)
            env_history.add("action", action)
            env_history.add("observation",observation)
            env_history.reset_message(p)
            message=env_history.create_message()
            continue
        if observation.startswith("Invalid"):
            env_history.add("action", action)
            env_history.add("observation","Invalid action!\n")
            env_history.add_message(action,"Invalid action!\n")
            trial_control.update_obs("Invalid action!\n")
            thought=deliberately_think(trial_control,env_history.human_message)
            env_history.add("action", thought)
            env_history.add("observation","OK.\n")
            env_history.add_message(thought,"OK.\n")
            trial_control.update_obs("OK.\n")
            cur_step+=2
            message=env_history.create_message()
            continue
        else:
            if done:
                env_history.add("action",action)
                env_history.add("observation",observation)
                return env_history, reward_now

            cur_step+=1
            env_history.add("action", action)
            env_history.add("observation",observation)
            env_history.add_message(action,observation)
            trial_control.update_obs(observation)
            message=env_history.create_message()
        continue
    return env_history, reward_now
def run_trial(
        trial_log_path: str,
        world_log_path: str,
        trial_idx: int,
        env_configs: List[Dict[str, Any]],
        use_memory: bool
    ) -> List[Dict[str, Any]]:
    env=WebAgentTextEnv(observation_mode="text_rich", human_goals=True)

    num_successes: int = 0
    num_additional_successes: int = 0
    num_envs: int = len(env_configs)
    reward_total=0

    for z, env_config in enumerate(env_configs):
        env.reset(z)
        observation = env.observation
        observation=observation.replace("WebShop\n", "", 1).strip()
        ins=env.get_instruction_text()[13:].strip()
        prompt=f"""You are an online shopping agent. You need to take an action on a text-based online shopping website, based on a shopping instruction and current webpage results.Your actions should follow the format below:
1. click[button]
2. think[thoughts]

Here is a demonstration for you to follow.
{BASE_PROMPT}

Your response should follow the structure of the example above, with the appropriate actions and thoughts.
Now, you task is as below.

{observation}"""
        print(f"using webshop environment: {z}",'\n')

        if env_config["is_success"]:
            num_successes += 1
            with open(world_log_path, 'a') as wf:
                wf.write(f'Environment #{z} Trial #{trial_idx}: SUCCESS\n')
            with open(trial_log_path, 'a') as wf:
                wf.write(f'\n#####\n\nEnvironment #{z}: Success\n\n#####\n')
            continue

        try:
            final_env_history, reward = webshop_run(env,prompt,ins,env_config["memory"] if use_memory else [], to_print=False)
            is_success=False
            if reward>0:
                status_str: str = f'Environment #{z} Trial #{trial_idx}: SUCCESS'
                env_configs[z]["is_success"] = False
                env_configs[z]["reward"]=reward
                reward_total+=reward
                if reward==1.0:
                    num_successes += 1
                    num_additional_successes += 1
                    is_success=True
            else:
                status_str: str = f'Environment #{z} Trial #{trial_idx}: FAIL'
            with open(trial_log_path, 'a') as wf:
                wf.write(f'\n#####\n\nEnvironment #{z}:\n{str(final_env_history)}\n\nSTATUS: {"OK" if is_success else "FAIL"}\n\n#####\n')

        except AssertionError:
            status_str: str = f'Environment #{z} Trial #{trial_idx}: FAIL'
            with open(trial_log_path, 'a') as wf:
                wf.write(f'\n#####\n\nEnvironment #{z}:\nAssertion Error\n\nSTATUS: FAIL\n\n#####\n')
        with open(world_log_path, 'a') as f:
            f.write(status_str + '\n')
    log_str: str = f"""
-----
SUCCESS: {num_successes}
ADDITIONAL SUCCESS: {num_additional_successes}
FAIL: {num_envs - num_successes}
TOTAL: {num_envs}
ACCURACY: {round(num_successes / num_envs, 2)}
REWARD TOTAL: {reward_total} / {num_envs}
-----"""
    with open(trial_log_path, 'a') as wf:
        wf.write(log_str)
    with open(world_log_path, 'a') as wf:
        wf.write(log_str + '\n')

    return env_configs
