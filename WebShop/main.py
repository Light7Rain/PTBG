import os
import json
from webshop_trial import run_trial
from llm import*
from typing import Any, List, Dict

def main() -> None:
    num_trials=1
    num_envs=100
    use_memory=False
    run_name="webshop_run_logs"
    if not os.path.exists(run_name):
        os.makedirs(run_name)
    logging_dir = run_name
    world_log_path: str = os.path.join(logging_dir, 'world.log')

    env_configs: List[Dict[str, Any]] = []
    for i in range(num_envs):
        env_configs += [{
            'name': f'env_{i}',
            'memory': [],
            'is_success': False,
            'reward':0,
            'skip': False
        }]

    print(f"""
    -----
    Starting run with the following parameters:
    Run name: {logging_dir}
    Number of trials: {num_trials}
    Number of environments: {num_envs}
    Use memory: {use_memory}

    Sending all logs to 'webshop_run_logs'
    -----
    """)
    trial_idx = 0
    while trial_idx < num_trials:
        with open(world_log_path, 'a') as wf:
            wf.write(f'\n\n***** Start Trial #{trial_idx} *****\n\n')
        trial_log_path: str = os.path.join(run_name, f'trial_{trial_idx}.log')
        trial_env_configs_log_path: str = os.path.join(run_name, f'env_results_trial_{trial_idx}.json')
        if os.path.exists(trial_log_path):
            open(trial_log_path, 'w').close()
        if os.path.exists(trial_env_configs_log_path):
            open(trial_env_configs_log_path, 'w').close()
        run_trial(trial_log_path, world_log_path, trial_idx, env_configs, use_memory)
        react_llm.store_token()
        think_llm.store_token()
        egp_llm.store_token()
        with open(trial_env_configs_log_path, 'w') as wf:
            json.dump(env_configs, wf, indent=4)
        with open(world_log_path, 'a') as wf:
            wf.write(f'\n\n***** End Trial #{trial_idx} *****\n\n')

        trial_idx += 1

if __name__ == '__main__':
    main()
