# -*- coding: utf-8 -*-
import pygame

# Configuración de la pantalla
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # pantalla completa
pygame.display.set_caption("Explon't")

# Definición de las opciones del menú y su posición
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 80)
options = ["Jugar", "Ayuda"]
option_positions = []
for i in range(len(options)):
    text = font.render(options[i], True, (0, 0, 0))
    width, height = text.get_size()
    x = (screen.get_width() - width) // 2
    y = (screen.get_height() - height * len(options)) // 2 + i * height * 2
    option_positions.append((x, y))
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
                    print("Iniciando el juego...")
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
    title_pos = ((screen.get_width() - title.get_width()) // 2, 100)
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
