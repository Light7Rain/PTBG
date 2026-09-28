import os
import sys
import json
import yaml
import importlib
import alfworld
import time
from alfworld.agents.environment import get_environment
from env_history import EnvironmentHistory
from trial_control import TrialControl
from typing import List, Dict, Any, Tuple
from llm import react_llm
from plan_navigator import deliberately_think
from utils import *

FOLDER = './prompts'
PROMPT_FILE = 'alfworld_3prompts.json'

with open(os.path.join(FOLDER, PROMPT_FILE), 'r') as f:
    d = json.load(f)

def process_ob(ob):
    if ob.startswith('You arrive at loc '):
        ob = ob[ob.find('. ')+2:]    
    return ob

def alfworld_run(env, prompt,memory: List[str], to_print=False, ob='') -> Tuple[EnvironmentHistory, bool]:
    if to_print:
        print(ob)
        sys.stdout.flush()

    env_history = EnvironmentHistory(prompt,ob, memory, [])
    trial_control=TrialControl(ob)
    cur_step = 0
    message=env_history.create_message()
    while cur_step < 39:
        action=react_llm(message)
        action=action.strip()
        action=parse_action(action)
        if action.startswith('think'):
            context=deliberately_think(trial_control, env_history.trajectory)
            env_history.add_message("context", context)
            cur_step+=1
            message=env_history.create_message()
            continue
        observation, _, done, info = env.step([action])
        observation, _, done = process_ob(observation[0]), info['won'][0], done[0]
        env_history.add("action", action)
        env_history.add("observation", observation)
        env_history.add_message("action",f"> {action}")
        env_history.add_message("observation",f"{observation}")
        if observation.startswith('Nothing'):
            context=deliberately_think(trial_control, env_history.trajectory)
            env_history.add_message("context", context)
            cur_step+=2
            message=env_history.create_message()
            continue
        else:
            if done:
                return env_history, True
            cur_step+=1
            message=env_history.create_message()
            continue
    return env_history, False

PREFIXES = {
    'pick_and_place': 'put',
    'pick_clean_then_place': 'clean',
    'pick_heat_then_place': 'heat',
    'pick_cool_then_place': 'cool',
    'look_at_obj': 'examine',
    'pick_two_obj': 'puttwo'
}

def run_trial(
        trial_log_path: str,
        world_log_path: str,
        trial_idx: int,
        env_configs: List[Dict[str, Any]],
        use_memory: bool,
    ) -> List[Dict[str, Any]]:
    importlib.reload(alfworld)
    importlib.reload(alfworld.agents.environment)

    with open('base_config.yaml') as reader:
        config = yaml.safe_load(reader)
    split = "eval_out_of_distribution"
    env = get_environment(config["env"]["type"])(config, train_eval=split)
    env = env.init_env(batch_size=1)

    num_successes: int = 0
    num_additional_successes: int = 0
    num_envs: int = len(env_configs)

    for idx, env_config in enumerate(env_configs):
        print("You are using task: ",idx,"\n")
        ob, info = env.reset()
        ob = '\n'.join(ob[0].split('\n\n')[1:])
        name = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])
        print(f"using {name}")
        if env_config["is_success"]:
            num_successes += 1
            with open(world_log_path, 'a') as wf:
                wf.write(f'Environment #{idx} Trial #{trial_idx}: SUCCESS\n')
            with open(trial_log_path, 'a') as wf:
                wf.write(f'\n#####\n\nEnvironment #{idx}: Success\n\n#####\n')
            continue

        for i, (k, v) in enumerate(PREFIXES.items()):
            if name.startswith(k):
                prompt=f"""You are an agent operating in a text-based virtual environment to perform household-type tasks. You need to decide on the next action based on your task objectives and environmental feedback. You can perform two types of actions:
1.When you do not know the specific action to take next, think about your task objectives and environmental feedback to formulate a plan for the next step.
2.When you clearly know the next action to take, execute the action directly.
Below is an example of successful task completion by agents in the same virtual environment. You need study the example carefully.
This is the example.
{d[f'react_{v}_1']}
Note that only when the object is 100% identical to your target can you take it. For a closed receptacle, you need to open it firstly. Now, your task is as following.
{ob}"""
                final_env_history, is_success = alfworld_run(env, prompt,env_config["memory"] if use_memory else [], to_print=False, ob=ob)
                if is_success:
                    status_str: str = f'Environment #{idx} Trial #{trial_idx}: SUCCESS'
                    env_configs[idx]['is_success'] = True
                    num_successes += 1
                    num_additional_successes += 1
                else:
                    status_str: str = f'Environment #{idx} Trial #{trial_idx}: FAIL'
                with open(world_log_path, 'a') as f:
                    f.write(status_str + '\n')
                with open(trial_log_path, 'a') as wf:
                    wf.write(f'\n#####\n\nEnvironment #{idx}:\n{str(final_env_history)}\n\nSTATUS: {"OK" if is_success else "FAIL"}\n\n#####\n')
        time.sleep(3)
    env.close()
    log_str: str = f"""
-----
SUCCESS: {num_successes}
ADDITIONAL SUCCESS: {num_additional_successes}
FAIL: {num_envs - num_successes}
TOTAL: {num_envs}
ACCURACY: {round(num_successes / num_envs, 2)}
-----"""
    with open(trial_log_path, 'a') as wf:
        wf.write(log_str)
    with open(world_log_path, 'a') as wf:
        wf.write(log_str + '\n')

    return env_configs

