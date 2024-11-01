import time
import logging

from camera import take_photo
from caption import get_caption
from render import create_image_with_caption, display_image
from utils import encode_image_to_base64

# Configuration des variables globales
IMAGE_PATH = "photo.jpg"
OUTPUT_IMAGE_PATH = "output.png"
DEBUG = True

# Configurer le logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction principale pour exécuter la tâche
def run_task():
    try:
        logging.debug("Début de l'exécution de la tâche principale.")
        # Prendre une photo
        take_photo(IMAGE_PATH)

        # Debug
        if DEBUG:
            caption = "Lorem ipsum dolor sit amet consectetur adesciping dolo radum etiam dolore magna aliqua. Ut enim ad minim veniam."
            logging.debug(f"Mode debug activé, légende utilisée: {caption}")
        else:
            # Encoder l'image en base64
            image_base64 = encode_image_to_base64(IMAGE_PATH)
            # Obtenir la légende
            caption = get_caption(image_base64)
        
        # Créer une image avec la légende
        create_image_with_caption(caption, OUTPUT_IMAGE_PATH)

        # Afficher l'image sur l'écran
        display_image(OUTPUT_IMAGE_PATH)
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution de la tâche: {e}")
        raise SystemExit(f"Erreur critique: {e}")

if __name__ == "__main__":
    while True:
        run_task()
        time.sleep(3600)  # Exécution de la tâche toutes les heures
