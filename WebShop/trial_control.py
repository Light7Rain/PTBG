from langchain_core.messages import ChatMessage,SystemMessage,HumanMessage
import re

class TrialControl:
    def __init__(self,start_ob):
        self.current_context=""
        self.trajectory=""
        self.state=0
        self.keywords=""
        self.product_all=""
        self.ins=start_ob
        self.price_upper=self.get_price_upper()
        self.items=[]
        self.goal_item=""
        self.current_item=""
        self.checked=0

    def generate_keywords_message(self,ins):
        human_message=f"""You are an online shopping assistant. I will provide you with a shopping instruction, and you need to extract keywords from the instruction for searching. Each keyword should be separated by a space. The keywords should not contain the price information.

Below is an example.
My shopping instruction is: i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin
Your response should be: 3 ounce bright citrus deodorant sensitive skin

Here is another example.
My shopping instruction is: i'm looking for a space-saving ottoman bench to match my blue living room. pick that one that's 100x45x45cm
Your response should be: space-saving blue ottoman bench 100x45x45cm

Now, my shopping instruction is: {ins}
Your response should be: """
        return [
            SystemMessage(content="Follow the syntax of the example closely while taking actions."),
            HumanMessage(content=human_message)
        ]
    
    def get_price_upper(self):
        start_phrase = ", and price lower than "
        start_index = self.ins.find(start_phrase)
        if start_index != -1:
            result = self.ins[start_index + len(start_phrase):]
        else:
            return 1000000
        parts=result.split(" ")
        return parts[0]

    def get_product_all(self,obs:str,item:str):
        first_product_start = obs.find("[button] B0")
        if first_product_start != -1:
            obs = obs[first_product_start:]
        items=[]
        i=0
        parts=obs.split("\n")
        for i in range(len(parts)):
            part = parts[i].strip()
            if part.startswith("[button] B0"):
                product_id = part.split()[1]
                j=i+2
                if parts[j].startswith("$"):
                    price_str = parts[j].split(" ")
                    price_str=price_str[0][1:]
                    price = float(price_str)
                    if True:
                        items.append(product_id)
            else:
                continue
        if item in items:
            items.remove(item)
        lines = obs.split("\n")
        product_lines = []
        current_product = []
        for line in lines:
            if line.strip().startswith("[button] B0"):
                if current_product and any(current_product[0].split()[1] in r for r in items):
                    product_lines.extend(current_product+[""])
                current_product = [line]
            else:
                current_product.append(line)
        if current_product and any(current_product[0].split()[1] in r for r in items):
            product_lines.extend(current_product+[""])
        self.product_all = "\n".join(product_lines).strip()
        self.product_all=self.product_all.strip()
        return self.product_all

    def set_goal_item(self,text:str):
        self.goal_item=text[-6:-2]

    def set_keywords(self,text:str):
        self.keywords=text

    def update_obs(self,obs:str):
        self.trajectory+=f"""{obs}\n\n"""
        invalid_obs=["Invalid action!","OK.",""]
        if not obs in invalid_obs:
            self.current_context=obs

    def process(self,state:int):
        pass

    def filter_products_all(self,obs:str):
        first_product_start = obs.find("[button] B0")
        if first_product_start != -1:
            result = obs[first_product_start:]
        else:
            result = "NULL"
        items=[]
        i=0
        parts=result.split("\n")
        for i in range(len(parts)):
            part = parts[i].strip()
            if part.startswith("[button] B0"):
                product_id = part.split()[1]
                j=i+2
                if parts[j].startswith("$"):
                    price_str = parts[j][1:]
                    price = float(price_str)
                    if price < self.price_upper:
                        items.append(product_id)
            else:
                continue

    def check_stage(self):
        obs=self.current_context.strip()
        pattern = r'\[button\] B0[A-Z0-9]{8} \[button_\]'
        matches = re.findall(pattern, obs)
        if len(matches)>=3:
            return 0
        if "[button] Buy Now [button_]" in obs:
            if "You have clicked" in obs or "[clicked button]" in obs:
                return 2
            elif not "You have clicked" in obs and not "[clicked button]" in obs:
                return 1
            else:
                return 3
        else:
            return 3