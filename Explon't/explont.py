import os
import sys
import math
import random

import pygame
from pygame.locals import *

import data.tile_map as tile_map
import data.spritesheet_loader as spritesheet_loader
from data.foliage import AnimatedFoliage
from data.entity import Entity, outline
from data.anim_loader import AnimationManager
from data.grass import GrassManager
from data.text import Font
from data.particles import Particle, load_particle_images

def load_img(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0, 0, 0))
    return img

class GameData:
    def __init__(self):
        self.reset()
        self.death_reset()
        self.tutorial = 2

    def death_reset(self):
        self.level = 1
        self.anger = 0

    def reset(self):
        self.scroll = []
        self.lollipops = []
        self.enemy_spawns = []
        self.spawn = (0, 0)
        self.edges = [999999, -999999, 999999, -999999]
        self.level_map = None
        self.player = None
        self.input = [False, False, False]
        self.clouds = []
        self.grass_manager = GrassManager('data/images/grass', tile_size=16)
        self.circle_particles = []
        self.enemies = []
        self.game_over = 0
        self.animations = []
        self.projectiles = []
        self.transition_state = 1
        self.transition_direction = -1
        self.screenshake = 0
        self.completed_level = 0
        self.init_lollipops = 0
        self.level_notice = 1
        self.sparks = []
        self.circles = []
        self.leaves = []

    def render_level_mask(self):
        width = self.edges[1] - self.edges[0]
        height = self.edges[3] - self.edges[2]

        mask_surf = pygame.Surface((width, height))
        mask_surf.set_colorkey((0, 0, 0))

        render_list = gd.level_map.get_visible([self.edges[0], self.edges[2]], size_override=(width, height))
        for layer in render_list:
            layer_id = layer[0]
            for tile in layer[1]:
                if tile[1][0] not in ['foliage', 'decor']:
                    offset = [0, 0]
                    if tile[1][0] in spritesheets_data:
                        tile_id = str(tile[1][1]) + ';' + str(tile[1][2])
                        if tile_id in spritesheets_data[tile[1][0]]:
                            if 'tile_offset' in spritesheets_data[tile[1][0]][tile_id]:
                                offset = spritesheets_data[tile[1][0]][tile_id]['tile_offset']
                    img = spritesheet_loader.get_img(spritesheets, tile[1])
                    mask_surf.blit(img, (tile[0][0] - self.edges[0] + offset[0], tile[0][1] - self.edges[2] + offset[1]))

        self.level_mask = pygame.mask.from_surface(mask_surf)

    def add_animation(self, animation_id, pos):
        self.animations.append(AnimationE(animation_manager, pos, (2, 2), animation_id))

    def spawn_enemy(self):
        spawn = random.choice(self.enemy_spawns)
        self.enemies.append(Enemy(animation_manager, [spawn[0][0], spawn[0][1] - 1], (7, 17), 'enemy'))

    def load_map(self, name):
        self.reset()

        self.level_map = tile_map.TileMap((TILE_SIZE, TILE_SIZE), display.get_size())
        self.level_map.load_map('data/maps/' + name + '.json')

        for entity in self.level_map.load_entities():
            entity_type = entity[2]['type'][1]
            if entity_type == 0:
                self.lollipops.append(Lollipop(animation_manager, entity[2]['raw'][0], (7, 16), 'lollipop'))
            if entity_type == 2:
                self.enemy_spawns.append([entity[2]['raw'][0]])
            if entity_type == 1:
                self.spawn = entity[2]['raw'][0]

        self.init_lollipops = len(self.lollipops)

        self.level_map.load_grass(self.grass_manager)

        self.scroll = [self.spawn[0] - display.get_width() // 2, self.spawn[1] - display.get_height() // 2]

        for pos in self.level_map.tile_map:
            x = pos[0] * TILE_SIZE
            y = pos[1] * TILE_SIZE
            if x < self.edges[0]:
                self.edges[0] = x
            if x > self.edges[1]:
                self.edges[1] = x + TILE_SIZE
            if y < self.edges[2]:
                self.edges[2] = y
            if y > self.edges[3]:
                self.edges[3] = y + TILE_SIZE

        width = self.edges[1] - self.edges[0]
        height = self.edges[3] - self.edges[2]
        area = width * height
        for i in range(int(area // 10000)):
            self.clouds.append([random.randint(0, len(cloud_images) - 1), (random.random() + 1) / 5, (self.edges[0] + random.random() * (width + display.get_width())) * PARALLAX, random.randint(self.edges[2], self.edges[3] - int(height * 0.3) + display.get_height()) * PARALLAX])

        gd.player = Player(animation_manager, (gd.spawn[0] - 2, gd.spawn[1] - 9), (20, 25), 'player')

        for i in range(gd.level * 2):
            self.spawn_enemy()

        self.render_level_mask()

class AnimationE(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.dead = False

    def update(self):
        super().update(1 / 60)
        if self.active_animation.frame >= self.active_animation.data.duration:
            self.dead = True

class Lollipop(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.hit = 0
        self.velocity = [0, 0]
        self.dead = False

    def update(self, gd):
        super().update(1 / 60)
        if not self.hit:
            if self.rect.colliderect(gd.player.rect):
                self.hit = 1
                self.velocity[0] = gd.player.velocity[0] / abs(gd.player.velocity[0]) * 2 if gd.player.velocity[0] else 0
                self.velocity[1] = -5.5
                gd.player.await_eat += 1
                gd.circles.append([self.center, 3, 1, 3, 0.12, 0.9, (247, 237, 186)])
                sounds['touch'].play()
        else:
            self.hit += 1
            if gd.player.eating:
                if gd.player.center[0] < self.center[0]:
                    gd.player.flip[0] = False
                else:
                    gd.player.flip[0] = True
                if abs(gd.player.center[0] - self.center[0]) > 10:
                    if gd.player.center[0] > self.center[0]:
                        self.velocity[0] += 0.25
                    else:
                        self.velocity[0] -= 0.25
                if abs(gd.player.center[1] - self.center[1]) > 10:
                    if gd.player.center[1] > self.center[1]:
                        self.velocity[1] += 0.25
                    else:
                        self.velocity[1] -= 0.25

                if math.sqrt(abs(gd.player.center[0] - self.center[0]) ** 2 + abs(gd.player.center[1] - self.center[1]) ** 2) < 10:
                    sounds['crunch'].play()
                    self.dead = True
                    if gd.tutorial == 1:
                        gd.tutorial = 0
                    gd.anger -= 5
                    gd.player.eating -= 1
                    gd.player.chomp = True
                    for i in range(12):
                        c = random.choice([(157, 48, 59), (157, 48, 59), (157, 48, 59), (157, 48, 59), (210, 100, 113), (210, 100, 113)])
                        gd.circle_particles.append(['flesh', self.center, [random.random() * 2 - 1, random.random() * 3 - 2], c, random.random() * 3.5 + 1, 0.005, 0])
                    gd.circles.append([self.center, 7, 1, 4.5, 0.15, 0.87, (247, 237, 186)])

            if self.hit > 10:
                self.velocity[0] *= 0.95
                self.velocity[1] *= 0.95

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def render(self, surf, scroll):
        scroll = scroll.copy()
        scroll[1] += round(math.sin((global_time % 60) / 60 * math.pi * 2), 0)
        super().render(surf, scroll)

class Enemy(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.velocity = [0, 0]
        self.dead = False
        self.walk_dir = random.choice([-1, 1])
        self.speed = random.random() * 0.25 + 0.35
        self.ground_dead = False
        self.sees_player = False
        self.weapon_angle = 0
        self.attack_speed = 80
        self.attack_timer = int(random.random() * self.attack_speed)

    def check_player_path(self, gd):
        surf = pygame.Surface((abs(self.center[0] - gd.player.center[0] + 2), abs(self.center[1] - gd.player.center[1] + 2)))
        top_left = (min(self.center[0], gd.player.center[0]) - 1, min(self.center[1], gd.player.center[1]) - 1)
        pygame.draw.line(surf, (255, 255, 255), (self.center[0] - top_left[0] + 1, self.center[1] - top_left[1] + 1), (gd.player.center[0] - top_left[0] + 1, gd.player.center[1] - top_left[1] + 1))
        if abs(self.center[0] - gd.player.center[0]) < 3:
            return False
        return not bool(gd.level_mask.overlap(pygame.mask.from_surface(surf), (top_left[0] - 1 - gd.edges[0], top_left[1] - 1 - gd.edges[2])))

    def update(self, gd):
        super().update(1 / 60)

        self.velocity[1] = min(4, self.velocity[1] + 0.25)

        self.attack_timer += 1

        temp_motion = self.velocity.copy()

        if not self.dead:
            temp_motion[0] += self.walk_dir * self.speed
            check_loc = None
            if random.random() < 0.01:
                if self.walk_dir:
                    self.walk_dir = 0
                else:
                    self.walk_dir = random.choice([1, -1])
            if self.walk_dir > 0:
                self.flip[0] = False
                check_loc = (self.center[0] + 9, self.rect.bottom + 5)
            if self.walk_dir < 0:
                self.flip[0] = True
                check_loc = (self.center[0] - 9, self.rect.bottom + 5)
            if check_loc:
                if not gd.level_map.tile_collide(check_loc):
                    self.walk_dir *= -1

            if self.walk_dir:
                self.set_action('run')
            else:
                self.set_action('idle')
        elif not self.ground_dead:
            if random.random() < 0.3:
                c = random.choice([(157, 48, 59), (157, 48, 59), (157, 48, 59), (31, 14, 28), (210, 100, 113), (31, 14, 28)])
                gd.circle_particles.append(['flesh', self.center, [random.random() * 2 - 1, 0], c, random.random() * 1.5 + 1, 0.005, 0])

        rects = [t[1] for t in gd.level_map.get_nearby_rects(self.center)]

        collisions = self.move(temp_motion, rects)
        if collisions['bottom']:
            if self.dead:
                self.ground_dead = True
        if collisions['top'] or collisions['bottom']:
            self.velocity[1] = 1
        if collisions['left'] or collisions['right']:
            self.velocity[0] = 0
            self.walk_dir *= -1
        elif self.rect.right > gd.edges[1]:
            self.pos[0] = gd.edges[1] - self.rect.width
            self.walk_dir *= -1
        elif self.pos[0] < gd.edges[0]:
            self.pos[0] = gd.edges[0]
            self.walk_dir *= -1

        if not self.dead:
            if self.sees_player:
                self.set_action('idle')
                self.walk_dir = 0
                if self.attack_timer % self.attack_speed == 0:
                    sounds['shoot'].play()
                    if gd.player.center[0] > self.center[0]:
                        gd.projectiles.append([self.center, -math.radians(self.weapon_angle), 1])
                        for i in range(3):
                            a = -math.radians(self.weapon_angle)
                            a += random.random() * 0.5 - 0.25
                            gd.sparks.append([self.center, a, 3 + random.random() * 2, 3, 0.1, 0.9, 6 + random.random() * 3, 0.97])
                    else:
                        gd.projectiles.append([self.center, math.pi - math.radians(self.weapon_angle), 1])
                        for i in range(3):
                            a = math.pi - math.radians(self.weapon_angle)
                            a += random.random() * 0.5 - 0.25
                            gd.sparks.append([self.center, a, 3 + random.random() * 2, 3, 0.1, 0.9, 6 + random.random() * 3, 0.97])

        player_dis = math.sqrt((gd.player.center[0] - self.center[0]) ** 2 + (gd.player.center[1] - self.center[1]) ** 2)
        if (self.flip[0] and (gd.player.center[0] < self.center[0])) or (not self.flip[0] and (gd.player.center[0] > self.center[0])):
            if player_dis < 150:
                if self.attack_timer % 10 == 0:
                    self.sees_player = self.check_player_path(gd)
            else:
                self.sees_player = False
        else:
            self.sees_player = False

    def render(self, surf, offset):
        super().render(surf, offset)

        if not self.dead:
            weapon_img = gun_img
            if self.flip[0]:
                weapon_img = pygame.transform.flip(weapon_img, True, False)
            if self.sees_player:
                angle = math.atan2(gd.player.center[1] - self.center[1], gd.player.center[0] - self.center[0])
                if self.flip[0]:
                    self.weapon_angle = -math.degrees(angle) + 180
                    weapon_img = pygame.transform.rotate(weapon_img, self.weapon_angle)
                else:
                    self.weapon_angle = -math.degrees(angle)
                    weapon_img = pygame.transform.rotate(weapon_img, self.weapon_angle)
            outline(surf, weapon_img, (self.center[0] - offset[0] - weapon_img.get_width() // 2, self.center[1] - offset[1] - weapon_img.get_height() // 2), (31, 14, 28))
            surf.blit(weapon_img, (self.center[0] - offset[0] - weapon_img.get_width() // 2, self.center[1] - offset[1] - weapon_img.get_height() // 2))

class Player(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.velocity = [0, 0]
        self.speed = 0.8
        self.accel = 0.2
        self.air_time = 0
        self.jump = 19
        self.eating = 0
        self.await_eat = 0
        self.chomp = False
        self.angry = 0
        self.squish_velocity = 0
        self.hurt_timer = 0

    def update(self, gd):
        super().update(1 / 60)

        if self.angry > 0:
            self.angry -= 1

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        if gd.completed_level < 60:
            self.scale[1] += self.squish_velocity
            self.scale[1] = max(0.3, min(self.scale[1], 1.7))
            self.scale[0] = 2 - self.scale[1]

            if self.scale[1] > 1:
                self.squish_velocity -= 0.02
            elif self.scale[1] < 1:
                self.squish_velocity += 0.02
            if self.squish_velocity > 0:
                self.squish_velocity -= 0.008
            if self.squish_velocity < 0:
                self.squish_velocity += 0.008

            if self.squish_velocity != 0:
                if (abs(self.squish_velocity) < 0.03) and (abs(self.scale[1] - 1) < 0.06):
                    self.scale[1] = 1
                    self.squish_velocity = 0

        rects = [t[1] for t in gd.level_map.get_nearby_rects(self.center)]
        if gd.completed_level < 60:
            self.velocity[1] = min(4, self.velocity[1] + 0.25)
        if (abs(self.velocity[0]) > self.speed) or (not (gd.input[0] or gd.input[1])) or self.eating:
            if abs(self.velocity[0]) <= self.speed:
                self.velocity[0] *= 0.85
            else:
                self.velocity[0] *= 0.97
        if abs(self.velocity[0]) < 0.1:
            self.velocity[0] = 0

        if gd.completed_level > 60:
            self.rotation += 18
            self.scale = [max(0, 1 - (gd.completed_level - 60) / 30), max(0, 1 - (gd.completed_level - 60) / 30)]
            self.velocity[1] = -0.3

        if not self.eating and not self.chomp and not gd.completed_level:
            if gd.input[0]:
                self.flip[0] = True
                if self.velocity[0] > -self.speed:
                    self.velocity[0] -= self.accel
                    self.velocity[0] = max(-self.speed, self.velocity[0])
            if gd.input[1]:
                self.flip[0] = False
                if self.velocity[0] < self.speed:
                    self.velocity[0] += self.accel
                    self.velocity[0] = min(self.speed, self.velocity[0])
            if gd.input[2]:
                if self.jump > 0:
                    if self.jump == 19:
                        self.velocity[0] *= 4
                        gd.add_animation('jump', (self.pos[0] - 5, self.pos[1]))
                        sounds['jump'].play()
                        if gd.tutorial == 2:
                            gd.tutorial = 1
                    self.jump -= 1
                    self.velocity[1] = -4.6
                    self.air_time = 6
                    if self.jump <= 0:
                        gd.input[2] = False
            elif self.jump < 19:
                self.jump = 0
        else:
            self.set_action('idle', force=not self.chomp)
            gd.input = [False, False, False]
            self.jump = 0

        if self.air_time > 5:
            if not self.hurt_timer:
                self.set_action('jump')
            if self.jump == 19:
                self.jump = 0
        else:
            self.jump = 19
            if self.await_eat:
                self.eating = self.await_eat
                self.await_eat = 0
            if gd.input[0] or gd.input[1]:
                if not self.hurt_timer:
                    self.set_action('walk')
            else:
                if not self.hurt_timer:
                    self.set_action('idle')

        self.flash = False
        if self.hurt_timer or (gd.anger > 55):
            if random.random() < 0.4:
                self.flash = True
            if self.hurt_timer:
                self.set_action('hurt')

        if self.chomp:
            self.active_animation.play(3 / 60)
            if self.active_animation.frame > 15:
                self.chomp = False

        self.air_time += 1
        collisions = self.move(self.velocity, rects)
        if collisions['top']:
            self.jump = 0
            gd.input[2] = False
        if collisions['bottom']:
            if self.velocity[1] > 2:
                self.squish_velocity = -0.15
                gd.screenshake = 8
                gd.add_animation('stomp', (self.pos[0] - 14, self.pos[1]))
                sounds['land'].play()
                damage_r = pygame.Rect(self.pos[0] - 24, self.pos[1] + 15, 68, 10)
                hit_enemy = False
                for enemy in gd.enemies:
                    if enemy.rect.colliderect(damage_r):
                        hit_enemy = True
                        enemy.dead = True
                        enemy.set_action('hurt', force=True)
                        enemy.velocity[1] = -(random.random() * 3 + 3)
                if hit_enemy:
                    sounds['hit'].play()
            self.air_time = 0
        if collisions['top'] or collisions['bottom']:
            self.velocity[1] = 1
        if collisions['left'] or collisions['right']:
            self.velocity[0] = 0

def end_screen(gd):
    state = 0
    max_state = False
    closing = False
    while True:
        display.fill((31, 14, 28))

        if closing:
            state -= 3
            if state <= 0:
                break
        else:
            if not max_state:
                state += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in [K_s, K_DOWN]:
                    closing = True
                    sounds['blip'].play()

        t1 = 'score'[:state // 4]
        font_white.render(t1, display, (display.get_width() // 2 - font_white.width(t1) // 2, display.get_height() // 2 - 60))
        t2 = str(min(gd.level, max(state - 20, 0) // 4))
        font_white.render(t2, display, (display.get_width() // 2 - font_white.width(t2) // 2, display.get_height() // 2 - 40))

        t3 = 'press down to continue'[:max(state - (20 + gd.level * 4), 0) // 4]
        if t3 == 'press down to continue':
            max_state = True

        font_white.render(t3, display, (display.get_width() // 2 - font_white.width(t3) // 2, display.get_height() // 2 + 20))

        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(65)


pygame.init()
pygame.display.set_caption('Explon\'t')

screen = pygame.display.set_mode((640, 480), 0, 32)
display = pygame.Surface((320, 240))
base_display = display.copy()
display.set_colorkey((0, 0, 0))

TILE_SIZE = 16
PARALLAX = 0.5

clock = pygame.time.Clock()

animation_manager = AnimationManager()

spritesheets, spritesheets_data = spritesheet_loader.load_spritesheets('data/images/spritesheets/')

foliage_animations = [AnimatedFoliage(load_img('data/images/foliage/' + str(i) + '.png'), [[23, 67, 75], [100, 125, 52], [192, 199, 65]], motion_scale=0.5) for i in range(3)]

load_particle_images('data/images/particles')

anger_icon_1 = load_img('data/images/anger_icon_1.png')
anger_icon_2 = load_img('data/images/anger_icon_2.png')
anger_s1 = load_img('data/images/anger_1.png')
anger_s2 = load_img('data/images/anger_2.png')
anger_bar = load_img('data/images/anger_bar.png')
anger_bar_end = load_img('data/images/anger_bar_end.png')
anger_bar_end_white = load_img('data/images/anger_bar_end_white.png')
bg_img = load_img('data/images/bg.png')
gun_img = load_img('data/images/gun.png')
lollipop_img = load_img('data/images/lollipop.png')
warp_img = load_img('data/images/warp.png')
hit_overlay_img = load_img('data/images/hit_overlay.png')
tutorial_img = load_img('data/images/tutorial.png')

cloud_images = [load_img('data/images/clouds/cloud_' + str(i + 1) + '.png') for i in range(3)]

font_white = Font('data/fonts/large_font.png', (247, 237, 186))
font_black = Font('data/fonts/large_font.png', (31, 14, 28))

sounds = {sound.split('/')[-1].split('.')[0] : pygame.mixer.Sound('data/sfx/' + sound) for sound in os.listdir('data/sfx')}
sounds['ambience'].set_volume(0.2)
sounds['crunch'].set_volume(0.7)
sounds['grass_1'].set_volume(0.06)
sounds['grass_2'].set_volume(0.06)
sounds['hit'].set_volume(0.5)
sounds['jump'].set_volume(0.3)
sounds['land'].set_volume(0.8)
sounds['shoot'].set_volume(0.3)
sounds['touch'].set_volume(0.25)
sounds['warp'].set_volume(0.4)
sounds['jump'].set_volume(0.5)
sounds['warning'].set_volume(0.3)

gd = GameData()

levels = [m.split('.')[0] for m in os.listdir('data/maps')]

def next_level():
    gd.load_map(random.choice(levels))

next_level()

global_time = 0
tutorial_x = -100

sounds['ambience'].play(-1)

pygame.mixer.music.load('data/music.ogg')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

while True:
    global_time += 1

    if random.random() < 0.001:
        random.choice([sounds['grass_1'], sounds['grass_2']]).play()

    gd.anger += 0.01
    gd.anger = max(0, gd.anger)

    gd.transition_state += gd.transition_direction * 0.023
    gd.transition_state = max(0, gd.transition_state)
    gd.transition_state = min(1, gd.transition_state)

    base_display.blit(bg_img, (0, 0))
    display.fill((0, 0, 0))

    if (not len(gd.lollipops)) and (not gd.completed_level):
        gd.completed_level = 1

    if gd.completed_level:
        gd.completed_level += 1
        if gd.completed_level > 120:
            gd.transition_direction = 1

    for cloud in gd.clouds:
        cloud[2] += cloud[1]
        base_display.blit(cloud_images[cloud[0]], (cloud[2] - gd.scroll[0] * PARALLAX, cloud[3] - gd.scroll[1] * PARALLAX))
        if cloud[2] > (gd.edges[1] + display.get_width()) * PARALLAX:
            cloud[2] = gd.edges[0] * PARALLAX - cloud_images[cloud[0]].get_width()

    gd.scroll[0] += (gd.player.center[0] - display.get_width() // 2 - gd.scroll[0]) / 20
    gd.scroll[1] += (gd.player.center[1] - display.get_height() // 2 - gd.scroll[1]) / 20

    if gd.scroll[0] < gd.edges[0]:
        gd.scroll[0] = gd.edges[0]
    if gd.scroll[0] > gd.edges[1] - display.get_width():
        gd.scroll[0] = gd.edges[1] - display.get_width()
    if gd.scroll[1] < gd.edges[2]:
        gd.scroll[1] = gd.edges[2]
    if gd.scroll[1] > gd.edges[3] - display.get_height():
        gd.scroll[1] = gd.edges[3] - display.get_height()

    for i, lollipop in list(enumerate(gd.lollipops))[::-1]:
        lollipop.update(gd)
        if lollipop.dead:
            gd.lollipops.pop(i)

    if not gd.game_over:
        gd.player.update(gd)
    if gd.player.rect.right > gd.edges[1]:
        gd.player.pos[0] = gd.edges[1] - gd.player.rect.width
    if gd.player.rect.left < gd.edges[0]:
        gd.player.pos[0] = gd.edges[0]

    for enemy in gd.enemies:
        enemy.update(gd)

    gd.grass_manager.apply_force(gd.player.center, 8, 16)

    entities_rendered = False
    render_list = gd.level_map.get_visible(gd.scroll)
    for layer in render_list:
        layer_id = layer[0]

        if not entities_rendered:
            if layer_id >= -4:
                for lollipop in gd.lollipops:
                    lollipop.render(display, gd.scroll)

                for enemy in gd.enemies:
                    enemy.render(display, gd.scroll)

                if not gd.game_over:
                    if gd.completed_level > 60:
                        if gd.completed_level == 70:
                            gd.circles.append([[gd.player.center[0], gd.player.center[1] + 6], 4, 1, 8, 0.1, 0.93, (88, 69, 99)])
                            gd.circles.append([[gd.player.center[0], gd.player.center[1] + 6], 3, 1, 4, 0.1, 0.94, (88, 69, 99)])
                            sounds['warp'].play()

                        if gd.completed_level <= 90:
                            r = (gd.completed_level - 60) / 2
                        else:
                            r = 15 - (gd.completed_level - 90) / 2
                        pygame.draw.circle(display, (31, 14, 28), (gd.player.center[0] - gd.scroll[0], gd.player.center[1] + 14 - gd.scroll[1]), int(r * 1.5))
                    gd.player.render(display, gd.scroll)

                gd.grass_manager.update_render(display, 1 / 60, offset=gd.scroll.copy(), rot_function=lambda x, y: int((math.sin(x / 100 + global_time / 40) - 0.7) * 30) / 10)

                entities_rendered = True

        for tile in layer[1]:
            if tile[1][0] == 'foliage':
                seed = int(tile[0][1] * tile[0][0] + (tile[0][0] + 10000000) ** 1.2)
                foliage_animations[tile[1][1]].render(display, (tile[0][0] - gd.scroll[0], tile[0][1] - gd.scroll[1]), m_clock=global_time / 100, seed=seed)
                chance = 0.02
                if tile[1][1] == 2:
                    chance = 0.003
                if random.random() < chance:
                    pos = foliage_animations[tile[1][1]].find_leaf_point()
                    gd.leaves.append(Particle(tile[0][0] + pos[0], tile[0][1] + pos[1], 'grass', [random.random() * 10 + 10, 8 + random.random() * 4], 0.7 + random.random() * 0.6, random.random() * 2, custom_color=random.choice([[23, 67, 75], [100, 125, 52], [192, 199, 65]])))
            else:
                offset = [0, 0]
                if tile[1][0] in spritesheets_data:
                    tile_id = str(tile[1][1]) + ';' + str(tile[1][2])
                    if tile_id in spritesheets_data[tile[1][0]]:
                        if 'tile_offset' in spritesheets_data[tile[1][0]][tile_id]:
                            offset = spritesheets_data[tile[1][0]][tile_id]['tile_offset']
                img = spritesheet_loader.get_img(spritesheets, tile[1])
                display.blit(img, (tile[0][0] - gd.scroll[0] + offset[0], tile[0][1] - gd.scroll[1] + offset[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key in [K_LEFT, K_a]:
                gd.input[0] = True
            if event.key in [K_RIGHT, K_d]:
                gd.input[1] = True
            if event.key in [K_SPACE, K_w, K_UP]:
                gd.input[2] = True
        if event.type == KEYUP:
            if event.key in [K_LEFT, K_a]:
                gd.input[0] = False
            if event.key in [K_RIGHT, K_d]:
                gd.input[1] = False
            if event.key in [K_SPACE, K_w, K_UP]:
                gd.input[2] = False

    # pos, speed, radius, width, decay, speed decay, color
    for c in gd.circles.copy():
        c[2] += c[1]
        c[1] *= c[5]
        c[3] -= c[4]
        if c[3] <= 1:
            gd.circles.remove(c)
            continue

        pygame.draw.circle(display, c[6], (int(c[0][0] - gd.scroll[0]), int(c[0][1] - gd.scroll[1])), int(c[2]), int(c[3]))

    for anim in gd.animations.copy():
        anim.update()
        if anim.dead:
            gd.animations.remove(anim)
        else:
            anim.render(display, gd.scroll)

    # pos, angle, speed
    for proj in gd.projectiles.copy():
        proj[0][0] += math.cos(proj[1]) * proj[2]
        proj[0][1] += math.sin(proj[1]) * proj[2]

        pygame.draw.line(display, (245, 237, 186), (proj[0][0] - gd.scroll[0], proj[0][1] - gd.scroll[1]), (proj[0][0] - math.cos(proj[1]) * 10 - gd.scroll[0], proj[0][1] - math.sin(proj[1]) * 10 - gd.scroll[1]), 6)
        pygame.draw.line(display, (157, 48, 59), (proj[0][0] - gd.scroll[0] - math.cos(proj[1]), proj[0][1] - gd.scroll[1] - math.sin(proj[1])), (proj[0][0] - math.cos(proj[1]) * 8 - gd.scroll[0], proj[0][1] - math.sin(proj[1]) * 8 - gd.scroll[1]), 4)

        player_dis = math.sqrt((proj[0][0] - gd.player.center[0]) ** 2 + (proj[0][1] - gd.player.center[1]) ** 2)
        if player_dis > 1000:
            gd.projectiles.remove(proj)
            continue
        elif player_dis < 20:
            if gd.player.rect.collidepoint(proj[0]) and not gd.game_over:
                for i in range(20):
                    a = proj[1] + random.random() - 0.5
                    if random.random() < 0.2:
                        a += math.pi
                    s = random.random() * 0.5 + 0.5
                    vel = [math.cos(a) * s, math.sin(a) * s]
                    gd.circle_particles.insert(random.randint(0, len(gd.circle_particles) - 1) if len(gd.circle_particles) else 0, ['fire', proj[0].copy(), [-vel[0], -vel[1]], (0, 0, 0), random.random() * 6 + 2, random.random() * 0.02 + 0.02, random.random() * 0.9])

                    if random.random() < 0.7:
                        gd.sparks.append([proj[0].copy(), a, s * 8, 2, 0.07, 0.9, 8 + random.random() * 5, 0.97])

                gd.projectiles.remove(proj)

                if (not gd.player.await_eat) and (not gd.player.eating) and (not gd.completed_level):
                    vel = [math.cos(proj[1]) * 1.5, math.sin(proj[1]) * 1.5]
                    gd.player.velocity[0] += vel[0]
                    gd.player.velocity[1] += vel[1]
                    gd.anger += 5
                    gd.player.hurt_timer = 20
                    gd.player.angry = 40
                    gd.screenshake = 14
                    sounds['hit'].play()

                continue

        if gd.level_map.tile_collide(proj[0]):
            for i in range(6):
                a = proj[1] + random.random() - 0.5
                a += math.pi
                s = (random.random() + 1) / 2
                gd.sparks.append([proj[0].copy(), a, s * 7, 2, 0.07, 0.9, 6 + random.random() * 4, 0.97])

            gd.projectiles.remove(proj)
            continue

    if (gd.anger >= 59) and (gd.game_over == 0):
        gd.screenshake = 40
        sounds['death'].play()
        for i in range(16):
            angle = random.random() * math.pi * 0.5 + math.pi * 5 / 4
            speed = random.random() * 2 + 1
            gd.circle_particles.append(['fire_base', [gd.player.center[0], gd.player.pos[1] + gd.player.rect.height], [math.cos(angle) * speed, math.sin(angle) * speed], (245, 237, 186), 2, 0.005, random.random() * 0.7])
        for i in range(30):
            gd.circle_particles.append(['fire', [gd.player.pos[0] + gd.player.rect.width * random.random(), gd.player.pos[1] + gd.player.rect.height * random.random()], [random.random() * 4 - 2, random.random() * 4 - 3], (0, 0, 0), random.random() * 24 + 2, random.random() * 0.3 + 0.3, random.random() * 0.8])
        for i in range(36):
            c = random.choice([(100, 125, 52), (192, 199, 65), (157, 48, 59), (157, 48, 59), (157, 48, 59), (157, 48, 59), (62, 33, 55), (62, 33, 55)])
            gd.circle_particles.append(['flesh', [gd.player.pos[0] + gd.player.rect.width * random.random(), gd.player.pos[1] + gd.player.rect.height * random.random()], [random.random() * 2 - 1, random.random() * 3 - 2], c, random.random() * 3.5 + 1, 0.001, 0])
        for i in range(30):
            a = random.random() * math.pi * 2
            s = random.random() + 0.5
            if random.random() < 0.2:
                s *= 3
            gd.sparks.append([gd.player.center, a, s * 5.5, 3, 0.05 + random.random() * 0.05, 0.88 + random.random() * 0.05, 10 + random.random() * 6, 0.99])
        gd.circles.append([gd.player.center, 10, 1, 10, 0.15, 0.9, (247, 237, 186)])
        gd.circles.append([gd.player.center, 7, 1, 6, 0.1, 0.87, (247, 237, 186)])
        gd.game_over = 1

    if gd.game_over:
        gd.game_over += 1
        if gd.game_over > 200:
            gd.transition_direction = 1

    if gd.game_over and gd.transition_state == 1:
        end_screen(gd)
        gd.death_reset()
        next_level()
    if gd.completed_level and gd.transition_state == 1:
        gd.level += 1
        next_level()

    # leaves
    for particle in gd.leaves.copy():
        alive = particle.update(1 / 60)
        shift = math.sin(particle.x / 20 + global_time / 40) * 16
        shift *= min(1, particle.time_alive)
        particle.draw(display, (gd.scroll[0] + shift, gd.scroll[1]))
        if not alive:
            gd.leaves.remove(particle)

    # type, pos, velocity, color, size, decay, dur
    for particle in gd.circle_particles.copy():
        if particle[0] not in ['fire_base', 'flesh']:
            particle[1][0] += particle[2][0]
            particle[1][1] += particle[2][1]
        particle[6] += particle[5]

        if particle[0] in ['fire_base', 'flesh']:
            if len(particle) == 7:
                particle.append(False)
            if not particle[7]:
                particle[1][0] += particle[2][0]
                if gd.level_map.tile_collide(particle[1]):
                    particle[1][0] -= particle[2][0]
                    particle[2][0] *= -0.7
                particle[1][1] += particle[2][1]
                if gd.level_map.tile_collide(particle[1]):
                    if 0 <= particle[2][1] < 0.1:
                        particle[7] = True
                    particle[1][1] -= particle[2][1]
                    particle[2][1] *= -0.7
                particle[2][1] += 0.1

        if particle[0] == 'fire_base':
            if particle[6] > 1:
                gd.circle_particles.remove(particle)
                continue

            particle[4] += particle[5]

            speed = math.sqrt(particle[2][1] ** 2 + particle[2][0] ** 2)
            angle = math.atan2(particle[2][1], particle[2][0])
            temp_pos = particle[1].copy()
            for j in range(int(speed // 4)):
                temp_pos[0] -= math.cos(angle) * 4
                temp_pos[1] -= math.sin(angle) * 4
                gd.circle_particles.insert(random.randint(0, len(gd.circle_particles) - 1) if len(gd.circle_particles) else 0, ['fire', temp_pos.copy(), [random.random() * 0.5 - 0.25, random.random() * 0.5 - 1], (0, 0, 0), (random.random() * 12 + 2) * (1 - particle[6]), random.random() * 0.02 + 0.02, random.random() * 0.9])
            gd.circle_particles.insert(random.randint(0, len(gd.circle_particles) - 1) if len(gd.circle_particles) else 0, ['fire', particle[1].copy(), [random.random() * 0.5 - 0.25, random.random() * 0.5 - 1], (0, 0, 0), (random.random() * 12 + 2) * (1 - particle[6]), random.random() * 0.02 + 0.02, random.random() * 0.9])

        if particle[0] == 'fire':
            if particle[6] < 0.2:
                particle[4] += particle[5]
            if particle[6] < 0.4:
                particle[3] = (245, 237, 186)
            elif particle[6] < 0.6:
                particle[3] = (228, 148, 58)
            elif particle[6] < 0.9:
                particle[3] = (157, 48, 59)
            elif particle[6] < 0.14:
                particle[3] = (62, 33, 55)
            else:
                particle[3] = (31, 14, 28)

        particle[4] -= particle[5]
        if particle[4] < 1:
            gd.circle_particles.remove(particle)
        else:
            pygame.draw.circle(display, particle[3], (particle[1][0] - gd.scroll[0], particle[1][1] - gd.scroll[1]), particle[4])

    # pos, angle, speed, width, decay, speed_decay, length, length_decay
    for spark in gd.sparks.copy():
        spark[0][0] += math.cos(spark[1]) * spark[2]
        spark[0][1] += math.sin(spark[1]) * spark[2]
        spark[3] -= spark[4]
        spark[2] *= spark[5]
        spark[6] *= spark[7]

        if spark[3] <= 0:
            gd.sparks.remove(spark)
            continue

        points = [
            (spark[0][0] + math.cos(spark[1]) * spark[6], spark[0][1] + math.sin(spark[1]) * spark[6]),
            (spark[0][0] + math.cos(spark[1] + math.pi / 2) * spark[3], spark[0][1] + math.sin(spark[1] + math.pi / 2) * spark[3]),
            (spark[0][0] - math.cos(spark[1]) * spark[6], spark[0][1] - math.sin(spark[1]) * spark[6]),
            (spark[0][0] + math.cos(spark[1] - math.pi / 2) * spark[3], spark[0][1] + math.sin(spark[1] - math.pi / 2) * spark[3]),
        ]
        points = [(p[0] - gd.scroll[0], p[1] - gd.scroll[1]) for p in points]
        pygame.draw.polygon(display, (245, 237, 186), points)

    display_mask = pygame.mask.from_surface(display)
    display_mask = display_mask.to_surface(setcolor=(31, 14, 28))
    display_mask.set_colorkey((0, 0, 0))
    base_display.blit(display_mask, (0, 3))

    # ui
    if gd.tutorial == 2:
        display.blit(tutorial_img, (gd.player.center[0] - 20 - gd.scroll[0], gd.player.pos[1] - gd.scroll[1] - 32 + (global_time % 60 // 40)))

    if (gd.player.hurt_timer or gd.anger > 55) and (not gd.game_over):
        if random.random() < 0.3:
            display.blit(hit_overlay_img, (0, 0))

    if gd.anger > 45:
        gd.player.angry = 40

    if gd.game_over:
        gd.anger = 59

    if (gd.player.angry > 0) and not gd.game_over:
        if gd.player.flip[0]:
            display.blit([anger_s2, anger_s1][(global_time % 60) // 40], (gd.player.center[0] + 4 - gd.scroll[0], gd.player.pos[1] - gd.scroll[1]))
        else:
            display.blit([anger_s2, anger_s1][(global_time % 60) // 40], (gd.player.center[0] - 12 - gd.scroll[0], gd.player.pos[1] - gd.scroll[1]))

    gd.anger = min(gd.anger, 59)
    bar_end = anger_bar_end
    if gd.anger < 58:
        anger_r = pygame.Rect(24, 7, 58 - int(gd.anger), 8)
        c = (157, 48, 59)
        if gd.anger > 50:
            if global_time % 30 == 0:
                sounds['warning'].play()
            if random.random() < 0.3:
                c = (245, 237, 186)
                bar_end = anger_bar_end_white
        pygame.draw.rect(display, c, anger_r)

    if gd.anger < 59:
        display.blit(bar_end, (25 + 57 - int(gd.anger), 7))
    display.blit(anger_bar, (20, 5))
    display.blit([anger_icon_2, anger_icon_1][(global_time % 60) // 50], (5, 3))

    display.blit(lollipop_img, (7, 22))
    l_pos = (23, 25)
    font_black.render(str(gd.init_lollipops - len(gd.lollipops)) + ' / ' + str(gd.init_lollipops), display, (l_pos[0] - 1, l_pos[1]))
    font_black.render(str(gd.init_lollipops - len(gd.lollipops)) + ' / ' + str(gd.init_lollipops), display, (l_pos[0] + 1, l_pos[1]))
    font_black.render(str(gd.init_lollipops - len(gd.lollipops)) + ' / ' + str(gd.init_lollipops), display, (l_pos[0], l_pos[1] + 1))
    font_black.render(str(gd.init_lollipops - len(gd.lollipops)) + ' / ' + str(gd.init_lollipops), display, (l_pos[0], l_pos[1] - 1))
    font_white.render(str(gd.init_lollipops - len(gd.lollipops)) + ' / ' + str(gd.init_lollipops), display, l_pos)

    display.blit(warp_img, (6, 46))
    l_pos = (23, 45)
    font_black.render(str(gd.level), display, (l_pos[0] - 1, l_pos[1]))
    font_black.render(str(gd.level), display, (l_pos[0] + 1, l_pos[1]))
    font_black.render(str(gd.level), display, (l_pos[0], l_pos[1] + 1))
    font_black.render(str(gd.level), display, (l_pos[0], l_pos[1] - 1))
    font_white.render(str(gd.level), display, l_pos)

    if gd.level_notice:
        gd.level_notice -= 0.01
        gd.level_notice = max(0, gd.level_notice)
        text = 'level ' + str(gd.level)
        w = font_white.width(text)
        if gd.level_notice > 0.8:
            l_pos = (display.get_width() // 2 - w // 2, display.get_height() // 2 - 16 - display.get_height() // 2 * (gd.level_notice - 0.8) * 5)
        elif gd.level_notice < 0.2:
            l_pos = (display.get_width() // 2 - w // 2, display.get_height() // 2 - 16 + (display.get_height() // 2 + 20) * (0.2 - gd.level_notice) * 5)
        else:
            l_pos = (display.get_width() // 2 - w // 2, display.get_height() // 2 - 16)
        font_black.render(text, display, (l_pos[0] - 1, l_pos[1]))
        font_black.render(text, display, (l_pos[0] + 1, l_pos[1]))
        font_black.render(text, display, (l_pos[0], l_pos[1] + 1))
        font_black.render(text, display, (l_pos[0], l_pos[1] + 2))
        font_black.render(text, display, (l_pos[0], l_pos[1] + 3))
        font_black.render(text, display, (l_pos[0], l_pos[1] - 1))
        font_white.render(text, display, l_pos)
    elif (gd.tutorial == 1) or (tutorial_x < display.get_width() + 100):
        if gd.tutorial == 1:
            tutorial_x += (display.get_width() // 2 - 12 - tutorial_x) / 20
        elif gd.tutorial == 0:
            tutorial_x += (display.get_width() + 150 - tutorial_x) / 20
        l_pos = (tutorial_x, display.get_height() // 4 - 8 + (global_time % 60) // 40)
        display.blit(lollipop_img, (tutorial_x - 20, l_pos[1]))
        font_black.render('collect', display, (l_pos[0] - 1, l_pos[1]))
        font_black.render('collect', display, (l_pos[0] + 1, l_pos[1]))
        font_black.render('collect', display, (l_pos[0], l_pos[1] + 1))
        font_black.render('collect', display, (l_pos[0], l_pos[1] - 1))
        font_white.render('collect', display, l_pos)


    if gd.transition_state:
        transition_surf = display.copy()
        transition_surf.fill((31, 14, 28))
        transition_surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(transition_surf, (0, 0, 0), (transition_surf.get_width() // 2, transition_surf.get_height() // 2), int(math.sqrt(2) * transition_surf.get_width() * (1 -gd.transition_state)))
        display.blit(transition_surf, (0, 0))

    screenshake_offset = [0, 0]
    if gd.screenshake:
        gd.screenshake -= 1
        screenshake_offset = [random.random() * 6 - 3, random.random() * 6 - 3]

    base_display.blit(display, screenshake_offset)

    screen.blit(pygame.transform.scale(base_display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(65)
