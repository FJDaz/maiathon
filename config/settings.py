#paramètres du modèle--
MODEL_ID = "Mistral-7B-SNB-fused"
MODEL_BASE_URL = "https://huggingface.co/mistralai"
MAX_TOKEN_HISTORY = 2048

# contraint Maïathon--
REGLES_DIALOGUE = {
    "Tutoie":True,
    "concit":True,
    "questionne_au_lieu_d_affirmer":True
 }