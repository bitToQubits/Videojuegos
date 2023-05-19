#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys
from clip import clip

path = input('path to image: ')

SCALE = 2
COLORKEY = (0, 0, 0)
FORCE_BG = (0, 0, 0)

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('spritesheet gen')
screen = pygame.display.set_mode((500, 500),0,32)
img = pygame.image.load(path).convert()
display_dimensions = [img.get_width() * SCALE, img.get_height() * SCALE]
screen = pygame.display.set_mode(display_dimensions,0,32)

display = img.copy()

clicking = None

def generate_borders(base_range):
    corners = [[min(base_range[0][0], base_range[1][0]), min(base_range[0][1], base_range[1][1])],
               [max(base_range[0][0], base_range[1][0]), min(base_range[0][1], base_range[1][1])],
               [max(base_range[0][0], base_range[1][0]), max(base_range[0][1], base_range[1][1])],
               [min(base_range[0][0], base_range[1][0]), max(base_range[0][1], base_range[1][1])],
               ]
    while True:
        full_clear = True
        for i in range(4):
            clear = True
            if i == 0: # top
                for j in range(corners[1][0] - corners[0][0] + 1):
                    c = img.get_at((corners[0][0] + j, corners[0][1]))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[0][1] -= 1
                    corners[1][1] -= 1

            clear = True   
            if i == 1: # right
                for j in range(corners[2][1] - corners[1][1] + 1):
                    c = img.get_at((corners[1][0], corners[1][1] + j))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[1][0] += 1
                    corners[2][0] += 1

            clear = True
            if i == 2: # bottom
                for j in range(corners[2][0] - corners[3][0] + 1):
                    c = img.get_at((corners[3][0] + j, corners[3][1]))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[2][1] += 1
                    corners[3][1] += 1

            clear = True
            if i == 3: # left
                for j in range(corners[3][1] - corners[0][1] + 1):
                    c = img.get_at((corners[0][0], corners[0][1] + j))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[0][0] -= 1
                    corners[3][0] -= 1
        if full_clear:
            break
                
    return corners

def generate_tileset():
    rect_form_clips = []
    for sec in clip_sections:
        row = sec[0]
        while row >= len(rect_form_clips):
            rect_form_clips.append([])
        sec = sec[1]
        rect_form_clips[row].append(pygame.Rect(sec[0][0] + 1, sec[0][1] + 1, sec[2][0] - sec[0][0] - 1, sec[2][1] - sec[0][1] - 1))

    max_width = 0
    height = 0
    for row in rect_form_clips:
        width = sum([sec.width + 2 for sec in row]) + 1
        height += max([sec.height + 2 for sec in row])
        max_width = max(width, max_width)

    tileset_surf = pygame.Surface((max_width, height))
    tileset_surf.fill(FORCE_BG)
    y = 0
    for row in rect_form_clips:
        tileset_surf.set_at((0, y), (255, 255, 0))
        x = 1
        for sec in row:
            sec_img = clip(img, sec.x, sec.y, sec.width, sec.height)
            if FORCE_BG:
                sec_img.set_colorkey(COLORKEY)
            tileset_surf.blit(sec_img, (x + 1, y + 1))
            tileset_surf.set_at((x, y), (255, 0, 255))
            tileset_surf.set_at((x + sec.width + 1, y), (0, 255, 255))
            tileset_surf.set_at((x, y + sec.height + 1), (0, 255, 255))
            x += sec.width + 2
        y += max([sec.height + 2 for sec in row])
    return tileset_surf

clip_sections = []
current_row = 0
generate_mode = False
save_count = 0

# Loop ------------------------------------------------------- #
while True:
    
    # Background --------------------------------------------- #
    display.fill((0,0,0))
    if not generate_mode:
        display.blit(img, (0, 0))

        mx, my = pygame.mouse.get_pos()
        mx = int(mx / SCALE)
        my = int(my / SCALE)

        for sec in clip_sections:
            c = (255, 0, 255)
            if sec[0] != current_row:
                c = (0, 255, 255)
            pygame.draw.polygon(display, c, sec[1], 1)

        if clicking:
            pygame.draw.rect(display, (255, 0, 255), pygame.Rect(clicking[0], clicking[1], mx-clicking[0], my-clicking[1]), 1)

    else:
        display.blit(genned_tileset, (0, 0))
    
    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_z:
                if clip_sections != []:
                    clip_sections.pop(-1)
            if event.key == K_r:
                current_row += 1
            if event.key == K_c:
                clip_sections = []
            if event.key == K_s:
                pygame.image.save(display, 'save_' + str(save_count) + '.png')
                save_count += 1
            if event.key == K_g:
                if not generate_mode:
                    generate_mode = True
                    genned_tileset = generate_tileset()
                    display_dimensions = [genned_tileset.get_width() * SCALE, genned_tileset.get_height() * SCALE]
                    screen = pygame.display.set_mode(display_dimensions,0,32)
                    display = genned_tileset.copy()
                else:
                    generate_mode = False
                    display = img.copy()
                    display_dimensions = [img.get_width() * SCALE, img.get_height() * SCALE]
                    screen = pygame.display.set_mode(display_dimensions,0,32)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = [mx, my]
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if clicking != None:
                    clip_sections.append([current_row,generate_borders([clicking, [mx, my]])])
                clicking = None
                
    # Update ------------------------------------------------- #
    screen.blit(pygame.transform.scale(display, display_dimensions), (0, 0))
    pygame.display.update()
    mainClock.tick(60)
    
