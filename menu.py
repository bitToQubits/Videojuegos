# -*- coding: latin-1 -*-
from select import select
import pygame

# Configuraci�n de la pantalla
pygame.init()
pygame.display.set_caption("Rage Arcade")
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
# Definici�n de las opciones del men� y su posici�n
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
    #Posici�n Vertical.
    y = (screen.get_height() - height * len(options)) // 2 + i * height * 2 
    option_positions.append((x, y))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Explont/data/fonts/font.ttf", size)

def main_menu():
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
                        import Explont.explont as explont
                        explont.explont()
                    elif selected_option == 1:
                        import TempestRun.main as tempest
                        tempest._main()
                    elif selected_option == 2:
                        import DonkeyKong.main as donkey
                        donkey._main()

        # Dibujar el t�tulo en la pantalla
        screen.fill((255, 255, 255))
        title = get_font(45).render("Rage Arcade", True, (253,0,29))
        title_pos = ((screen.get_width() - title.get_width()) // 2, 100)
        screen.blit(title, title_pos)

        # Dibujar las opciones en la pantalla
        for i in range(len(options)):  
            text = get_font(30).render(options[i], True, (0, 0, 0))
            text_rect = text.get_rect(center=option_positions[i])
            screen.blit(text, text_rect)
            #Resaltar la opci�n seleccionada
            if i == 0 and i == selected_option:
                highlight_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
                pygame.draw.rect(screen, '#c0c741', highlight_rect, 5)
            elif i == 1 and i == selected_option:
                highlight_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
                pygame.draw.rect(screen, '#2081F7', highlight_rect, 5)
            elif i == 2 and i == selected_option:
                highlight_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
                pygame.draw.rect(screen, '#4B1A09', highlight_rect, 5)
            elif i == 3 and i == selected_option:
                highlight_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
                pygame.draw.rect(screen, '#E11C00', highlight_rect, 5)
        pygame.display.update()

main_menu()