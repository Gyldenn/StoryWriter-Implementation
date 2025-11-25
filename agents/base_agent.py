from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Clase base que se encarga de almacenar el cliente LLM.
    Todos los agentes heredan de esta clase y usan self.llm.
    """

    def __init__(self, llm_client, name: str = "", prompt_template: str = ""):
        self.llm = llm_client
        self.name = name
        self.prompt_template = prompt_template

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def call_llm(self, prompt: str, **gen_kwargs):
        return self.llm.generate(prompt, **gen_kwargs)
