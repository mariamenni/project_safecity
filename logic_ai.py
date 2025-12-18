import streamlit as st
from groq import Groq

def get_groq_client():
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return None

def get_ai_analysis(context_data, user_question=None):
    client = get_groq_client()
    if not client: return "⚠️ Erreur config API."

    # --- LE COEUR DU SUJET : UN PROMPT OPTIMISÉ POUR VOS 4 OBJECTIFS ---
    system_prompt = """
    Tu es SafeCityBot, expert en analyse de données criminelles.
    
    Tes objectifs obligatoires :
    1. ANALYSE TENDANCES : Si des données historiques sont fournies, commente l'évolution (hausse/baisse brutale).
    2. CONTEXTUALISATION : Rapporte toujours les chiffres à la population (densité, taux pour 100k hab) pour nuancer.
    3. DÉTECTION ANOMALIES : Signale si un taux est anormalement élevé par rapport à la moyenne.
    4. SYNTHÈSE : Fais des phrases courtes et percutantes.

    Format de réponse : Markdown propre.
    """

    # --- Construction du message selon le mode ---
    if user_question:
        # MODE 4 : CHATBOT
        user_content = f"""
        DONNÉES :
        {context_data}
        
        QUESTION UTILISATEUR : "{user_question}"
        
        Consigne : Réponds uniquement en te basant sur les données ci-dessus.
        """
    else:
        # MODE 1, 2, 3 : RAPPORT / TENDANCES / COMPARAISON
        user_content = f"""
        DONNÉES :
        {context_data}
        
        TÂCHE : Génère un rapport de sécurité complet.
        Structure :
        1. 📊 **Situation Globale** (Chiffres clés & Population concernée)
        2. 📈 **Analyse des Tendances** (Évolution N vs N-1, Anomalies détectées)
        3. 🗺️ **Focus Territorial** (Zone critique vs Moyenne nationale)
        4. 💡 **Conclusion** (Synthèse en 1 phrase)
        """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.4
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erreur : {e}"