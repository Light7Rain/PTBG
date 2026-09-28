import os
import time
from typing import List
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ChatMessage
os.environ["DASHSCOPE_API_KEY"] = ""
class deepseek_action:
    def __init__(self):
        self.llm = ChatTongyi(
            model="deepseek-v3",
            max_tokens=40,
            temperature=0.0,
            top_p=1
        )
        self.total_token=0
    def __call__(self, prompt:List[ChatMessage],replace_newline: bool = True) -> str:
        kwargs = {}
        kwargs['stop'] = ["\n"]
        for i in range(5):
            try:
                result=self.llm.invoke(prompt, **kwargs)
                output = result.content.strip('\n').strip()
                token=result.response_metadata.get('token_usage').get('total_tokens')
                self.total_token+=token
                break
            except:
                print(f'\nRetrying {i}...')
                time.sleep(1)
        else:
            raise RuntimeError('Failed to generate response')
        if replace_newline:
            output = output.replace('\n', '')
        return output
    
    def store_token(self):
        path="token.txt"
        print(self.total_token)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"Here is the total token used in ReAct and Refelxion"+'\n'+str(self.total_token)+'\n')


class deepseek_think:
    def __init__(self):
        self.llm = ChatTongyi(
            model="deepseek-v3",
            max_tokens=120,
            temperature=0.0,
            top_p=1
        )
        self.total_token=0
    def __call__(self, prompt:List[ChatMessage],replace_newline: bool = True) -> str:
        kwargs = {}
        kwargs['stop'] = ["\n"]
        for i in range(5):
            try:
                result=self.llm.invoke(prompt, **kwargs)
                output = result.content.strip('\n').strip()
                token=result.response_metadata.get('token_usage').get('total_tokens')
                self.total_token+=token
                break
            except:
                print(f'\nRetrying {i}...')
                time.sleep(1)
        else:
            raise RuntimeError('Failed to generate response')
        if replace_newline:
            output = output.replace('\n', '')
        return output
    
    def store_token(self):
        path="token.txt"
        print(self.total_token)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"Here is the total token used in ReAct and Refelxion"+'\n'+str(self.total_token)+'\n')

act_llm=deepseek_action()
react_llm=deepseek_think()