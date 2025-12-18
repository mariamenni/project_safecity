import streamlit as st
from groq import Groq

def get_groq_client():
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return None

def get_ai_analysis(context_data, user_question=None, mode="rapport"):
    """
    Modes disponibles : "tendance", "comparaison", "chat", "rapport"
    """
    client = get_groq_client()
    if not client: return "⚠️ Erreur config API."

    # --- INSTRUCTIONS SELON LE MODE ---
    if mode == "tendance":
        sys_prompt = "Tu es un expert temporel. Analyse UNIQUEMENT l'évolution (Hausse/Baisse) entre N et N-1. Sois bref et direct."
        user_task = "Quelle est la tendance temporelle exacte ?"
        
    elif mode == "comparaison":
        sys_prompt = "Tu es un expert géographe. Contextualise le chiffre du département par rapport à la moyenne nationale et la densité."
        user_task = "Compare la zone critique avec la moyenne nationale."
        
    elif mode == "chat":
        sys_prompt = "Tu es un assistant factuel. Réponds à la question en te basant sur les données."
        user_task = f"Question : {user_question}"
        
    else: # mode "rapport"
        sys_prompt = "Tu es un consultant sécurité. Rédige une synthèse complète et structurée (Situation, Tendance, Contexte)."
        user_task = "Rédige le rapport complet."

    # --- APPEL API ---
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"DONNÉES: {context_data}\n\nCONSIGNE: {user_task}"}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erreur : {e}"