import pygame
import sys

pygame.init()

# Set up the clock
clock = pygame.time.Clock()

# Farben
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pong')

# Set up font
font = pygame.font.Font(None, 36)

spielaktiv = True

# Schleife Hauptprogramm
while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
            print("Spieler hat Quit-Button angeklickt")

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Spiellogik hier integrieren

    # Spielfeld löschen
    screen.fill(SCHWARZ)

    # Spielfeld/figuren zeichnen
    text = font.render(f"Mouse Position: ({mouse_x}, {mouse_y})", True, WEISS)
    screen.blit(text, (20, 20))
    pygame.draw.rect(screen, WEISS, [55, 20, 25, 100], 0)

    # Fenster aktualisieren
    pygame.display.flip()

    # Refresh-Zeiten festlegen
    clock.tick(60)

pygame.quit()
sys.exit()
