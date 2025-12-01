import pytest
from config.settings import REGLES_DIALOGUE, MAX_TOKEN_HISTORY

def test_longueur_context_est_optimale():
    """vérifie si le context maximal est bien celui defini pour l'optimisations """
    assert MAX_TOKEN_HISTORY == 2048, "La longueur du context maximal n'est pas optimale"

def test_regles_dialogue_sont_valides():
    """vérifie si la régle 'questionne au lieu d'affirmer' est bien enclenchée"""
    assert REGLES_DIALOGUE["questionne_au_lieu_d_affirmer"] is True 

def test_regles_dialogue_contient_tutoie():
    """vérifie si la régle 'Tutoie' est présente"""
    assert"Tutoie" in REGLES_DIALOGUE, "La régle 'tutoie' n'est pas présente"