#!/bin/bash
# Activar entorno virtual
source .venv/bin/activate

# Rutas relativas
MODEL_DIR="./modelo_local/HF_original"
GGUF_OUT="./modelo_local/GGUF/modelo.gguf"
CONVERT_SCRIPT="./llama_cpp/convert_hf_to_gguf.py"

# Ejecutar conversión
python "$CONVERT_SCRIPT" "$MODEL_DIR" \
    --outfile "$GGUF_OUT"