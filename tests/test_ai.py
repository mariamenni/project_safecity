import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic_ai import get_ai_analysis

# On "Mock" (simule) Groq et Streamlit pour ne pas avoir d'erreurs réelles
@patch("logic_ai.Groq")
@patch("logic_ai.st.secrets")
def test_get_ai_analysis_success(mock_secrets, mock_groq):
    
    # 1. Simuler la clé API
    mock_secrets.__getitem__.return_value = "fake_key"
    
    # 2. Simuler la réponse de l'IA (On triche, on force la réponse)
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Ceci est une réponse simulée."
    mock_client.chat.completions.create.return_value = mock_response
    mock_groq.return_value = mock_client
    
    # 3. Lancer la fonction
    resultat = get_ai_analysis("Contexte test", mode="rapport")
    
    # 4. Vérifier
    assert resultat == "Ceci est une réponse simulée."
    # Vérifie qu'on a bien appelé le modèle Llama 3
    call_args = mock_client.chat.completions.create.call_args
    assert "llama-3.3-70b-versatile" in call_args[1]['model']

@patch("logic_ai.st.secrets")
def test_missing_api_key(mock_secrets):
    # Simuler une erreur de clé manquante
    mock_secrets.__getitem__.side_effect = KeyError("Key not found")
    
    resultat = get_ai_analysis("Contexte")
    assert "Erreur" in resultat or "config" in resultat