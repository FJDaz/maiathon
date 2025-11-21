---
title: Spinoza Secours
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Spinoza Secours - Mistral 7B + LoRA

Backup léger de Bergson & Friends pour CPU/GPU.

## Modèle
- **Base**: Mistral 7B Instruct v0.2
- **LoRA**: Fine-tuné sur schèmes logiques spinozistes (900 exemples)
- **Quantization**: 4-bit (GPU) ou FP32 (CPU)

## API REST
- `GET /health` - Status
- `POST /chat` - Chat avec Spinoza
- `GET /init` - Question d'amorce

## Usage
```python
import requests

# Init
resp = requests.get("https://your-space.hf.space/init")
print(resp.json()["greeting"])

# Chat
resp = requests.post("https://your-space.hf.space/chat", json={
    "message": "La liberté c'est faire ce qu'on veut ?"
})
print(resp.json()["reply"])
```
