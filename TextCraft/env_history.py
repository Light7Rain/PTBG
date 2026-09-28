from typing import List, Dict
from langchain_core.messages import ChatMessage,SystemMessage,HumanMessage

class EnvironmentHistory:
    def __init__(self, base_query: str, obs, memory: List[str], history: List[Dict[str, str]] = []) -> None:
        self.mem=memory
        self.start_obs=obs
        self.commands=""
        self.task=""
        self._history: List[Dict[str, str]] = history # record current task history
        self._last_action: str = ''
        self._is_exhausted: bool = False
        self.human_message=base_query+'\n'+obs+'\n'
        self.history_message:str=''
        self.reflections=''

    def initiallze_info(self) -> None:
        commands,task=self.start_obs.split('Goal: ')
        self.commands=commands
        self.task=task
        self.task=self.task.replace(".","")

    def add(self, label: str, value: str) -> None:
        assert label in ['action', 'observation']
        self._history += [{
            'label': label,
            'value': value,
        }]

    def add_message(self, value:str)->str:
        self.human_message+=f"{value}\n"
        self.history_message+=f"{value}\n"
    
    def create_message(self)->List[ChatMessage]:
        return [
            SystemMessage(content="Follow the syntax of the examples closely when taking actions."),
            HumanMessage(content=self.human_message)
        ]

    def check_is_exhausted(self) -> bool:
        return self._is_exhausted

    def reset(self) -> None:
        self._history = []

    def __str__(self) -> str:
        s: str = self.start_obs+'\n'
        for i, item in enumerate(self._history):
            if item['label'] == 'action':
                s += f'> {item["value"]}'
            elif item['label'] == 'observation':
                s += item['value']
            if i != len(self._history) - 1:
                s += '\n'
        return s