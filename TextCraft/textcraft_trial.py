import sys
import time
from textcraft.env import TextCraft
from env_history import EnvironmentHistory
from typing import List, Dict, Any, Tuple
from llm import act_llm
from utils import *
from ptbg import deliberate_think

with open("./prompts.txt", 'r') as f:
    BASE_PROMPTS = f.read()
def textcraft_run(env, base_prompt, memory, to_print=False, obs='') -> Tuple[EnvironmentHistory, bool]:
    env_history = EnvironmentHistory(base_prompt, obs, memory, [])
    env_history.reset()
    if to_print:
        print(obs)
        sys.stdout.flush()
    cur_step = 0
    message=env_history.create_message()
    drop=0
    last_invalid=False

    while cur_step < 39:
        if drop>0:
            break
        if cur_step%2==0:
            time.sleep(1)
        if last_invalid:
            action="think"
            last_invalid=False
        else:
            action=act_llm(message).strip()
            action=parse_answer(action)
        if action.startswith('think'):
            rationale="think: "+deliberate_think(env_history,env)
            env_history.add("action", rationale)
            env_history.add("observation", "OK.")
            env_history.add_message(f"> {rationale}")
            env_history.add_message("OK.")
            cur_step+=1
            message=env_history.create_message()
            continue
        observation, reward, done,_, info = env.step(action)
        if "Could not find" in observation:
            drop=1
        if observation.strip() == "" or observation.startswith("Could not"):
            last_invalid = True
        env_history.add("action", action)
        env_history.add("observation", observation)
        env_history.add_message(f"> {action}")
        env_history.add_message(f"{observation}")
        if to_print:
            print(f'{action}\n{observation}\n')
            sys.stdout.flush()
        message=env_history.create_message()
        if done:
            cur_step+=1
            return env_history, True, cur_step
        cur_step += 1
    return env_history, False, cur_step

def run_trial(
        trial_log_path: str,
        world_log_path: str,
        trial_idx: int,
        env_configs: List[Dict[str, Any]],
        use_memory: bool,
    ) -> List[Dict[str, Any]]:

    env = TextCraft(minecraft_dir="")
    num_successes: int = 0
    num_envs: int = len(env_configs)

    for idx, env_config in enumerate(env_configs):
        print("You are using task: ",idx,"\n")
        obs, info = env.reset(seed=idx)
        obs=parse_obs(obs)
        if env_config["is_success"]:
            num_successes += 1
            with open(world_log_path, 'a') as wf:
                wf.write(f'Environment #{idx} Trial #{trial_idx}: SUCCESS\n')
            with open(trial_log_path, 'a') as wf:
                wf.write(f'\n#####\n\nEnvironment #{idx}: Success\n\n#####\n')
            continue
        prompt=prompt=f"""{BASE_PROMPTS}"""
        final_env_history, is_success,steps=textcraft_run(env,prompt,env_config["memory"] if use_memory else [],to_print=False,obs=obs)
        env_configs[idx]['steps'] = steps
        if is_success:
            status_str: str = f'Environment #{idx} Trial #{trial_idx}: SUCCESS'
            env_configs[idx]['is_success'] = True
            num_successes += 1
        else:
            status_str: str = f'Environment #{idx} Trial #{trial_idx}: FAIL'
        with open(world_log_path, 'a') as f:
            f.write(status_str + '\n')
        with open(trial_log_path, 'a') as wf:
            wf.write(f'\n#####\n\nEnvironment #{idx}:\n{str(final_env_history)}\n\nSTATUS: {"OK" if is_success else "FAIL"}\n\n#####\n')
        time.sleep(2)
    log_str: str = f"""
-----
SUCCESS: {num_successes}
FAIL: {num_envs - num_successes}
TOTAL: {num_envs}
ACCURACY: {round(num_successes / num_envs, 2)}
-----"""
    with open(trial_log_path, 'a') as wf:
        wf.write(log_str)
    with open(world_log_path, 'a') as wf:
        wf.write(log_str + '\n')

    return env_configs
