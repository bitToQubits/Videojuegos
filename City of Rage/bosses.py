import pygame,sys,random
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
PURPLE=pygame.color.THECOLORS["purple"]
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
CENTER_X= int(320/2)


def load_sprite_data(sprite_file):
    sprites = {'rect':[], 'axis_shift':[], 'offense_box':[], 'defense_box':[]}
    with open(sprite_file, 'r') as file:
         data=file.read()
         data=data.split(';')
         del(data[-1])
         for i in range(len(data)):
             data[i] = data[i].split(",")
             for j in range(len(data[i])):
                 data[i][j] = data[i][j].split(" ")
                 for k in range(len(data[i][j])):
                     data[i][j][k] = int(data[i][j][k])
             sprites['rect'].append(data[i][0])
             sprites['axis_shift'].append(data[i][1])
             sprites['offense_box'].append(data[i][2])
             sprites['defense_box'].append(data[i][3])
    return sprites

def load_animation_data(animation_file):
    animations = None
    with open(animation_file, 'r') as file:
         data=file.read()
         data=data.split(',')
         del(data[-1])
         for i in range(len(data)):
             data[i] = data[i].split(" ")
             if data[i][0] == "-1":
                del(data[i][0])
             else:
                data[i].append(-1)
             for j in range(len(data[i])):
                 data[i][j] = int(data[i][j])
         animations = data
    return animations

def load_data():
    image = pygame.image.load('data\\Genesis 32X SCD - Streets of Rage 2 - Big-Ben.png').convert()
    Big_Ben.get_sprites(image)
    Big_Ben.get_animations()
    Big_Ben.health_bar = Big_Ben.make_health_bar()
    

