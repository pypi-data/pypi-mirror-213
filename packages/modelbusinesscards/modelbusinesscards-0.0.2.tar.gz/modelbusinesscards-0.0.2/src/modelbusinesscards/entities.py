from typing import List


class ModelBusinessPromptDoc:
    """Represents a prompt variable in code"""
    def __init__(self, name: str, prompt: dict):
        self.name = name
        self.prompt = prompt

class ModelBusinessDoc:
    """Represents a function docstring and code"""
    def __init__(self, name: str, business_logic: str, models: List[str], tags: List[str], prompts: List[str]):
        self.name = name
        self.business_logic = business_logic
        self.models = models
        self.tags = tags
        self.prompts = prompts
