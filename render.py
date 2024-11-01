from PIL import Image, ImageDraw, ImageFont
import subprocess

import logging

import shutil

# Fonction pour créer une image avec une légende
# Ajout du wrapping de texte

def create_image_with_caption(caption, output_path):
    try:
        logging.debug(f"Création de l'image avec la légende: {caption}")
        image = Image.new("RGB", (800, 480), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            logging.warning("Police Arial non trouvée, utilisation de la police par défaut.")
            font = ImageFont.load_default()  # Pour une meilleure qualité, installer une police comme Arial
        
        # Wrapper le texte pour qu'il ne déborde pas
        max_width = 750
        lines = []
        words = caption.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}" if line else word
            width, _ = draw.textbbox((0, 0), test_line, font=font)[2:]  # Correction pour utiliser textbbox correctement
            if width <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)  # Ajouter la dernière ligne
        
        y_offset = 50
        for line in lines:
            draw.text((25, y_offset), line, fill=(200, 200, 200), font=font)
            y_offset += 40  # Espacement entre les lignes
        
        image.save(output_path)
        logging.info(f"Image créée avec la légende: {output_path}")
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'image: {e}")
        raise SystemExit(f"Erreur critique: {e}")

# Fonction pour afficher l'image sur l'écran du Raspberry Pi
def display_image(image_path):
    if shutil.which("fim") is None:
        logging.error("Le programme 'fim' n'est pas installé. Veuillez l'installer pour pouvoir afficher l'image.")
        raise SystemExit("Erreur critique: 'fim' non installé.")
    try:
        logging.debug(f"Affichage de l'image: {image_path}")
        subprocess.run(["fim", "--quiet", image_path], check=True)
        logging.info(f"Image affichée: {image_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors de l'affichage de l'image: {e}")
        raise SystemExit(f"Erreur critique: {e}")