SCHEMAS = {
    "put": [
        ["you have not found the target object", "you are not holding the target object", "go to an unchecked receptacle to search for the target object"],
        ["you find the target object in a receptacle", "you are not holding the target object and are not at that receptacle", "go to that receptacle"],
        ["you find the target object in a receptacle", "you are not holding the target object and are at that receptacle", "take the target object from that receptacle"],
        ["you are at the target receptacle", "you are holding the target object", "put the target object in/on the target receptacle"],
        ["you are not at the target receptacle", "you are holding the target object", "go to the target receptacle"],
    ],
    "clean": [
        ["you have not found the target object", "you are not holding the target object", "go to an unchecked receptacle to search for the target object"],
        ["you find the target object in a receptacle", "you are not holding the target object and are not at that receptacle", "go to that receptacle"],
        ["you find the target object in a receptacle", "you are not holding the target object and are at that receptacle", "take the target object from that receptacle"],
        ["you are at the sinkbasin", "you are holding the target object and it is not clean", "clean the target object with the sinkbasin"],
        ["you are not at the sinkbasin", "you are holding the target object and it is not clean", "go to the sinkbasin"],
        ["you are at the target receptacle", "you are holding the target object and it is clean", "put the target object in/on the target receptacle"],
        ["you are not at the target receptacle", "you are holding the target object and it is clean", "go to the target receptacle"],
    ],
    "heat": [
        ["you have not found the target object", "you are not holding the target object", "go to an unchecked receptacle to search for the target object"],
        ["you find the target object in a receptacle", "you are not holding the target object and are not at that receptacle", "go to that receptacle"],
        ["you find the target object in a receptacle", "you are not holding the target object and are at that receptacle", "take the target object from that receptacle"],
        ["you are at the microwave", "you are holding the target object and it is not hot", "heat the target object with the microwave"],
        ["you are not at the microwave", "you are holding the target object and it is not hot", "go to the microwave"],
        ["you are at the target receptacle", "you are holding the target object and it is hot", "put the target object in/on the target receptacle"],
        ["you are not at the target receptacle", "you are holding the target object and it is hot", "go to the target receptacle"],
    ],
    "cool": [
        ["you have not found the target object", "you are not holding the target object", "go to an unchecked receptacle to search for the target object"],
        ["you find the target object in a receptacle", "you are not holding the target object and are not at that receptacle", "go to that receptacle"],
        ["you find the target object in a receptacle", "you are not holding the target object and are at that receptacle", "take the target object from that receptacle"],
        ["you are at the fridge", "you are holding the target object and it is not cool", "cool the target object with the fridge"],
        ["you are not at the fridge", "you are holding the target object and it is not cool", "go to the fridge"],
        ["you are at the target receptacle", "you are holding the target object and it is cool", "put the target object in/on the target receptacle"],
        ["you are not at the target receptacle", "you are holding the target object and it is cool", "go to the target receptacle"],
    ],
    "examine": [
        ["you have not found the target object", "you are not holding the target object", "go to an unchecked receptacle to search for the target object"],
        ["you find the target object in a receptacle", "you are not holding the target object and are not at that receptacle", "go to that receptacle"],
        ["you find the target object in a receptacle", "you are not holding the target object and are at that receptacle", "take the target object from that receptacle"],
        ["you are at the desk", "you are holding the target object", "use the desklamp to examine the target object"],
        ["you are not at the desk", "you are holding the target object", "go to the desk"],
    ],
    "puttwo": [
        ["you have not found the first target object", "you are not holding it", "go to an unchecked receptacle to search for the first target object"],
        ["you find the first target object in a receptacle", "you are not holding it and are not at that receptacle", "go to that receptacle"],
        ["you find the first target object in a receptacle", "you are not holding it and are at that receptacle", "take the first target object from that receptacle"],
        ["you are at the target receptacle", "you are holding the first target object", "put the first target object in/on the target receptacle"],
        ["you are not at the target receptacle", "you are holding the first target object", "go to the target receptacle"],
        ["you have not found the second target object", "you are not holding it", "go to an unchecked receptacle to search for the second target object"],
        ["you find the second target object in a receptacle", "you are not holding it and are not at that receptacle", "go to that receptacle"],
        ["you find the second target object in a receptacle", "you are not holding it and are at that receptacle", "take the second target object from that receptacle"],
        ["you are at the target receptacle", "you are holding the second target object", "put the second target object in/on the target receptacle"],
        ["you are not at the target receptacle", "you are holding the second target object", "go to the target receptacle"],
    ],
}

def render_schema(task_type):
    entries = SCHEMAS.get(task_type, [])
    lines = []
    for i, entry in enumerate(entries):
        lines.append(f"{i + 1}. When [{entry[0]}] and [{entry[1]}], the action \"{entry[2]}\" is applicable.")
    return "\n".join(lines)