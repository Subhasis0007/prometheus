from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.memory = {}

    @abstractmethod
    def run(self, task: str):
        pass

    def log(self, message: str):
        print(f"[{self.name}] {message}")
