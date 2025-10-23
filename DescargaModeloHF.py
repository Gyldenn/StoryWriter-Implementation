from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "ibm-granite/granite-3.0-1b-a400m-base"
local_path = "./modelo_local"


device = "cuda" if torch.cuda.is_available() else "cpu"

# Descargar el modelo y tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, device_map=device, legacy=False)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map=device,
    torch_dtype=torch.float16  # ayuda a usar menos memoria
)

# Guardar localmente
tokenizer.save_pretrained(local_path)
model.save_pretrained(local_path)
print(f"Modelo y tokenizer guardados en {local_path}")