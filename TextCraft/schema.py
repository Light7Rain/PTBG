CRAFT_SCHEMA = [
    ["a recipe for the target item is found and a required material is missing and has no crafting recipe", "the agent has not obtained the missing material and cannot craft it", "get the missing raw material"],
    ["a recipe for the target item is found and a required material is missing and has a crafting recipe", "the agent has not obtained the missing material and can craft it", "craft the missing intermediate material using its recipe"],
    ["a recipe for the target item is found and all required materials are obtained", "the agent holds enough materials", "craft the target item"],
]
