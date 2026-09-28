import re
from collections import defaultdict
def parse_thought(thought:str):
    for i, char in enumerate(thought):
        if char.isalpha():
            thought=thought[i:]
            break
    if not thought.startswith("think:"):
        thought="think: "+thought
    thought=thought.replace(">","")
    return thought

def parse_action(action:str)->str:
    for i, char in enumerate(action):
        if char.isalpha():
            action=action[i:]
            break
    if 'put' in action and 'in/on' in action:
        return action

    has_put = 'put' in action
    has_in = 'in' in action.split()
    has_on = 'on' in action.split()

    if not has_put or (not has_in and not has_on):
        return action

    pattern_in = r'\bin\b'
    pattern_on = r'\bon\b'
    
    result=''

    if has_in:
        result = re.sub(pattern_in, 'in/on', action)
        result=result.replace("the ","")
        return result
    elif has_on:
        result = re.sub(pattern_on, 'in/on', action)
        result=result.replace("the ","")
        return result
def sort_by_prefix_and_number(text):
    prefix_groups = defaultdict(list)
    for item in text:
        parts = item.split()
        if len(parts) == 2 and parts[1].isdigit():
            prefix, number = parts[0], int(parts[1])
        else:
            prefix, number = item, 0
        prefix_groups[prefix].append((number, item))
    sorted_result = []
    for prefix in prefix_groups:
        sorted_group = sorted(prefix_groups[prefix], key=lambda x: x[0])
        sorted_result.extend([item for _, item in sorted_group])
    return sorted_result
def get_information(text:str):
    split_texts = text.split('\n')
    available_receptacles = split_texts[0]
    task = (split_texts[1])[17:]
    task=task.replace(".", "")
    target_obj=''
    target_receptacle=''
    parts = task.split()
    if task.startswith("put"):
        target_receptacle=parts[-1]
        target_obj=parts[-3]
    elif task.startswith("examine") or task.startswith("look"):
        target_receptacle=parts[-1]
        target_obj=parts[-4]
    else:
        target_receptacle=parts[-1]
        target_obj=parts[-6]

    target_receptacle+=" 1"
    available_receptacles=available_receptacles[69:]
    available_receptacles= available_receptacles.replace("and ", "")
    available_receptacles = available_receptacles.replace(".", "")
    result=[item.strip() for item in available_receptacles.split(",")]
    result=[item[2:] for item in result]
    result=sort_by_prefix_and_number(result)
    task=task.strip()
    result.append(task)
    target_obj=target_obj.strip()
    result.append(target_obj)
    result.append(target_receptacle)
    return result

def get_target_receptacles(keyword:str,receptacles:list):
    result=[item for item in receptacles if item.startswith(keyword)]
    return result

def parse_objects(value:str):
    flag1 = re.search(r'\[(.*?)\]', value)
    objects=[]
    if not flag1:
        objects.append("nothing")
        return "nothing"
    first_content = flag1.group(1)
    flag2 = re.findall(r'\[(.*?)\]', value)
    if len(flag2) > 1:
        second_content = flag2[1]
        items = [item.strip() for item in second_content.split(',')]
        if items:
            for i in range(len(items)):
                objects.append(items[i])
        else:
            objects.append("nothing")
        return first_content, objects
    else:
        objects.append("nothing")
        return first_content, objects