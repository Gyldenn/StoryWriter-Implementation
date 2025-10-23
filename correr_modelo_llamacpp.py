from llama_cpp import Llama

llm = Llama(model_path="./modelo_local/GGUF/modelo.gguf")


output = llm("which is the capital of France? answer in a few words")

print(output['choices'][0]['text'])