class Boss():
    def __init__(self, axis_pos, z_pos, groups):
        for group in groups:
            group.append(self)
        self.groups = groups       
        self.axis_pos = axis_pos
        self.current_animation =  self.animations['stand']
        self.animation_frame = 0
        self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        self.image_pos=[
        self.axis_pos[0] + self.current_sprite['axis_shift'][0],
        self.axis_pos[1] + self.current_sprite['axis_shift'][1]]
        self.anim_time = 0
        self.max_anim_time = 2
        self.walk_speed = 2
        self.xvel = self.walk_speed
        self.yvel = 0
        self.zvel = 0
        self.z_pos = z_pos
        self.direction = 1
        self.hit_points = 1
        self.attack_type = None
        self.hit_connect = False
        self.move_time = 0
        self.hit_freeze_time = 0
        self.current_state = 'idle'
        self.states = {'stand':self.stand, 'walk':self.walk, 'hurt':self.hurt, 'death':self.death}
        
    def get_sprites(image, sprite_file):
        sprites = []
        sprites_data = load_sprite_data(sprite_file)
        for i in range(len(sprites_data['rect'])):
            sprites.append({'image':image.subsurface(sprites_data['rect'][i]),
                            'axis_shift':sprites_data['axis_shift'][i],
                            'offense_box':sprites_data['offense_box'][i],
                            'defense_box':sprites_data['defense_box'][i]})
        return sprites
                            
    def get_animations(animation_file):
        animations = {}            
        animations_data = load_animation_data(animation_file)
        animations['idle'] = animations_data[14]
        animations['walk'] = animations_data[2]
        return animations
                            
    def get_left_side_sprites(sprites):
        left_side_sprites=[]
        for sprite in sprites:
            image_width, image_height = sprite['image'].get_size()             
            left_side_sprite={
            'image':pygame.transform.flip(sprite['image'], True, False),    
            'axis_shift':[-(image_width + sprite['axis_shift'][0]), sprite['axis_shift'][1]],
            'offense_box':sprite['offense_box'],
            'defense_box':sprite['defense_box']}
            if sprite['offense_box'] != [0,0,0,0]:
               offense_box = sprite['offense_box']
               left_side_offense_box = [image_width - (offense_box[0] + offense_box[2]),
                                        offense_box[1], offense_box[2], offense_box[3]]
               left_side_sprite['offense_box'] = left_side_offense_box
            if sprite['defense_box'] != [0,0,0,0]:
               defense_box = sprite['defense_box']
               left_side_defense_box = [image_width - (defense_box[0] + defense_box[2]),
                                        defense_box[1], defense_box[2], defense_box[3]]
               left_side_sprite['defense_box'] = left_side_defense_box
            left_side_sprites.append(left_side_sprite)            
        return left_side_sprites

    def update_animation(self):
        self.anim_time += 1
        if self.anim_time  >= self.max_anim_time:
           self.anim_time = 0
           self.animation_frame += 1
           if self.current_animation[self.animation_frame] == -1:
              self.animation_frame = 0
           self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
           self.image = self.current_sprite['image']
           
    def change_animation(self, animation):
        self.current_animation =  self.animations[animation]
        self.anim_time = 0
        self.animation_frame = 0
        self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        
    def end_of_animation(self):
        return self.animation_frame == 0 and self.anim_time == 0
                        
    def stand(self):
        pass
                         
    def hurt(self):
        self.update_animation()
        if self.end_of_animation():
           self.attack_type = None
           self.hit_connect = False
           self.current_state = 'stand'
           self.change_animation('stand')
                      
    def knocked_up(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= 1        
        self.update_animation()
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.axis_pos[1] = 0
           #self.xvel = 3 
           self.yvel = 6
           self.current_state = 'knocked_down'
           self.change_animation('knocked_down')
           
    def knocked_down(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= 1             
        self.update_animation()
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.axis_pos[1] = 0
           #self.xvel = 3
           self.yvel = 0
           if self.health <= 0:
              self.current_state = 'death'
              self.change_animation('death')
           else:  
              self.current_state = 'hurt'
              self.change_animation('get_up')
           
    def grabbed(self):
        self.update_animation()
        if self.end_of_animation():
           self.change_animation('grabbed')
           
    def throwed(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= 1
        if self.current_animation[self.animation_frame + 1] != -1:
           self.update_animation()
           if self.anim_time == 0:
              self.image = pygame.transform.flip(self.image, True, True)           
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.health -= 20
           self.opponent.enemy_draw_health_bar = self.draw_health_bar
           self.opponent.enemy_health_bar_timer = 80
           self.axis_pos[1] = 0
           self.xvel = 3 * self.direction
           self.yvel = 6
           self.current_state = 'knocked_down'
           self.change_animation('knocked_down')
        
    def death(self):
        self.update_animation()
        if self.end_of_animation():
           self.kill()
        
    def kill(self):
        for group in self.groups:
            group.remove(self)
            
    def draw_health_bar(self, surface):            
        surface.blit(self.health_bar, (5, 25))
        if self.health > 0:
           pygame.draw.rect(surface, YELLOW, [20, 36, self.health, 6])
        
    def draw(self, surface):
        self.image_pos[0] = self.axis_pos[0] + self.current_sprite['axis_shift'][0]
        self.image_pos[1] = self.axis_pos[1] + self.current_sprite['axis_shift'][1] + self.z_pos        
        surface.blit(self.image, self.image_pos)        
        
            
class Big_Ben(Boss):
    def __init__(self, axis_pos, z_pos, direction, opponent, groups=[]):
        self.left_side_sprites = Big_Ben.left_side_sprites
        self.right_side_sprites = Big_Ben.right_side_sprites
        self.sprites = self.left_side_sprites
        self.animations = Big_Ben.animations
        self.opponent = opponent
        Boss.__init__(self, axis_pos, z_pos, groups=groups)
        self.states = {'stand':self.stand, 'walk':self.walk, 'attack':self.attack,
                       'grabbed':self.grabbed, 'hurt':self.hurt, 'throwed':self.throwed,
                       'hunt_opponent':self.hunt_opponent, 'prepare_flame_attack': self.prepare_flame_attack,
                       'jump_start':self.jump_start, 'jump':self.jump, 'flame_attack':self.flame_attack,
                       'knocked_up':self.knocked_up, 'knocked_down':self.knocked_down, 'death':self.death}
        self.hit_reactions = {'normal':'hurt', 'strong':'knocked_up'}
        self.direction = direction
        self.flames = [Flame(self) for i in range(6)]
        self.flames_length = len(self.flames) - 1
        self.flames_index = 0
        self.timer = 0
        self.health = 120
        self.health_bar = Big_Ben.health_bar
        self.health_bar_timer = 0
        if self.direction == 1:
           self.xvel = self.walk_speed 
           self.sprites = self.left_side_sprites
        if self.direction == -1:
           self.xvel = -self.walk_speed
           self.sprites = self.right_side_sprites        
        self.current_state = 'stand'
        self.change_animation('laugh')
        
    def get_sprites(image):
        sprite_file = "data\\Big-Ben.spr"
        Big_Ben.right_side_sprites = Boss.get_sprites(image, sprite_file)
        Big_Ben.left_side_sprites = Boss.get_left_side_sprites(Big_Ben.right_side_sprites)

    def get_animations():
        animation_file = "data\\Big-Ben.anm"
        animations = {}            
        animations_data = load_animation_data(animation_file)
        animations['stand'] = animations_data[0]
        animations['walk'] = animations_data[1]
        animations['attack'] = animations_data[2]
        animations['hurt'] = animations_data[3]
        animations['grabbed_hurt'] = animations_data[4]
        animations['knocked_up'] = animations_data[5]
        animations['knocked_down'] = animations_data[6]
        animations['get_up'] = animations_data[7]
        animations['grabbed'] = animations_data[8]
        animations['throwed1'] = animations_data[9]
        animations['throwed2'] = animations_data[10]
        animations['jump_start'] = animations_data[11]
        animations['jump'] = animations_data[14]
        animations['air_attack'] = animations_data[13]
        animations['chain_attack'] = animations_data[15]
        animations['flame'] = animations_data[12]
        animations['flame_attack'] = animations_data[16]
        animations['prepare_flame_attack'] = animations_data[17]
        animations['laugh'] = animations_data[18]
        animations['death'] = animations_data[19]
        Big_Ben.animations = animations
        
    def make_health_bar():
        surface1 = pygame.Surface([136, 18]).convert()
        surface1.set_colorkey(BLACK)       
        surface2 = pygame.Surface([122, 8]).convert()
        surface2.fill(RED)
        rect = [0, 0, 122, 8]
        pygame.draw.rect(surface2, WHITE, rect, 1)
        surface1.blit(surface2, (14, 10))
        image = Big_Ben.right_side_sprites[-1]['image'].copy()
        pygame.draw.rect(image, BLUE, image.get_rect(), 1)
        surface3 = pygame.Surface(image.get_size()).convert()
        surface3.fill((1, 1, 1))
        surface3.blit(image, (0, 0))        
        surface1.blit(surface3, (0, 3))
        font = pygame.font.SysFont('Arial', 11, bold = True)
        name = font.render("Big-Ben", True, WHITE)
        surface1.blit(name, (22, -2))
        return surface1
        
    def stand(self):
        self.update_animation()
        x_distance = self.axis_pos[0] - self.opponent.axis_pos[0]
        z_distance = self.z_pos - self.opponent.z_pos
        if x_distance > 0:
           self.sprites = self.right_side_sprites
           self.direction = -1
        else:
           self.sprites = self.left_side_sprites
           self.direction = 1
        if random.randint(1, 3) == 3:
           if abs(z_distance) < 9:
              if abs(x_distance) < 60:
                 self.current_state = 'attack'
                 animation = random.choice(('attack', 'chain_attack'))
                 if animation == 'attack':
                    self.attack_type = "strong"
                 else:
                    self.attack_type = "normal"
                 self.change_animation(animation)
              else:   
                 self.xvel = 4 * self.direction
                 self.yvel = 10
                 self.current_state = 'jump_start'
                 self.change_animation('jump_start')
        elif random.randint(1, 10) == 10:   
           self.current_state = 'prepare_flame_attack'
           self.change_animation('prepare_flame_attack')
        self.move_time -= 1
        if self.move_time <= 1:
           if abs(x_distance) > 60 or abs(z_distance) > 10:
              self.current_state = random.choice(('walk', 'hunt_opponent'))
              self.change_animation('walk')
              self.move_time = random.randint(10, 50)
              if x_distance < 0:
                 self.xvel = self.walk_speed
              else:
                 self.xvel = -self.walk_speed         
           elif random.randint(1, 5) == 5:
              self.current_state = 'attack'
              animation = random.choice(('attack', 'chain_attack'))
              if animation == 'attack':
                 self.attack_type = "strong"
              else:
                 self.attack_type = "normal"
              self.change_animation(animation)
        
    def walk(self):
        self.update_animation()
        x_distance = self.axis_pos[0] - self.opponent.axis_pos[0]
        z_distance = self.z_pos - self.opponent.z_pos
        self.axis_pos[0] += self.xvel
        self.z_pos += self.zvel
        if self.z_pos < 160 or self.z_pos > 230:
           self.z_pos -= self.zvel        
        if x_distance > 0:
           self.sprites = self.right_side_sprites
        else:
           self.sprites = self.left_side_sprites
        if abs(z_distance) < 9:
           if random.randint(1, 5) == 5:
              self.xvel = 4 * self.direction
              self.yvel = 10
              self.current_state = 'jump_start'
              self.change_animation('jump_start')
        self.move_time -= 1
        if self.move_time <= 1:
           if random.randint(1, 3) == 3:
              self.current_state = 'stand'
              self.change_animation('laugh')
              self.move_time = random.randint(10, 50)
           elif random.randint(1, 5) == 5:
              self.current_state = 'hunt_opponent'
              self.change_animation('walk')
              self.move_time = random.randint(10, 100)
           else:
              if 60 > abs(x_distance) > 40:
                 self.xvel = random.choice((0, self.walk_speed, -self.walk_speed))
              else:
                 if x_distance < 0:
                    self.xvel = self.walk_speed
                 else:
                    self.xvel = -self.walk_speed
              self.zvel = random.choice((0, self.walk_speed, -self.walk_speed))
              self.move_time = random.randint(10, 50)
        if 30 < abs(x_distance) < 60 and  abs(z_distance) <= 10:
           if random.randint(1, 5) == 5:
              self.current_state = 'attack'
              animation = random.choice(('attack', 'chain_attack'))
              if animation == 'attack':
                 self.attack_type = "strong"
              else:
                 self.attack_type = "normal"
              self.change_animation(animation)
              
    def attack(self):
        self.update_animation()
        if self.current_animation == self.animations['chain_attack']:
           if self.animation_frame == 4:
              self.hit_connect = False
           elif self.animation_frame == 8:
              self.hit_connect = False
              self.attack_type = "strong"
        if self.end_of_animation():
           if abs(self.axis_pos[0] - self.opponent.axis_pos[0]) > 0:
              self.xvel = self.walk_speed
           else:
              self.xvel = -self.walk_speed
           self.attack_type = None
           self.hit_connect = False
           self.current_state = 'walk'
           self.change_animation('walk')
           self.move_time = random.randint(10, 50)
           
    def hunt_opponent(self):
        self.update_animation()       
        x_distance = self.axis_pos[0] - self.opponent.axis_pos[0]
        z_distance = self.z_pos - self.opponent.z_pos
        self.move_time -= 1
        if self.move_time <= 1:
           if random.randint(1, 3) == 3:
              self.current_state = 'stand'
              self.change_animation('laugh')
              self.move_time = random.randint(10, 50)
           elif random.randint(1, 5) == 5:
              self.current_state = 'walk'
              self.change_animation('walk')
              self.move_time = random.randint(10, 50)
        if x_distance > 0:
           self.sprites = self.right_side_sprites
        else:
           self.sprites = self.left_side_sprites
        if abs(x_distance) > 40:
           if x_distance < 0:
              self.axis_pos[0] += self.walk_speed
           else:
              self.axis_pos[0] -= self.walk_speed
        if abs(z_distance) > 1:      
           if z_distance < 0:
              self.z_pos += self.walk_speed
           else:
              self.z_pos -= self.walk_speed
        if abs(x_distance) < 60 and abs(z_distance) <= 1:
           if random.randint(1, 5) == 5:
              self.current_state = 'attack'
              animation = random.choice(('attack', 'chain_attack'))
              if animation == 'attack':
                 self.attack_type = "strong"
              else:
                 self.attack_type = "normal"
              self.change_animation(animation)
        
    def jump_start(self):
        self.update_animation()
        if self.end_of_animation():
           if self.yvel > 0:
              self.current_state = 'jump'
              self.change_animation('jump')
           else:
              self.current_state = 'stand'
              self.change_animation('stand')
              
    def jump(self):
        global punch
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= 1
        self.update_animation()
        if abs(self.axis_pos[0] - self.opponent.axis_pos[0]) < 60 \
        and abs(self.z_pos - self.opponent.z_pos) < 9:
           self.attack_type = "normal"
           self.change_animation('air_attack')
        if self.axis_pos[1] + self.z_pos >= self.z_pos:
           self.axis_pos[1] = 0
           self.xvel = 0
           self.yvel = 0
           self.current_state = 'jump_start'
           self.change_animation('jump_start')
           self.hit_connect = False
           self.attack_type = None
           
    def prepare_flame_attack(self):
        self.update_animation()
        x_distance = self.axis_pos[0] - self.opponent.axis_pos[0]
        z_distance = self.z_pos - self.opponent.z_pos
        if x_distance > 0:
           self.sprites = self.right_side_sprites
           self.direction = -1
        else:
           self.sprites = self.left_side_sprites
           self.direction = 1
        if self.end_of_animation():
           self.attack_type = "strong"
           self.current_state = 'flame_attack'
           self.change_animation('flame_attack')
           #self.attack_type = None
           self.flames_index = 0
           self.timer = 0
           for flame in self.flames:
               flame.active = False
               flame.anim_time = 0
               flame.animation_frame = 0
               flame.current_sprite = flame.owner.sprites[self.current_animation[flame.animation_frame]]
               flame.image = flame.current_sprite['image']
           self.flames[0].reset()
           self.flames[0].active = True
           self.flames[0].xvel = 4 * self.direction
           self.xvel = 5 * self.direction
           if abs(z_distance) > 9:
              if z_distance > 0:
                 self.zvel = -3
              else:
                 self.zvel = 3
           else:
              self.zvel = 0
           self.move_time = 50
        
    def flame_attack(self):
        self.update_animation()
        self.axis_pos[0] += self.xvel
        self.z_pos += self.zvel
        if self.z_pos < 160 or self.z_pos > 230:
           self.z_pos -= self.zvel
           for flame in self.flames:
               if flame.active:
                  flame.axis_pos[1] -= self.zvel           
        for flame in self.flames:
            if flame.active:
               flame.axis_pos[0] += self.xvel
               flame.axis_pos[1] += self.zvel
               flame.update()
        self.move_time -= 1
        if self.move_time <= 1:
           self.attack_type = None
           self.hit_connect = False
           self.current_state = 'stand'
           self.change_animation('stand')
        if self.flames_index < self.flames_length:
           self.timer += 1
           if self.timer > 3:
              self.timer = 0
              self.flames_index += 1
              flame = self.flames[self.flames_index]
              if not flame.active:
                 flame.active = True
                 flame.reset()
              #if self.flames_index == self.flames_length:
                 #self.attack_type = "strong"
                  
    def draw(self, surface):
        self.image_pos[0] = self.axis_pos[0] + self.current_sprite['axis_shift'][0]
        self.image_pos[1] = self.axis_pos[1] + self.current_sprite['axis_shift'][1] + self.z_pos        
        surface.blit(self.image, self.image_pos)
        if self.current_state == 'flame_attack':
           for flame in self.flames:
               if flame.active:
                  flame.draw(surface)


class Flame():
    def __init__(self, owner):
        self.owner = owner
        self.axis_pos = [0, 0]
        self.current_animation =  owner.animations['flame']
        self.animation_frame = 0
        self.current_sprite = self.owner.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        self.image_pos=[
        self.axis_pos[0] + self.current_sprite['axis_shift'][0],
        self.axis_pos[1] + self.current_sprite['axis_shift'][1]]
        self.anim_time = 0
        self.max_anim_time = 2
        self.xvel = 0
        self.active = False
        
    def update(self):
        self.axis_pos[0] += self.xvel
        self.update_animation()
        if self.end_of_animation():
           self.reset()
           
    def update_animation(self):
        self.anim_time += 1
        if self.anim_time  >= self.max_anim_time:
           self.anim_time = 0
           self.animation_frame += 1
           if self.current_animation[self.animation_frame] == -1:
              self.animation_frame = 0
           self.current_sprite = self.owner.sprites[self.current_animation[self.animation_frame]]
           self.image = self.current_sprite['image']

    def end_of_animation(self):
        return self.animation_frame == 0 and self.anim_time == 0
      
    def reset(self):
        self.animation_frame = 0
        self.current_sprite = self.owner.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        self.xvel = 4 * self.owner.direction
        self.axis_pos[0] = self.owner.axis_pos[0] + (20 * self.owner.direction)
        self.axis_pos[1] = (self.owner.axis_pos[1] + self.owner.z_pos) - 58

    def draw(self, surface):           
        self.image_pos[0] = self.axis_pos[0] + self.current_sprite['axis_shift'][0]
        self.image_pos[1] = self.axis_pos[1] + self.current_sprite['axis_shift'][1]
        surface.blit(self.image, self.image_pos)

