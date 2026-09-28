import re
def parse_answer(answer:str)->str:
    action=""
    for i, char in enumerate(answer):
        if char.isalpha():
            action=answer[i:]
            break
    pattern=["craft", "inventory", "get", "think"]
    if any(action.strip().startswith(p) for p in pattern):
        return action
    else:
        return "think: "+action

def get_info(text:str):
    lines = text.split('\n')[1:]
    lines=[s for s in lines if s != '']
    lines = '\n'.join(lines)
    commands,task=lines.split('Goal: ')
    target=task.replace("craft ","")
    target=target.replace(".","")
    info=[commands,target]
    return info

def parse_response(text:str):
    start1 = text.find('[')
    end1 = text.find(']', start1)
    result=text[start1 + 1:end1]
    return result

def command_decompose(text:str):
    start1 = text.find('[')
    end1 = text.find(']', start1)
    if start1 == -1 or end1 == -1:
        return None, None
    command = text[start1 + 1:end1]
    start2 = text.find('[', end1 + 1)
    end2 = text.find(']', start2)
    if start2 == -1 or end2 == -1:
        return None, None
    number_str = text[start2 + 1:end2]
    try:
        number = int(number_str)
    except ValueError:
        return None, None
    return command, number

def parse_craft(text:str):
    parts = text.split()
    count = int(parts[1])
    item_full = parts[2]
    if item_full.startswith("minecraft:"):
        item = item_full[len("minecraft:"):]
    else:
        item = item_full
    item=item.replace("_"," ")
    return (count,item)

def parse_obs(commands:str):
    lines = commands.split('\n')
    pattern = re.compile(r'(\d+) planks')
    pattern2=re.compile(r'(\d+) wool')
    modified_lines = []
    for line in lines:
        if 'using' in line:
            parts = line.split('using', 1)
            parts[1] = pattern.sub(r'\1 oak planks', parts[1])
            parts[1]=pattern2.sub(r'\1 white wool',parts[1])
            line = 'using'.join(parts)
        modified_lines.append(line)
    oak_planks_recipe = "craft 4 oak planks using 1 oak logs"
    recipe_exists = any(oak_planks_recipe in line for line in modified_lines)
    if not recipe_exists:
        for i, line in enumerate(modified_lines):
            if line.strip() == "Crafting commands:":
                modified_lines.insert(i+1, oak_planks_recipe)
                break
    modified_commands = '\n'.join(modified_lines)
    return modified_commands