# -*- coding: latin-1 -*-
import pygame
from Explont.explont import juego
import main as tempest

# Configuración de la pantalla
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # pantalla completa
pygame.display.set_caption("Explon't")
pygame.mouse.set_visible(False)

# Definición de las opciones del menú y su posición
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 80)
options = ["Explont", "Tempest Run","Donkey Kong","Rage"]
option_positions = []
for i in range(len(options)):
    text = font.render(options[i], True, (0, 0, 0))
    width, height = text.get_size()
    if i == 1:
        x = (screen.get_width() - width) // 1.65 #Posicion Horizontal.
    else:
        x = (screen.get_width() - width) // 1.9 #Posicion Horizontal.
    #Posición Vertical.
    y = (screen.get_height() - height * len(options)) // 2 + i * height * 2 
    option_positions.append((x, y))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Explont/data/fonts/font.ttf", size)

def main_menu():
    selected_option = 0
    # Bucle principal del juego
    while True:
        # Manejar eventos de teclado
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_option > 0:
                    selected_option -= 1
                elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                    selected_option += 1

                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        juego()
                    elif selected_option == 1:
                        tempest._main()
                    elif selected_option == 2:
                        import DonkeyKong.main

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # Dibujar el título en la pantalla
        screen.fill((255, 255, 255))
        title = get_font(45).render("Explon't", True, (0, 0, 0))
        title_pos = ((screen.get_width() - title.get_width()) // 2, 100)
        screen.blit(title, title_pos)

        # Dibujar las opciones en la pantalla
        for i in range(len(options)):
            text = get_font(30).render(options[i], True, (0, 0, 0))
            text_rect = text.get_rect(center=option_positions[i])
            screen.blit(text, text_rect)
            #Resaltar la opción seleccionada
            if i == selected_option:
                highlight_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
                pygame.draw.rect(screen, '#c0c741', highlight_rect, 5)

        pygame.display.update()


def ayuda():
    while True:
        screen.fill((255, 255, 255))

        title = get_font(40).render("Controles", True, '#065aa0')
        title_pos = ((screen.get_width() - title.get_width()) // 2, 100)
        screen.blit(title, title_pos)

        title = get_font(20).render("Presiona Start para volver.", True, (0, 0, 0))
        title_pos = ((screen.get_width() - title.get_width()) // 10, 950)
        screen.blit(title, title_pos)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        
        pygame.display.update()

main_menu()