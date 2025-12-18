import os
from groq import Groq

# 👇 COLLE TA CLÉ ICI JUSTE POUR LE TEST (Ne jamais commiter ce fichier sur GitHub !)
API_KEY = "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" 

def test_ia():
    print("🤖 Tentative de connexion à Groq Cloud...")
    
    try:
        # 1. Connexion
        client = Groq(api_key=API_KEY)

        # 2. Envoi de la demande
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en sécurité urbaine concis."
                },
                {
                    "role": "user",
                    "content": "Explique en une phrase pourquoi l'analyse de données aide la police."
                }
            ],
            # On utilise Mixtral (le modèle français très puissant)
            model="llama-3.3-70b-versatile",
        )

        # 3. Affichage de la réponse
        reponse = chat_completion.choices[0].message.content
        print("\n✅ SUCCÈS ! Réponse de l'IA :\n")
        print(reponse)

    except Exception as e:
        print(f"\n❌ ERREUR : {e}")

if __name__ == "__main__":
    test_ia()