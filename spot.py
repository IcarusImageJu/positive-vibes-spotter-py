import time
import signal
import sys

from camera import take_photo
from caption import get_caption
from render import render
from utils import encode_image_to_base64

# Configuration des variables globales
DEBUG = False
DURATION = 3600  # Durée de fonctionnement de la tâche en secondes

# Gestionnaire de signal pour terminer le programme
def signal_handler(sig, frame):
    print("Signal d'arrêt reçu, arrêt immédiat du programme...")
    sys.exit(0)  # Sortie immédiate du programme avec un code 0 (succès)

# Enregistrer le gestionnaire pour les signaux SIGINT et SIGTERM
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Fonction principale pour exécuter la tâche
def run_task():
    try:
        print("Début de l'exécution de la tâche principale.")
        # Prendre une photo
        image_path = take_photo()

        # Mode debug
        if DEBUG:
            caption = "Lorem ipsum dolor sit amet consectetur adesciping dolo radum etiam dolore magna aliqua. Ut enim ad minim veniam."
            print(f"Mode debug activé, légende utilisée: {caption}")
        else:
            # Encoder l'image en base64
            image_base64 = encode_image_to_base64(image_path)
            # Obtenir la légende
            caption = get_caption(image_base64)

        # Afficher la légende sur l'écran
        render(caption, DURATION)  # Cette fonction dure DURATION secondes
    except Exception as e:
        print(f"Erreur lors de l'exécution de la tâche: {e}")
        sys.exit(f"Erreur critique: {e}")  # Sortie immédiate en cas d'erreur critique

if __name__ == "__main__":
    while True:
        run_task()
        print("Redémarrage de la tâche après l'attente définie.")
        