import os
from dotenv import load_dotenv
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

import re

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
                "text": "Génère une phrase courte, positive, et agréable en français qui décrit un instant capturé par une caméra située sur un Raspberry Pi. La description doit être basée uniquement sur l'image observée et doit transmettre un message positif et encourageant à ceux qui la lisent. Sois attentif aux détails présents dans l'image et tente de capturer l'essence même de l'interaction, en infusant plus de dynamisme et de présence dans la formulation.\n\nUtilise un langage familier et tutoie les personnes dans la phrase. Infuse des mots gentils, chaleureux et familiaux pour renforcer le côté convivial et réconfortant.\n\nLa phrase doit être:\n- Positive et mettant en valeur l'instant présent ou l'interaction capturée, en observant bien les détails de l'image.\n- Orientée principalement sur les personnes et le moment de complicité, sans mentionner le décor ou l'environnement en détail.\n- Courte, conviviale, encourageante, familiale, et rédigée en français.\n- Dans un style qui apporte un sentiment de joie, de réconfort, et qui traduise subtilement les détails uniques observés dans l'image, afin d'apporter de la vivacité au message.\n\n# Output Format\n\nLa sortie doit consister en une seule phrase, en français, qui véhicule un sentiment chaleureux, convivial et inspirant. La phrase doit être concise, d'une longueur d'environ 10 à 15 mots, et doit être rédigée en tutoyant les personnes impliquées.\n\n# Examples\n\n- \"On dirait que ton sourire illumine tout autour, quel bonheur partagé !\"\n- \"C'est un moment parfait pour des rires complices, continuez comme ça !\"\n- \"Votre amitié, si sincère, apporte une belle lumière dans cette image.\"\n\n(Note: Ces exemples sont représentatifs, mais la phrase générée doit s'adapter scrupuleusement à ce qui est observé dans l'image. Chaque détail vu doit enrichir la description pour capturer un sentiment plus profond.)"
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
        content = re.sub(r'^"|"$', '', content)  # Retire les guillemets au début et à la fin
        print(f"Légende générée: {content}")
        return content
    
    return retry(request_caption)