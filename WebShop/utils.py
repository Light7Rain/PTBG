def parse_answer(text:str):
    text=text.strip()
    keywords = ["think", "search", "click"]
    min_index = len(text)
    for keyword in keywords:
        index = text.find(keyword)
        if index != -1 and index < min_index:
            min_index = index
    if min_index < len(text):
        text=text[min_index:]
    text=text.strip()
    if text.startswith("search") or text.startswith("click"):
        action = "search" if text.startswith("search") else "click"
        remaining_text = text[len(action):].strip()
        if not remaining_text:
            return action
        if remaining_text.startswith("[") and remaining_text.endswith("]"):
            return f"{action}{remaining_text}"
        return f"{action}[{remaining_text}]"
    if text=="< Prev":
        text="click[< Prev]"
    elif text=="> Next":
        text="click[> Next]"
    return text

def parse_observation(text:str):
    start1=text.find("You have clicked")
    if start1!=-1:
        return text[start1:]
    else:
        start=text.find("[button]")
        if start!=-1:
            return text[start:]
        else:
            return text

def parse_product(text:str):
    return text[-11:-1]

def parse_traj(text:str):
    lines=text.split("\n")
    info=[]
    for line in reversed(lines):
        info.append(line)
        if "click[Description]" in line:
            break
    num=0
    num1=0
    info=list(reversed(info))
    flag=False

    for i in range(len(info)):
        if "< Prev" in info[i]:
            current=info[i+1]
            if current=="" or "click[< Prev]" in current:
                flag=True
            else:
                num=i+1
                break
    product=[]
    if flag:
        for i in range(0,len(info)):
            if "click[< Prev]" in info[i]:
                num2=i
        num2+=2
        for i in range(num2,len(info)):
            if not "Action" in info[i]:
                product.append(info[i])
            else:
                break
        p=["Description:None"]
        product[-5:-5] = p
        product_all="\n".join(product).strip()
        return product_all
    description=[]
    for i in range(num,len(info)):
        if not "click[< Prev]" in info[i]:
            description.append(info[i])
        else:
            num1=i
            break
    if description[0]=="":
        description.pop(0)
    if description[-1]=="":
        description.pop()
    description[0]="Description:"+description[0]
    num1+=2
    
    for i in range(num1,len(info)):
        if not "Action" in info[i]:
            product.append(info[i])
        else:
            break
    if product[0]=="":
        product.pop(0)
    if product[-1]=="":
        product.pop()

    product[-5:-5] = description
    product_all="\n".join(product).strip()
    return product_all