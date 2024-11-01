import os
import time
import base64
from openai import OpenAI
from picamzero import Camera
from PIL import Image, ImageDraw, ImageFont
import subprocess
import random
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration des variables globales
API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
MODEL = "gpt-4o-mini"
IMAGE_PATH = "photo.jpg"
OUTPUT_IMAGE_PATH = "output.png"
CAPTION_TEMPLATE = (
    "Il est {time}, le {date}. Tu es une caméra sur un Raspberry Pi dans mon salon, et tu observes de temps en temps "
    "ce qu’il s’y passe pour afficher un mot sur l’écran du Raspberry. Ton travail c’est d’observer la photo "
    "que je t’envoie et de trouver quelque chose d’agréable et positif à écrire sur l’écran. "
    "Formule uniquement une phrase courte, en français, positive, sympathique, et family friendly."
)

# Initialiser le client OpenAI
client = OpenAI(api_key=API_KEY)

# Fonction pour prendre une photo avec la caméra Pi
def take_photo(image_path):
    cam = Camera()
    cam.still_size(800, 600)
    cam.flip_camera(vflip=True, hflip=True)
    cam.start_preview()
    cam.take_photo(image_path)
    cam.stop_preview()
    print(f"Photo prise avec succès: {image_path}")

# Fonction pour encoder l'image en base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    print("Image encodée en base64 avec succès.")
    return encoded_string

# Fonction pour obtenir la légende à partir de l'API OpenAI
def get_caption(image_base64):
    date = time.strftime("%d %B %Y")
    current_time = time.strftime("%Hh%M")
    content = CAPTION_TEMPLATE.format(time=current_time, date=date)
    
    messages = [
        {"role": "system", "content": content},
        {"role": "user", "content": f"data:image/jpeg;base64,{image_base64}"},
    ]
    retry_attempts = 5
    for attempt in range(retry_attempts):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={"type": "json_object"}
            )
            caption = response["choices"][0]["message"]["content"]
            print(f"Légende générée: {caption}")
            return caption
        except Exception as e:
            if "429" in str(e):
                wait_time = random.uniform(5, 15)
                print(f"Trop de requêtes. Attente de {wait_time} secondes avant de réessayer... (tentative {attempt + 1}/{retry_attempts})")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Échec de la génération de légende après plusieurs tentatives.")

# Fonction pour créer une image avec une légende
def create_image_with_caption(caption, output_path):
    image = Image.new("RGB", (1280, 720), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial", 36)
    except IOError:
        font = ImageFont.load_default()  # Pour une meilleure qualité, installer une police comme Arial
    text_position = (50, 600)
    draw.text(text_position, caption, fill=(255, 255, 255), font=font)
    image.save(output_path)
    print(f"Image créée avec la légende: {output_path}")

# Fonction pour afficher l'image sur l'écran du Raspberry Pi
def display_image(image_path):
    try:
        subprocess.run(["fbi", "-T", "1", "--noverbose", image_path], check=True)
        print(f"Image affichée: {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'affichage de l'image: {e}")

# Fonction principale pour exécuter la tâche
def run_task():
    try:
        # Prendre une photo
        take_photo(IMAGE_PATH)

        # Encoder l'image en base64
        image_base64 = encode_image_to_base64(IMAGE_PATH)

        # Obtenir la légende
        caption = get_caption(image_base64)

        # Créer une image avec la légende
        create_image_with_caption(caption, OUTPUT_IMAGE_PATH)

        # Afficher l'image sur l'écran
        display_image(OUTPUT_IMAGE_PATH)
    except Exception as e:
        print(f"Erreur lors de l'exécution de la tâche: {e}")

if __name__ == "__main__":
    while True:
        run_task()
        time.sleep(3600)  # Exécution de la tâche toutes les heures
