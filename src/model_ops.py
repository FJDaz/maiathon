# Fichier: src/model_ops.py
# Ce script doit être exécuté dans un environnement avec un GPU (Colab ou Vast.ai)

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

def fusionner_lora(
    modele_base_id: str,
    lora_adapter_id: str,
    output_dir: str,
    tokenizer_id: str
) -> str:
    """
    Phase 1.2 : Charge le modèle de base et l'adapter LoRA, puis effectue la fusion
    et sauvegarde le modèle fusionné complet (Full-Fidelity).
    
    Args:
        modele_base_id (str): ID du modèle de base (ex: 'mistralai/Mistral-7B-v0.2').
        lora_adapter_id (str): ID ou chemin local de l'adapter PEFT/LoRA (ex: 'francois-d/spinoza_lora_v1').
        output_dir (str): Chemin local pour sauvegarder le modèle fusionné.
        tokenizer_id (str): ID du tokenizer.

    Returns:
        str: Le chemin vers le modèle fusionné.
    """
    print(f"Chargement du modèle de base : {modele_base_id}")
    
    # 1. Charger le modèle de base (doit être en 4bit/8bit ou sur GPU, d'où device_map="auto")
    modele_base = AutoModelForCausalLM.from_pretrained(
        modele_base_id,
        device_map="auto",
        torch_dtype=torch.float16,  # Utilisation du FP16 pour économiser la VRAM lors de la fusion
        trust_remote_code=True,
    )
    
    # 2. Charger l'adapter LoRA
    print(f"Chargement de l'adapter LoRA : {lora_adapter_id}")
    modele_fusion = PeftModel.from_pretrained(
        model=modele_base, 
        model_id=lora_adapter_id
    )
    
    # 3. Fusion (Merge) et Nettoyage (Unload)
    # C'est l'opération critique qui incorpore les poids LoRA dans le modèle de base.
    print("Début de la fusion LoRA (merge_and_unload)...")
    modele_fusion = modele_fusion.merge_and_unload()
    
    # 4. Sauvegarde
    print(f"Sauvegarde du modèle fusionné complet dans : {output_dir}")
    modele_fusion.save_pretrained(output_dir)
    
    # Sauvegarde du tokenizer (critique pour l'inférence)
    AutoTokenizer.from_pretrained(tokenizer_id).save_pretrained(output_dir)
    
    print("Fusion et sauvegarde terminées.")
    return output_dir


if __name__ == '__main__':
    # Exemple d'exécution (à lancer sur Colab/GPU)
    from config.settings import MODEL_ID 
    
    # Remplacez ceci par les IDs réels de votre projet
    MODELE_BASE_ID = "mistralai/Mistral-7B-Instruct-v0.2"
    LORA_ADAPTER_ID = "FJDaz/mistral-7b-philosophes-lora" # <--- À mettre à jour
    OUTPUT_DIR = "./models/mistral_spinoza_fused"
    
    # On utilise l'ID du modèle de base pour le tokenizer
    fusionner_lora(
        modele_base_id=MODELE_BASE_ID,
        lora_adapter_id=LORA_ADAPTER_ID,
        output_dir=OUTPUT_DIR,
        tokenizer_id=MODELE_BASE_ID 
    )


#--------------------------------------------------------------------------------------------------------------------------
#QUANTIZATION DU MODELE FUSIONNE
#--------------------------------------------------------------------------------------------------------------------------


# Importation spécifique pour la quantification (déjà installé)
from transformers import BitsAndBytesConfig 
import os # Pour les opérations de fichier

def quantifier_modele(
    input_dir: str, 
    output_dir: str, 
    quantization_type: str = "4bit"
) -> str:
    """
    Phase 1.3 : Quantifie le modèle fusionné vers un format à faible précision (INT4).
    
    Args:
        input_dir (str): Chemin local vers le modèle FUSIONNÉ complet.
        output_dir (str): Chemin local pour sauvegarder le modèle quantifié.
        quantization_type (str): Type de quantification ('4bit' ou autre si supporté).

    Returns:
        str: Le chemin vers le modèle quantifié.
    """
    if quantization_type != "4bit":
        print(f"La quantification {quantization_type} n'est pas supportée dans ce script.")
        return input_dir

    # 1. Définition de la configuration de quantification 4 bits
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4", # Type de quantification (NF4)
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16 # dtype pour le calcul interne
    )

    print(f"Chargement du modèle depuis {input_dir} pour quantification 4 bits...")

    # 2. Rechargement du modèle avec la configuration de quantification
    # Note: Ceci est une simulation de chargement, l'opération réelle prend VRAM.
    modele_quantifie = AutoModelForCausalLM.from_pretrained(
        input_dir,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    
    # 3. Sauvegarde du modèle quantifié
    print(f"Sauvegarde du modèle quantifié dans : {output_dir}")
    modele_quantifie.save_pretrained(output_dir)
    
    # Le tokenizer est déjà sauvegardé à l'étape de fusion, pas besoin de le refaire.
    
    print("Quantification et sauvegarde terminées.")
    return output_dir
    

if __name__ == '__main__':
    # ... (le code d'exemple pour fusionner_lora reste ici)
    
    # Nouvelle étape d'exemple (à lancer sur Colab/GPU après la fusion)
    # Assurez-vous que les chemins correspondent à ceux du fichier settings.py
    quantifier_modele(
        input_dir="./models/mistral_spinoza_fused",
        output_dir="./models/mistral_spinoza_quantized"
    )