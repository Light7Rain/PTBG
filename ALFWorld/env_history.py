from typing import List, Dict
from langchain_core.messages import ChatMessage,SystemMessage,HumanMessage,AIMessage

class EnvironmentHistory:
    def __init__(self, prompt: str, start_info, memory: List[str], history: List[Dict[str, str]] = []) -> None:
        '''
        base_query contains base prompt and few-shots
        start_info describes initial environment
        '''
        self._cur_query: str = f'{_get_base_query(start_info)}'
        self._history: List[Dict[str, str]] = history
        self._last_action: str = ''
        self._is_exhausted: bool = False
        self.human_message=prompt
        self.trajectory:str=start_info+"\n"
        self.reflections=''

    def add(self, label: str, value: str) -> None:
        assert label in ['action', 'observation']
        self._history += [{
            'label': label,
            'value': value,
        }]
        if label == 'action':
            if value == self._last_action:
                self._is_exhausted = True
            else:
                self._is_exhausted = False
                self._last_action = value
    def add_message(self, label:str, value:str)->str:
        self.human_message+=f"{value}\n"
        self.trajectory+=f"{value}\n"
    
    def create_message(self)->List[ChatMessage]:
        return [
            SystemMessage(content="Follow the syntax of the examples closely when taking actions"),
            HumanMessage(content=self.human_message)
        ]

    def check_is_exhausted(self) -> bool:
        return self._is_exhausted

    def reset(self) -> None:
        self._history = []

    def __str__(self) -> str:
        s: str = self._cur_query + '\n'
        for i, item in enumerate(self._history):
            if item['label'] == 'action':
                s += f'> {item["value"]}'
            elif item['label'] == 'observation':
                s += item['value']
            if i != len(self._history) - 1:
                s += '\n'
        return s

def _get_base_query(start_info: str) -> str:
    query=''
    query += f"\nHere is the task:\n{start_info}"
    return query
