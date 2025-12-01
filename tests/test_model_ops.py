# Fichier: tests/test_model_ops.py
import torch
import pytest
from unittest.mock import patch, MagicMock
from src.model_ops import fusionner_lora, quantifier_modele

# Les décorateurs @patch simulent le comportement des fonctions d'Hugging Face
@patch('src.model_ops.AutoModelForCausalLM')
@patch('src.model_ops.PeftModel')
@patch('src.model_ops.AutoTokenizer')
def test_fusion_lora_appels_hf_corrects(MockAutoTokenizer, MockPeftModel, MockAutoModel):
    """
    Simule la fusion LoRA pour s'assurer que la fonction appelle les bonnes méthodes
    d'Hugging Face (chargement, fusion, sauvegarde) avec les bons arguments.
    """
    # Arguments simulés
    MODELE_BASE = "Mistral-7B-base"
    ADAPTER_LORA = "mon_lora_spinoza"
    OUTPUT_PATH = "models/fused"

    # Exécution de la fonction
    fusionner_lora(MODELE_BASE, ADAPTER_LORA, OUTPUT_PATH, MODELE_BASE)

    # 1. Vérification du chargement du modèle de base
    MockAutoModel.from_pretrained.assert_called_with(
        MODELE_BASE,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    
    # 2. Vérification de l'appel à la méthode critique de fusion (merge_and_unload)
    # On récupère l'instance du modèle PeftModel
    modele_instance = MockPeftModel.from_pretrained.return_value
    modele_instance.merge_and_unload.assert_called_once()
    
    # 3. Vérification de l'appel à la sauvegarde au bon endroit
    # merge_and_unload() retourne un nouvel objet (le modèle fusionné)
    modele_fusionne = modele_instance.merge_and_unload.return_value
    modele_fusionne.save_pretrained.assert_called_with(OUTPUT_PATH)
    
    # 4. Vérification de la sauvegarde du tokenizer
    MockAutoTokenizer.from_pretrained.assert_called_with(MODELE_BASE)
    
    # On vérifie que la sauvegarde est bien appelée avec le chemin de sortie
    MockAutoTokenizer.from_pretrained.return_value.save_pretrained.assert_called_with(OUTPUT_PATH)



#--------------------------------------------------------------------------------------------------------------------------
#TEST DE LA QUANTIZATION DU MODELE FUSIONNE
#-------------------------------------------------------------------------------------------------------------------------- 
# Nous utilisons le même patching (simulation) pour les classes lourdes
@patch('src.model_ops.AutoModelForCausalLM')
@patch('src.model_ops.BitsAndBytesConfig') 
def test_quantifier_modele_appels_hf_corrects(MockBitsAndBytesConfig, MockAutoModel):
    """
    Simule la quantification INT4 pour s'assurer que le modèle est rechargé 
    avec la bonne configuration de quantification (BitsAndBytesConfig).
    """
    # Arguments simulés
    INPUT_PATH = "models/fused"
    OUTPUT_PATH = "models/quantized"
    
    # 1. Exécution de la fonction
    quantifier_modele(INPUT_PATH, OUTPUT_PATH, quantization_type="4bit")
    
    # 2. Vérification que la configuration BnB a été créée
    MockBitsAndBytesConfig.assert_called_with(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16 # Fait référence à l'import torch
    )
    
    # On récupère l'instance de la configuration BnB qui a été créée
    bnb_config_instance = MockBitsAndBytesConfig.return_value
    
    # 3. Vérification que le modèle a été chargé AVEC la configuration de quantification
    MockAutoModel.from_pretrained.assert_called_with(
        INPUT_PATH,
        quantization_config=bnb_config_instance,
        device_map="auto",
        trust_remote_code=True,
    )
    
    # 4. Vérification de la sauvegarde
    modele_instance = MockAutoModel.from_pretrained.return_value
    modele_instance.save_pretrained.assert_called_with(OUTPUT_PATH)