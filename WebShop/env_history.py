from typing import List, Dict
from langchain_core.messages import ChatMessage,SystemMessage,HumanMessage

class EnvironmentHistory:
    def __init__(self, base_prompt: str,instruction:str,memory: List[str], history: List[Dict[str, str]] = []) -> None:
        self._history: List[Dict[str, str]] = history
        self.base_prompt=base_prompt
        self.human_message=""
        self.current_state:str=''
        self.instruction=instruction
        self.last_action=""

    def set_base_prompt(self,prompt:str):
        self.base_prompt+=f"""\n\nAction: {prompt}"""

    def reset_basic(self):
        pass

    def reset_message(self,products:str):
        self.human_message=f"""{self.base_prompt}\n
Observation:
{products}"""

    def add(self, label: str, value: str) -> None:
        assert label in ['action', 'observation']
        self._history += [{
            'label': label,
            'value': value,
        }]

    def check_repeated(self,action:str):
        if action==self.last_action:
            return True
        else:
            self.last_action=action
            return False

    def update_state(self, obs:str,acts_list:str):
        current_information=f"""Observation: \n{obs}\nAvailable actions:{acts_list}\n"""
        self.current_state=current_information
    
    def add_message(self,act:str,obs:str):
        self.human_message+=f"\nAction:{act}\n"
        self.human_message+=f"Observation:{obs}\n"

    def create_message(self)->List[ChatMessage]:
        return [
            SystemMessage(content="Follow the syntax of the example closely while taking actions."),
            HumanMessage(content=self.human_message)
        ]

    def __str__(self) -> str:
        s: str = self.instruction + '\n'
        for i, item in enumerate(self._history):
            if item['label'] == 'action':
                s += f'Action: {item["value"]}'
            elif item['label'] == 'observation':
                s += f'Observation: {item["value"]}'
            if i != len(self._history) - 1:
                s += '\n'
        return s