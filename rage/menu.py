# -*- coding: latin -*-
import pygame

# Configuración de la pantalla
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # pantalla completa
pygame.display.set_caption("Rage")
pygame.mouse.set_visible(False)

# Definición de las opciones del menú y su posición
font = pygame.font.Font(None, 50)
big_font = pygame.font.Font(None, 100)
options = ["Jugar", "Ayuda"]
option_positions = [((screen.get_width()/2)-50, (screen.get_height()/2)-20), ((screen.get_width()/2)-50, (screen.get_height()/2)+40)]
selected_option = 0

# Bucle principal del juego
while True:
    # Manejar eventos de teclado
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = 0
            elif event.key == pygame.K_DOWN:
                selected_option = 1
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    print("Inicializando juego...")
                elif selected_option == 1:
                    print("Mostrando la ayuda...")
                pygame.quit()
                quit()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    # Dibujar el título en la pantalla
    screen.fill((255, 255, 255))
    title = big_font.render("Explon't", True, (0, 0, 0))
    title_pos = ((screen.get_width()/2)-(title.get_width()/2), 100)
    screen.blit(title, title_pos)

    # Dibujar las opciones en la pantalla
    for i in range(len(options)):
        text = font.render(options[i], True, (0, 0, 0))
        text_rect = text.get_rect(center=option_positions[i])
        screen.blit(text, text_rect)
        # Resaltar la opción seleccionada
        if i == selected_option:
            highlight_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
            pygame.draw.rect(screen, (255, 0, 0), highlight_rect, 5)

    pygame.display.update()



