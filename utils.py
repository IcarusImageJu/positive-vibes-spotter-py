import logging
import base64
import time

# Fonction pour encoder l'image en base64
def encode_image_to_base64(image_path):
    try:
        logging.debug(f"Encodage de l'image {image_path} en base64.")
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        logging.info("Image encodée en base64 avec succès.")
        return encoded_string
    except Exception as e:
        logging.error(f"Erreur lors de l'encodage de l'image: {e}")
        raise SystemExit(f"Erreur critique: {e}")
      
      # Fonction de retry avec backoff exponentiel
def retry(func, attempts=5, initial_wait=5, backoff=2):
    wait = initial_wait
    for attempt in range(attempts):
        try:
            logging.debug(f"Tentative {attempt + 1} d'exécution de la fonction {func.__name__}.")
            return func()
        except Exception as e:
            if "429" in str(e):
                logging.warning(f"Trop de requêtes. Tentative {attempt + 1}/{attempts}. Attente de {wait} secondes avant de réessayer...")
                time.sleep(wait)
                wait *= backoff  # Backoff exponentiel
            else:
                logging.error(f"Erreur irrécupérable lors de la tentative {attempt + 1}: {e}")
                raise SystemExit(f"Erreur critique: {e}")
    raise SystemExit("Échec de l'opération après plusieurs tentatives.")