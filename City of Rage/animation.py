import pygame,sys,random
from pygame.locals import *


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


class Animation():
    def __init__(self, image, sprite_file, animation_file, axis_pos, scale=None):
        if scale:
           self.right_side_sprites = self.get_scaled_sprites(image, sprite_file, scale)
        else:
           self.right_side_sprites = self.get_sprites(image, sprite_file)
        self.left_side_sprites = self.get_left_side_sprites(self.right_side_sprites)
        self.sprites = self.right_side_sprites
        self.animations = self.get_animations(animation_file)
        self.axis_pos = axis_pos
        self.current_animation =  self.animations[0]
        self.animation_frame = 0
        self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        self.image_pos=[
        self.axis_pos[0] + self.current_sprite['axis_shift'][0],
        self.axis_pos[1] + self.current_sprite['axis_shift'][1]]
        self.anim_time = 0
        self.max_anim_time = 2
        self.active = False
        self.hit_freeze_time = 0
        
    def get_sprites(self, image, sprite_file):
        sprites = []
        sprites_data = load_sprite_data(sprite_file)
        for i in range(len(sprites_data['rect'])):
            sprites.append({'image':image.subsurface(sprites_data['rect'][i]),
                            'axis_shift':sprites_data['axis_shift'][i],
                            'offense_box':sprites_data['offense_box'][i],
                            'defense_box':sprites_data['defense_box'][i]})
        return sprites
    
    def get_animations(self, animation_file):
        animations = {}            
        animations_data = load_animation_data(animation_file)
        for i in range(len(animations_data)):
            animations[i] = animations_data[i]
        return animations
    
    def get_left_side_sprites(self, sprites):
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
    
    def update(self):
        self.update_animation()
        if self.end_of_animation():
           self.active = False
           
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
    
    def get_scaled_sprites(self, image, sprite_file, scale):
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        image = pygame.transform.scale(image, (width, height))    
        sprites = []
        sprites_data = load_sprite_data(sprite_file)
        for i in range(len(sprites_data['rect'])):
            rect = sprites_data['rect'][i]
            rect[0] = int(rect[0] * scale)
            rect[1] = int(rect[1] * scale)
            rect[2] = int(rect[2] * scale)
            rect[3] = int(rect[3] * scale)
            axis_shift = sprites_data['axis_shift'][i]
            axis_shift[0] = int(axis_shift[0] * scale)
            axis_shift[1] = int(axis_shift[1] * scale)
            offense_box = sprites_data['offense_box'][i]
            offense_box[0] = int(offense_box[0] * scale)
            offense_box[1] = int(offense_box[1] * scale)
            offense_box[2] = int(offense_box[2] * scale)
            offense_box[3] = int(offense_box[3] * scale)
            defense_box = sprites_data['defense_box'][i]
            defense_box[0] = int(defense_box[0] * scale)
            defense_box[1] = int(defense_box[1] * scale)
            defense_box[2] = int(defense_box[2] * scale)
            defense_box[3] = int(defense_box[3] * scale)
            sprites.append({'image':image.subsurface(rect),
                            'axis_shift':axis_shift,
                            'offense_box':offense_box,
                            'defense_box':defense_box})
        return sprites
    
    def draw(self, surface):           
        self.image_pos[0] = self.axis_pos[0] + self.current_sprite['axis_shift'][0]
        self.image_pos[1] = self.axis_pos[1] + self.current_sprite['axis_shift'][1]
        surface.blit(self.image, self.image_pos)
        #print(self.sprites.index(self.current_sprite))
        #offense_box = self.current_sprite['offense_box']
        #offense_box = [self.image_pos[0] + offense_box[0],
                      #self.image_pos[1] + offense_box[1],
                      #offense_box[2], offense_box[3]]
        #pygame.draw.rect(surface, RED, offense_box, 2)

