import os
import time
from picamzero import Camera

is_interactive = os.isatty(0)
IMAGE_PATH = "photo.jpg"

# Fonction pour prendre une photo avec la caméra Pi
def take_photo():
    try:
        print("Initialisation de la caméra pour prendre une photo.")
        cam = Camera()
        cam.still_size = (800, 480)
        cam.preview_size = (800, 480)
        cam.flip_camera(vflip=True, hflip=True)
        
        # Si on est sur un terminal interactif, alors lancer la prévisualisation
        if is_interactive:
            cam.start_preview()
        time.sleep(2)
        cam.take_photo(IMAGE_PATH)
        
        if is_interactive:
            cam.stop_preview()
            
        print(f"Photo prise avec succès: {IMAGE_PATH}")
        
        return IMAGE_PATH
    except Exception as e:
        print(f"Erreur lors de la prise de la photo: {e}")
        raise SystemExit(f"Erreur critique: {e}")