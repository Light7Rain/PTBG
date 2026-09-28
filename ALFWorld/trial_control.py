from utils import get_information

class TrialControl:
    def __init__(self,start_ob):
        self.all_information=get_information(start_ob)
        self.task_receptacle=self.all_information[-1]
        self.task_object=self.all_information[-2]
        self.task=self.all_information[-3]
        self.all_receptacles=self.all_information[0:-3]

    def get_task_type(self):
        t=self.task
        if t.startswith("find two") or t.startswith("put two"):
            return "puttwo"
        if t.startswith("put a cool") or t.startswith("cool"):
            return "cool"
        if t.startswith("put a hot") or t.startswith("heat"):
            return "heat"
        if t.startswith("put a clean") or t.startswith("clean"):
            return "clean"
        if t.startswith("examine") or t.startswith("look at"):
            return "examine"
        return "put"
