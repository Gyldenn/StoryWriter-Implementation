# llm.py
from llama_cpp import Llama
from typing import Dict, Any

class LLMClient:
    def __init__(self, model_path: str, **kwargs):
        # kwargs pueden incluir n_ctx, n_threads, etc.
        self.model = Llama(model_path=model_path, **kwargs)

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7, stop: list = None) -> str:
        out = self.model(prompt, max_tokens=max_tokens, temperature=temperature)
        text = out['choices'][0].get('text', '')
        return text.strip()

# Ejemplo de uso:
# client = LLMClient(model_path="./modelo_local/GGUF/modelo.gguf", n_ctx=512)
# respuesta = client.generate("Escribe un evento principal: ...")