import logging
import time
from picamzero import Camera

# Fonction pour prendre une photo avec la caméra Pi
def take_photo(image_path):
    try:
        logging.debug("Initialisation de la caméra pour prendre une photo.")
        cam = Camera()
        cam.still_size = (800, 480)
        cam.preview_size = (800, 480)
        cam.flip_camera(vflip=True, hflip=True)
        cam.start_preview()
        time.sleep(2)
        cam.take_photo(image_path)
        cam.stop_preview()
        logging.info(f"Photo prise avec succès: {image_path}")
    except Exception as e:
        logging.error(f"Erreur lors de la prise de la photo: {e}")
        raise SystemExit(f"Erreur critique: {e}")