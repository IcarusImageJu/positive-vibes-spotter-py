import os
from dotenv import load_dotenv
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

from utils import retry

API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
MODEL = "gpt-4o-mini"

# Initialiser le client OpenAI
from openai import OpenAI
client = OpenAI()

# Fonction pour obtenir la légende à partir de l'API OpenAI
def get_caption(image_base64):
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Tu es une caméra sur un Raspberry Pi dans mon salon. Tu observes de temps en temps ce qu’il s'y passe et affiches un mot sur l’écran du Raspberry. "
                        "Ton travail consiste à observer la photo que je t’envoie et à trouver un détail particulier pour formuler quelque chose d’agréable et positif lié à ce détail. "
                        "L'objectif est d'écrire une phrase courte en français, positive, sympathique, et family friendly. Mentionne spécifiquement quelque chose que tu vois sur la photo que tu trouves charmant ou joyeux.\n\n"
                        "# Exigences\n"
                        "- Utilise un détail précis visible sur l'image.\n"
                        "- Assure-toi que la phrase soit courte, sympathique, et optimiste.\n\n"
                        "# Format de Sortie\n"
                        "- Une seule phrase en français.\n"
                        "- Évoque un détail clair de l'image que tu trouves agréable.\n\n"
                        "# Exemples\n"
                        "**Image Input Détail :** Un chat endormi sur le canapé.\n"
                        "**Phrase Output :** \"Ce chat a vraiment trouvé l'endroit parfait pour se détendre, c'est adorable!\"\n\n"
                        "**Image Input Détail :** Une lumière douce qui éclaire la table avec des livres.\n"
                        "**Phrase Output :** \"La lumière douce sur ces livres crée une atmosphère merveilleusement apaisante.\"\n\n"
                        "# Notes\n"
                        "- Cherche toujours quelque chose de charmant ou joyeux.\n"
                        "- Évite les répétitions ; chaque observation doit être unique à l’image reçue.\n"
                        "- Assure-toi que le ton reste léger et invitant."
                    )
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ]
    
    def request_caption():
        print("Envoi de la requête à l'API OpenAI pour obtenir la légende.")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "text"}
        )
        content = response.choices[0].message.content
        print(f"Légende générée: {content}")
        return content
    
    return retry(request_caption)