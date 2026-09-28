import os
import time
from typing import List
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ChatMessage
os.environ["DASHSCOPE_API_KEY"] = ""

class deepseek:
    def __init__(self, max_tokens=80, stop_newline=True):
        self.llm = ChatTongyi(
            model="deepseek-v3.2",
            max_tokens=max_tokens,
            temperature=0.0,
            top_p=1
        )
        self.stop = ["\n"] if stop_newline else None
        self.total_token=0
    def __call__(self, prompt:List[ChatMessage],replace_newline: bool = True) -> str:
        kwargs = {}
        if self.stop is not None:
            kwargs['stop'] = self.stop
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

react_llm=deepseek()
egp_llm=deepseek(max_tokens=500, stop_newline=False)
