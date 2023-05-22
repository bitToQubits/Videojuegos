# -*- coding: utf-8 -*-
from select import select
import pygame
import math
import random

import pygame

import TempestRun.rendering.neon as neon
import TempestRun.keybinds as keybinds
import TempestRun.util.fonts as fonts
import TempestRun.config as config
from TempestRun.sound_manager.SoundManager import SoundManager

# Configuraci�n de la pantalla
pygame.init()
SoundManager.init()
pygame.display.set_caption("Rage Arcade")
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Explont/data/fonts/font.ttf", size)

def main_menu():
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    title_font = fonts.get_font(40,name="blocky")
    subtitle_font = fonts.get_font(20,name="blocky")
    option_font = fonts.get_font(15,name="blocky")
    info_font = fonts.get_font(20)
    TARGET_FPS = config.Display.fps if not config.Debug.fps_test else -1
    n_squares = 25
    squares = [_generate_square() for _ in range(n_squares)]  # format -> [x, y, angle, speed]
    options = [
            ("Explon't", None),
            ("Tempest Run", None),
            ("Donkey Kong", None),
            ("Rage", None)
        ]
    selected_option_idx = 0
    # Bucle principal del juego
    while True:
        clock = pygame.time.Clock()
        dt = clock.tick(TARGET_FPS) / 1000.0
        for i in squares:
            i[2] += i[3] * dt * 100
            i[1] -= abs(i[3]) * dt  * 100
        squares = [s for s in squares if s[1] > -50]  # purge squares that fell off the top of the screen

        while len(squares) < n_squares:
            squares.append(_generate_square())

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key in keybinds.LEFT:
                    SoundManager.play('blip')
                    selected_option_idx = (selected_option_idx - 1) % len(options)
                elif e.key in keybinds.RIGHT:
                    SoundManager.play('blip')
                    selected_option_idx = (selected_option_idx + 1) % len(options)
                elif e.key in keybinds.MENU_CANCEL:
                    SoundManager.play('blip2')
                elif e.key in keybinds.MENU_ACCEPT:
                    SoundManager.play("accept")
                    if selected_option_idx == 0:
                        import Explont.explont as explont
                        explont.explont()
                    if selected_option_idx == 1:
                        import TempestRun.main as tempest
                        tempest._main()
                    if selected_option_idx == 2:
                        import DonkeyKong.main as donkey
                        donkey._main()
                    if selected_option_idx == 3:
                        import rage.main as rage
                        rage._main()
                    

        screen.fill((0, 0, 0))

        for i in squares:
            pygame.draw.lines(screen, (0, 255, 0), True, get_square_points(i[0], i[1], i[2]))
        screen_size = screen.get_size()
        title_surface = title_font.render('RAGE ARCADE', False, neon.RED)

        title_size = title_surface.get_size()
        title_y = screen_size[1] // 4 - title_size[1] // 2
        screen.blit(title_surface, dest=(screen_size[0] // 2 - title_size[0] // 2,
                                         title_y))

        option_y = max(screen_size[1] // 2, title_y + title_size[1])
        msgs = []
        for i in range(len(options)):
            option_text = options[i][0]
            is_selected = i == selected_option_idx
            color = neon.WHITE
            if is_selected:
                if i == 0:
                    msgs = ['↑ Joystick arriba o [X] para saltar',
                            '← Joystick a Izquierda',
                            '→ Joystick a Derecha',
                            '[start] para menú']
                    color = neon.LIME
                    title_bottom = subtitle_font.render('Press [x] to start', False, color)
                    subtitle_size = title_bottom.get_size()
                    screen.blit(title_bottom, dest=(screen_size[0] // 2 - subtitle_size[0] // 2,
                                                 title_y+630))
                elif i == 1:
                    msgs = ['↑ Joystick arriba o [X] para saltar',
                            '← Joystick a Izquierda',
                            '→ Joystick a Derecha',
                            '↓ Joystick abajo para deslizarte',
                            '[O] para resetear el nivel',
                            'presiona [X] para volver o aceptar',
                            '[start] para menú']
                    color = (11,116,255)
                    title_bottom = subtitle_font.render('Press [x] to start', False, color)
                    subtitle_size = title_bottom.get_size()
                    screen.blit(title_bottom, dest=(screen_size[0] // 2 - subtitle_size[0] // 2,
                                         title_y+630))
                elif i == 2:
                    msgs = ['↑ Joystick arriba para subir', '[X] para saltar','← Joystick a Izquierda','→ Joystick a Derecha','[start] para menú']
                    color = (241,166,112)
                    title_bottom = subtitle_font.render('Press [x] to start', False, color)
                    subtitle_size = title_bottom.get_size()
                    screen.blit(title_bottom, dest=(screen_size[0] // 2 - subtitle_size[0] // 2,
                                                 title_y+630))
                elif i == 3:
                    color = neon.RED
                    title_bottom = subtitle_font.render('Press [x] to start', False, color)
                    subtitle_size = title_bottom.get_size()
                    screen.blit(title_bottom, dest=(screen_size[0] // 2 - subtitle_size[0] // 2,
                                                 title_y+630))

            option_surface = option_font.render(option_text.upper(), True, color)
            option_size = option_surface.get_size()
            screen.blit(option_surface, dest=((screen_size[0] // (len(options) + 1)) * (i + 1) - option_size[0] // 2, option_y))
            for index, msg in enumerate(msgs):
                msg_surf = info_font.render(msg, True, neon.WHITE)
                screen.blit(msg_surf, msg_surf.get_rect(center=(screen_size[0] // 2, screen_size[1] * 2 / 3.3 + msg_surf.get_size()[1] * index)))
        pygame.display.update()

def _generate_square():
        screen_w, screen_h = pygame.display.get_surface().get_size()
        return [random.randint(0, screen_w),  # x position
                screen_h + 25,                # y position
                random.randint(0, 360),       # angle
                random.randint(2, 10) / 2 * random.choice([-1, 1])]  # speed

def get_square_points(x, y, angle, size=50):
        # points of a square rotated at an angle with respect to it's center
        points = [
            [-size // 2, - size // 2],
            [size // 2, - size // 2],
            [size // 2, size // 2],
            [-size // 2, size // 2]
        ]
        points = [pygame.Vector2(i[0], i[1]).rotate(angle) for i in points]
        points = [[x + i[0], y + i[1]] for i in points]
        return points


main_menu()