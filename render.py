import os
import pygame
import time

SCREEN_SIZE = (800, 480)

# Fonction pour créer une légende et des masques en damier dynamiquement pour prévenir le burn-in des pixels
def draw_caption_with_checkerboard(screen, caption, font, clock, duration):
    # Initialiser les couleurs
    text_color = (175, 175, 175)
    background_color = (0, 0, 0)
    checker_color = (0, 0, 0)
    checker_size = 2  # Augmenter la taille du damier pour une meilleure visibilité
    
    # Découper la légende en lignes pour qu'elle ne déborde pas
    max_width = 750
    lines = []
    words = caption.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}" if line else word
        width, _ = font.size(test_line)
        if width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)  # Ajouter la dernière ligne

    running = True
    frame = 0
    end_time = time.time() + duration  # Fixe la durée de fonctionnement à une heure
    while running and time.time() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Remplir l'arrière-plan
        screen.fill(background_color)

        # Dessiner la légende
        y_offset = 50
        for line in lines:
            text_surface = font.render(line, True, text_color)
            screen.blit(text_surface, (25, y_offset))
            y_offset += 56  # Espacement entre les lignes

        # Appliquer le motif en damier animé par-dessus le texte
        for x in range(0, SCREEN_SIZE[0], checker_size):
            for y in range(0, SCREEN_SIZE[1], checker_size):
                if (x // checker_size + y // checker_size + (frame // 20)) % 2 == 0:
                    pygame.draw.rect(screen, checker_color, (x, y, checker_size, checker_size))

        # Afficher les modifications
        pygame.display.flip()

        # Attendre avant la prochaine frame
        frame += 1
        clock.tick(30)
        
def render(caption, duration=3600):
    # Définir la variable d'environnement si elle n'est pas définie
    if not os.environ.get("XDG_RUNTIME_DIR"):
        os.environ["XDG_RUNTIME_DIR"] = "/tmp"

    # Initialiser Pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.mouse.set_visible(False)  # Masquer le curseur de la souris
    clock = pygame.time.Clock()

    # Charger la police
    try:
        font = pygame.font.Font(pygame.font.match_font('arial'), 48)
    except IOError:
        print("Police Arial non trouvée, utilisation de la police par défaut.")
        font = pygame.font.Font(pygame.font.get_default_font(), 48)

    # Afficher la légende avec le motif en damier
    draw_caption_with_checkerboard(screen, caption, font, clock, duration)

    pygame.quit()

# Exemple d'utilisation
if __name__ == "__main__":
    caption = "Ceci est un exemple de légende pour tester l'affichage alterné."
    render(caption)
