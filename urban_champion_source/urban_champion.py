import pygame,sys,random
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
NES_RESOLUTION = (256, 240)
SCALE = 3
SCREEN_WIDTH = NES_RESOLUTION[0] * SCALE
SCREEN_HEIGHT = NES_RESOLUTION[1] * SCALE
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
CENTER_X= int(NES_RESOLUTION[0]/2)
TITLE_SCREEN = 0
P1_VS_COM = 1
P1_VS_P2 = 2
COM_VS_COM = 3


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

def pause(surface, uc_font):
    #pygame.mixer.music.pause()
    uc_font.font = uc_font.gray_font
    uc_font.size = uc_font.normal_size
    text = uc_font.render(" pause ")
    scaled_size = [text.get_width()*SCALE, text.get_height()*SCALE]
    text = pygame.transform.scale(text, scaled_size)
    text_pos = [int(SCREEN_WIDTH/2) - int(text.get_width()/2), 430]
    surface.blit(text, text_pos)
    pygame.display.flip()
    while True:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  global game_mode 
                  game_mode = TITLE_SCREEN
                  return
               elif event.key == K_p:
                  #pygame.mixer.music.unpause() 
                  return
                
def title_screen(image, screen, display_surface, uc_font):
    modes = [P1_VS_COM, P1_VS_P2, COM_VS_COM]
    modes_index = 0
    selected_mode = modes[modes_index]
    cursor = image.subsurface([284, 369, 8, 6])
    cursor_pos = [28, 151]
    title1 = image.subsurface([0, 0, 256, 142])
    title2 = image.subsurface([256, 360, 256, 96])
    black_surface = pygame.Surface([8, 6]).convert()
    uc_font.font = uc_font.white_font
    uc_font.size = uc_font.normal_size
    text1 = uc_font.render(" by raytomely ")
    text1_pos = [int(256/2) - int(text1.get_width()/2) + 4, 198]
    uc_font.font = uc_font.pink_font
    text2 = uc_font.render("game c    com vs com")
    text2_pos = [44, 182]
    while True:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
                  
               if event.key == K_UP:
                  modes_index -= 1
                  cursor_pos[1] -= 16
                  if modes_index < 0:
                     modes_index = len(modes)-1
                     cursor_pos[1] = 151 + 32
                  selected_mode = modes[modes_index]   
               elif event.key == K_DOWN:
                  modes_index += 1
                  cursor_pos[1] += 16
                  if modes_index > len(modes)-1:
                     modes_index = 0
                     cursor_pos[1] = 151
                  selected_mode = modes[modes_index]
               elif event.key == K_RETURN:
                  return selected_mode
                
        display_surface.blit(title1, (0, 0))
        display_surface.blit(title2, (0, 142))
        display_surface.blit(text1, text1_pos)
        display_surface.blit(text2, text2_pos)
        display_surface.blit(text2, text2_pos)
        display_surface.blit(black_surface, (28, 151))
        display_surface.blit(cursor, cursor_pos)
        scaled_display_surface = pygame.transform.scale(display_surface, SCREEN_SIZE)
        screen.blit(scaled_display_surface, (0, 0))
        pygame.display.flip()

def load_sounds():
    path = "data\\sounds\\"
    sounds = {}
    sounds['attack'] = pygame.mixer.Sound(path+'wp_alwa.wav')
    sounds['player_hit'] = pygame.mixer.Sound(path+'hit1.wav')
    sounds['enemy_hit'] = pygame.mixer.Sound(path+'001.wav')
    sounds['knocked_down'] = pygame.mixer.Sound(path+'BodyFall_001.wav')
    sounds['player_die'] = pygame.mixer.Sound(path+'argh1.wav')
    sounds['enemy_die'] = pygame.mixer.Sound(path+'Groan_007a.wav')
    sounds['special_move1'] = pygame.mixer.Sound(path+'045.wav')
    sounds['special_move2'] = pygame.mixer.Sound(path+'moveF10.wav')
    sounds['done'] = pygame.mixer.Sound(path+'done.wav')
    sounds['player_die'].set_volume(0.3)
    sounds['special_move1'].set_volume(0.3)
    sounds['special_move2'].set_volume(0.3)
    return sounds

def collisions(player, opponent):
    if player.attack_type != None and not player.hit_connect:
       if opponent.current_state not in ('death') \
       and player.current_sprite['offense_box']!= [0, 0, 0, 0] \
       and opponent.current_sprite['defense_box']!= [0, 0, 0, 0]:
          offense_box = player.current_sprite['offense_box']
          offense_box = [player.image_pos[0] + offense_box[0],
                         player.image_pos[1] + offense_box[1],
                         offense_box[2], offense_box[3]]
          defense_box = opponent.current_sprite['defense_box']
          defense_box = [opponent.image_pos[0] + defense_box[0],
                         opponent.image_pos[1] + defense_box[1],
                         defense_box[2], defense_box[3]]        
          if offense_box[0] < defense_box[0] + defense_box[2] \
          and offense_box[0] + offense_box[2] > defense_box[0] \
          and offense_box[1] < defense_box[1] + defense_box[3] \
          and offense_box[1] + offense_box[3] > defense_box[1]:
              if opponent.stamina <= 0:
                 player.attack_type = "strong"              
              if player.stamina <= 0:
                 player.attack_type = "normal"
              if opponent.current_state == 'dizzy':
                 opponent.look_at_direction() 
              if opponent.out_of_boundary(opponent.axis_pos[0] + (10 * -opponent.direction)):
                 player.attack_type = "strong"
              if player.attack_type == "normal":
                 opponent.stamina -= 4
                 if opponent.stamina < 0:
                    opponent.stamina = 0                 
                 opponent.xvel = 10 * -opponent.direction
                 opponent.current_state = 'hurt'
                 opponent.fight_distance = False
                 player.fight_distance = False
                 if player.fight_stance == 'high':
                    opponent.current_animation =  opponent.animations['hurt1']
                 elif player.fight_stance == 'low':
                    opponent.current_animation =  opponent.animations['hurt2']
                 player.fight_distance = False
              elif player.attack_type == "strong":
                 opponent.stamina -= 10
                 if opponent.stamina < 0:
                    opponent.stamina = 0
                 opponent.xvel = 1.22 * -opponent.direction
                 opponent.yvel = 3
                 opponent.current_state = 'knocked_up'
                 if player.fight_stance == 'high':
                    opponent.current_animation =  opponent.animations['knocked_up1']
                 elif player.fight_stance == 'low':
                    opponent.current_animation =  opponent.animations['knocked_up2'] 
              opponent.anim_time = opponent.max_anim_time
              opponent.animation_frame = 0
              opponent.hit_freeze_time = 5
              player.hit_freeze_time = 5
              player.hit_connect = True

def handle_controls(character, event):     
    if event.type == KEYDOWN:
        if event.key == character.BACKWARD:
           character.backward = True
           character.forward = False
           if character.current_state == 'walk':
              character.xvel = -walk_speed
        elif event.key == character.FORWARD:
           character.forward = True
           character.backward = False                   
           if character.current_state == 'walk':
              character.xvel = walk_speed
        if event.key == character.UP:
           character.up = True
           character.down = False
        elif event.key == character.DOWN:
           character.down = True
           character.up = False                      
        if event.key == character.BUTTON1:
           character.button1 = True
        if event.key == character.BUTTON2:
           character.button2 = True         
    if event.type == KEYUP:
        if event.key == character.BACKWARD:
           character.backward=False
           if character.current_state == 'walk':
              character.xvel = 0
              character.current_state = 'stand'
              character.change_animation('stand')
        elif event.key == character.FORWARD:
           character.forward=False
           if character.current_state == 'walk':
              character.xvel = 0
              character.current_state = 'stand'
              character.change_animation('stand')
        if event.key == character.DOWN:
           character.down = False
        elif event.key == character.UP:
           character.up = False
              
def ai(character):
    if character.current_state == 'stand':
       if not (character.fight_distance and character.opponent.fight_distance):
          character.current_state = 'auto_walk'
          character.change_animation('walk_forward')
          character.xvel = walk_speed * character.direction
       else:
          if random.randint(0, 100) > 95:
             if character.opponent.current_state == 'attack':
                if character.opponent.fight_stance == 'high':
                   character.fight_stance = 'high'
                elif character.opponent.fight_stance == 'low':
                   character.fight_stance = 'low'  
             else:      
                character.fight_stance = random.choice(("high", "low"))
             if character.fight_stance == 'high':
                character.current_animation = character.animations['fight_stance1']
             elif character.fight_stance == 'low':
                character.current_animation = character.animations['fight_stance2']
          elif random.randint(0, 100) > 95:
             if character.opponent.current_state == 'attack':
                character.current_state = 'evade'
                character.change_animation('evade')
          elif random.randint(0, 100) > 95:
             character.current_state = 'attack'
             character.attack_type = random.choice(("normal", "strong"))
             if character.fight_stance == 'high':
                if character.attack_type == "normal":
                   character.change_animation('high_attack1')
                elif character.attack_type == "strong":
                   character.change_animation('high_attack2')                
             elif character.fight_stance == 'low':
                if character.attack_type == "normal":
                   character.change_animation('low_attack1')
                elif character.attack_type == "strong":
                   character.change_animation('low_attack2')          
    elif character.current_state == 'evade':
       if character.opponent.attack_type:
          character.backward = True
    elif character.current_state == 'walk':
       character.backward = False

def draw_hud(surface, hud1, hud2, uc_font, player, opponent):
    #draw the head up display
    if game_mode != P1_VS_COM:
       surface.blit(hud2, (0,160))
       uc_font.font = uc_font.blue_numeric_font
       uc_font.size = uc_font.scaled_size
       surface.blit(uc_font.render(("0"*(2-len(str(time))))+str(time)), (112,192))
       uc_font.font = uc_font.green_numeric_font
       surface.blit(uc_font.render(("0"*(3-len(str(player.stamina))))+str(player.stamina)), (24,176))
       surface.blit(uc_font.render(("0"*(3-len(str(opponent.stamina))))+str(opponent.stamina)), (184,176))
       uc_font.font = uc_font.gray_font
       uc_font.size = uc_font.normal_size
       surface.blit(uc_font.render(str(player.points)), (56,200))
       surface.blit(uc_font.render(str(opponent.points)), (216,200))     
    elif game_mode == P1_VS_COM:
       surface.blit(hud1, (0,160))
       uc_font.font = uc_font.blue_numeric_font
       uc_font.size = uc_font.scaled_size
       surface.blit(uc_font.render(("0"*(2-len(str(time))))+str(time)), (112,184))
       uc_font.font = uc_font.green_numeric_font
       surface.blit(uc_font.render(("0"*(3-len(str(player.stamina))))+str(player.stamina)), (24,184))
       uc_font.font = uc_font.gray_font
       uc_font.size = uc_font.normal_size
       surface.blit(uc_font.render(str(player.points)), (208,192))
       surface.blit(uc_font.render(str(opponent.points)), (208,184))
       uc_font.font = uc_font.yellow_font
       surface.blit(uc_font.render("0"+str(player.rounds)), (224,168))


class UC_Font():
     #urban champion font
     def __init__(self, image):
         font = {}
         font_size = (8, 8)
         self.normal_size = font_size
         self.scaled_size = (font_size[0]*2, font_size[1]*2)
         self.size = self.normal_size
         letters = "abcdefghijklmnoprstuvwxyz"  # 'q' is lacking
         numbers = "0123456789"
         alphabet_font = image.subsurface([257, 197, 200, 8])
         numeric_font = image.subsurface([256, 223, 109, 8])
         font[" "] = pygame.Surface(font_size).convert()
         for x in range(len(letters)):
             font[letters[x]] = pygame.Surface(font_size)
             font[letters[x]].blit(alphabet_font, (-x*font_size[0], 0))
         for x in range(len(numbers)):
             font[numbers[x]] = pygame.Surface(font_size)
             font[numbers[x]].blit(numeric_font, (-x*font_size[0], 0))

         self.white_font = font   
         self.gray_font = {}
         self.yellow_font = {}
         self.pink_font = {}
         for letter in font:
             letterimg = font[letter]
             self.gray_font[letter] = pygame.Surface(font_size).convert()
             self.yellow_font[letter] = pygame.Surface(font_size).convert()
             self.pink_font[letter] = pygame.Surface(font_size).convert()
             for y in range(letterimg.get_height()):
                 for x in range(letterimg.get_width()):
                     if letterimg.get_at((x, y)) != (0, 0, 0):
                        self.gray_font[letter].set_at((x, y), (173, 173, 173)) 
                        self.yellow_font[letter].set_at((x, y), (228, 229, 148))
                        self.pink_font[letter].set_at((x, y), (255, 110, 204))
         self.font = self.gray_font

         green_numeric_font = image.subsurface([257, 161, 160, 16])
         blue_numeric_font = image.subsurface([257, 178, 160, 16])
         self.green_numeric_font = {}
         self.blue_numeric_font = {}
         for x in range(len(numbers)):
             self.green_numeric_font[numbers[x]] = pygame.Surface(self.scaled_size)
             self.green_numeric_font[numbers[x]].blit(green_numeric_font, (-x*self.scaled_size[0], 0))
             self.blue_numeric_font[numbers[x]] = pygame.Surface(self.scaled_size)
             self.blue_numeric_font[numbers[x]].blit(blue_numeric_font, (-x*self.scaled_size[0], 0))

     def render(self, text):
        text = text.lower()
        img = pygame.Surface((len(text)*self.size[0], self.size[1])).convert()
        pos = 0
        for char in text:
            if char in self.font:
                img.blit(self.font[char], (pos, 0))
            pos += self.size[0]
        return img


class Game_Event():
     def __init__(self, image, player, opponent):
         self.images = self.load_images(image)
         self.events = []
         self.happy_lady = Happy_Lady(self.images)
         self.angry_man = Angry_Man(self.images, [player, opponent])
         self.police = Police(self.images, [player, opponent])
         self.wait = False
         
     def load_images(self, image):
         images = {'angry_man':[],
                   'happy_lady':[],
                   'papers':[],
                   'police_car':[]}
         images['angry_man'].append(image.subsurface([252, 237, 14, 34]))
         images['angry_man'].append(image.subsurface([268, 253, 16, 18]))
         images['happy_lady'].append(image.subsurface([287, 250, 12, 21]))
         images['happy_lady'].append(image.subsurface([303, 250, 14, 21]))
         images['papers'].append(image.subsurface([254, 276, 7, 8]))
         images['papers'].append(image.subsurface([264, 276, 7, 8]))
         images['papers'].append(image.subsurface([272, 276, 8, 8]))
         images['papers'].append(image.subsurface([281, 276, 8, 8]))
         images['papers'].append(image.subsurface([290, 276, 7, 8]))
         images['papers'].append(image.subsurface([299, 276, 7, 8]))
         images['papers'].append(image.subsurface([307, 276, 8, 8]))
         images['police_car'].append(image.subsurface([254, 320, 64, 24]))
         images['police_car'].append(image.subsurface([321, 320, 64, 24]))
         images['policeman_head'] = image.subsurface([301, 293, 14, 16])
         images['vase'] = image.subsurface([264, 292, 8, 14])
         images['broken_vase'] = image.subsurface([278, 291, 8, 15])
         return images
      
     def add_event(self, event_type):
         if event_type == 'angry_man':
            if not self.angry_man in self.events \
            and not self.happy_lady in self.events \
            and not self.police in self.events:
               self.angry_man.initialize()
               self.events.append(self.angry_man)
         elif event_type == 'police':      
            if not self.police in self.events \
            and not self.happy_lady in self.events:
               self.police.initialize()
               self.events.append(self.police)
         elif event_type == 'happy_lady':
            if not self.happy_lady in self.events: 
               self.events.clear()
               self.happy_lady.initialize()
               self.events.append(self.happy_lady)
               
     def scroll(self, x):
         for event in self.events:
             event.scroll(x)
             
     def clear(self):
         self.events.clear()
         self.wait = False
             
     def update(self):
         if not self.wait:
            for event in self.events:
                event.phases[event.current_phase]()
            if random.randint(1, 300) == 1:
               self.add_event('angry_man')                
            elif random.randint(1, 500) == 1:
               self.add_event('police')
                 
     def draw(self, surface):
         for event in self.events:
             event.draw(surface)


class Happy_Lady():
     def __init__(self, images):
         self.images = images['happy_lady']
         self.image = self.images[0]         
         self.y_pos = 27
         self.height = self.image.get_height()
         self.width = self.image.get_width()
         self.image_pos = [154, self.y_pos + (self.height - 1)]
         self.timer = 0
         self.time = 0
         self.papers_pos = [[[152, 51], [160, 58], [152, 68]],
                            [[138, 68], [168, 68], [144, 78], [160, 78]],
                            [[152, 88], [144, 98], [168, 98], [128, 88], [120, 78]],
                            [[152, 106], [176, 106], [128, 106], [112, 106], [104, 88], [136, 114]],
                            [[120, 122], [96, 106], [160, 122], [182, 128]],
                            [[152, 136], [128, 136], [88, 122], [72, 114]],
                            [[96, 136]],
                            [[72, 136], [50, 128]],
                            [[144, 144], [80, 144], [176, 144], [42, 144], [34, 136]],
                            [[186, 152], [202, 152], [160, 152], [120, 152], [96, 152], [64, 152]]]
         self.papers_index = 0
         self.papers_type_images = images['papers']
         self.papers_images = []
         for papers_pos in self.papers_pos:
             images = []
             for pos in papers_pos:
                 images.append(self.papers_type_images[0])
             self.papers_images.append(images)         
         self.current_phase = 'shows_up'
         self.phases = {'shows_up':self.shows_up,'throw_papers':self.throw_papers, 'hide':self.hide}
        
     def initialize(self):
         self.timer = 0
         self.time = 0
         self.image_pos = [154, self.y_pos + (self.height - 1)]
         self.papers_index = 0
         self.shows_up()
         self.current_phase = 'shows_up'
        
     def shows_up(self):
         if self.image_pos[1] != self.y_pos:
            height = (self.y_pos + self.height + 1) - self.image_pos[1]
            self.image = self.images[0].subsurface([0, 0, self.width, height])
            self.image_pos[1] -= 1
         else:
            self.image = self.images[1]
            self.image_pos = [153, 27]
            self.current_phase = 'throw_papers'
            
     def throw_papers(self):        
         self.timer += 1
         if self.timer > 5:
            self.timer = 0
            if self.papers_index < len(self.papers_pos):
               self.papers_index += 1
            if self.image == self.images[0]:
               self.image = self.images[1]
               self.image_pos = [153, 27]
            else:
               self.image = self.images[0]
               self.image_pos = [154, 27]
         self.time += 1      
         if self.time >= 200:
            self.image = self.images[0]
            self.image_pos = [154, 27]
            self.papers_index = -2
            self.current_phase = 'hide'
            
     def hide(self):        
         if self.image_pos[1] != (self.y_pos + self.height):
            height = (self.y_pos + self.height - 1) - self.image_pos[1]
            self.image = self.images[0].subsurface([0, 0, self.width, height])
            self.image_pos[1] += 1
         self.timer += 1
         if self.papers_index < len(self.papers_pos) - 3:
            if self.timer > 5:
               self.timer = 0
               self.papers_index += 1
         else:
            global game_mode
            game_mode = TITLE_SCREEN
            game_event.events.remove(self)
            game_event.wait = True
                           
     def scroll(self, x):
         self.image_pos[0] += x                  
         for papers_pos in self.papers_pos:
             for pos in papers_pos:
                 pos[0] += x
               
     def draw(self, surface):
         surface.blit(self.image, self.image_pos)
         if self.current_phase == 'throw_papers':
            for i in range(self.papers_index):
                for j in range(len(self.papers_pos[i])):
                    if self.timer == 0:
                       self.papers_images[i][j] = random.choice(self.papers_type_images)
                    surface.blit(self.papers_images[i][j], self.papers_pos[i][j])
         elif self.current_phase == 'hide':           
            for i in range(len(self.papers_pos) - 1, self.papers_index, -1):
                for j in range(len(self.papers_pos[i])):
                    if self.timer == 0:
                       self.papers_images[i][j] = random.choice(self.papers_type_images)
                    surface.blit(self.papers_images[i][j], self.papers_pos[i][j])


class Angry_Man():
     def __init__(self, images, targets):
         self.images = images['angry_man']
         self.image = self.images[1]         
         self.y_pos = 30
         self.height = self.image.get_height()
         self.width = self.image.get_width()
         self.image_pos = [88, self.y_pos + (self.height - 1)]
         self.timer = 0
         self.vase_collided = False
         self.draw_vase = False
         self.normal_vase_image = images['vase']
         self.broken_vase_image = images['broken_vase']
         self.vase_image = self.normal_vase_image
         self.vase_pos = [0, 0]
         self.targets = targets
         self.current_phase = 'shows_up'
         self.phases = {'shows_up':self.shows_up,'throw_vase':self.throw_vase, 'hide':self.hide}
         
     def initialize(self):
         self.timer = 0
         self.vase_collided = False
         self.draw_vase = False
         self.vase_image = self.normal_vase_image
         self.image_pos[1] = self.y_pos + (self.height - 1)
         self.current_phase = 'shows_up'
         self.shows_up()
         target = random.choice(self.targets)
         x_offset = int(self.width / 2)
         dx = 1000
         for pos in ([56, 48], [88, 48], [120, 48], [152, 48], [184, 48]):
             if abs((pos[0] + x_offset) - target.axis_pos[0]) < dx:
                self.image_pos = pos
                dx = abs(pos[0] - target.axis_pos[0])
        
     def collision(self, target):
         if target.current_sprite['defense_box']!= [0, 0, 0, 0]:
            offense_box = [self.vase_pos[0] + 2, self.vase_pos[1], 6, 12]
            defense_box = target.current_sprite['defense_box']
            defense_box = [target.image_pos[0] + defense_box[0],
                           target.image_pos[1] + defense_box[1],
                           defense_box[2], defense_box[3]]
            if defense_box[1] > 102:
               defense_box[1] = 102
            if offense_box[0] < defense_box[0] + defense_box[2] \
            and offense_box[0] + offense_box[2] > defense_box[0] \
            and offense_box[1] < defense_box[1] + defense_box[3] \
            and offense_box[1] + offense_box[3] > defense_box[1]:
               if defense_box[1] - offense_box[1] > 8:
                  target.stamina -= 5
                  if target.stamina < 0:
                     target.stamina = 0 
                  self.vase_collided = True
                  target.current_state = 'dizzy'
                  target.change_animation('dizzy')
                  target.timer = 0
                  target.hit_freeze_time = 20
          
     def shows_up(self):
         if self.image_pos[1] > self.y_pos:
            height = (self.y_pos + self.height + 1) - self.image_pos[1]
            self.image = self.images[1].subsurface([0, 0, self.width, height])
            self.image_pos[1] -= 1
            if self.image_pos[1] == self.y_pos:
               self.image = self.images[0]
               self.image_pos[0] += 1
               self.image_pos[1] = 14
         else:
            self.timer += 1
            if self.timer >= 20:
               self.timer = 0 
               self.image = self.images[1]
               self.image_pos[0] -= 1
               self.image_pos[1] = 30
               self.vase_pos[0] = self.image_pos[0] + 4
               self.vase_pos[1] = self.image_pos[1] + 3
               self.draw_vase = True
               self.current_phase = 'throw_vase'         
            
     def throw_vase(self):        
         if not self.vase_collided:
            for target in self.targets:
                self.collision(target)
            self.vase_pos[1] += 2               
            if self.vase_pos[1] + 14 >= ground_y_pos:
               self.vase_pos[1] = ground_y_pos - 14
               self.vase_collided = True
               self.vase_image = self.broken_vase_image
               self.vase_pos[1] -= 1
               self.timer = 20
               self.current_phase = 'hide'
         else:
            self.current_phase = 'hide'
            
     def hide(self):        
         if self.image_pos[1] != (self.y_pos + self.height):
            height = (self.y_pos + self.height - 1) - self.image_pos[1]
            self.image = self.images[1].subsurface([0, 0, self.width, height])
            self.image_pos[1] += 1
         self.timer += 1
         if self.timer == 20:
            self.vase_image = self.broken_vase_image
            self.vase_pos[1] -= 1
         if self.timer == 25:
            self.draw_vase = False
         if self.timer >= 25:
            if self.image_pos[1] == (self.y_pos + self.height):
               game_event.events.remove(self)
                           
     def scroll(self, x):
         self.image_pos[0] += x
         self.vase_pos[0] += x                  
               
     def draw(self, surface):
         surface.blit(self.image, self.image_pos)
         if self.draw_vase:
            surface.blit(self.vase_image, self.vase_pos)


class Police():
     def __init__(self, images, targets):
         self.images = images['police_car']
         self.policeman_image = images['policeman_head']
         self.image = self.images[0]         
         self.image_pos = [384, 136]
         self.policeman_pos = [0, 0]
         self.draw_policeman = False
         self.target_arrested = False
         self.timer = 0
         self.targets = targets
         self.target = None
         self.current_phase = 'patrol'
         self.phases = {'patrol':self.patrol,'arrest':self.arrest}
         
     def initialize(self):
         self.image_pos = [384, 136]
         self.draw_policeman = False
         self.target_arrested = False
         self.timer = 0
         self.target = None
         self.current_phase = 'patrol'
         
     def patrol(self):
         self.timer += 1
         if self.timer > 5:
            self.timer = 0
            if self.image == self.images[0]:
               self.image = self.images[1]
            else:
               self.image = self.images[0]  
         self.image_pos[0] -= 3
         if not self.target_arrested:
            for target in self.targets:
                if target.current_state != 'fool_police':
                   if target.current_state in ('stand', 'walk', 'auto_walk'):
                      target.fight_distance = False
                      target.current_state = 'fool_police'
                      target.change_animation('walk_backward')
                      target.xvel = -walk_speed * target.direction
                      if target.out_of_boundary(target.axis_pos[0]):
                         target.change_animation('stand')
                         target.timer = 40
         if not self.target:
            if self.image_pos[0] > 256:
               for target in self.targets:
                   if target.current_state == 'attack' \
                   and target.hit_connect:
                      self.target = target
         elif self.target:
            if self.image_pos[0] - self.target.axis_pos[0] <= -40:
               self.current_phase = 'arrest'
               self.target.current_state = 'wait'
               self.target.change_animation('caught')
               self.draw_policeman = True
               self.policeman_pos[0] = self.image_pos[0] + 18
               self.policeman_pos[1] = self.image_pos[1] + 8
               self.timer = -30
         if self.image_pos[0] < -64:
            self.image_pos[0] = -64
            if self.target_arrested:
               target = self.target
               opponent = target.opponent
               if abs(opponent.axis_pos[0] - self.target.x_boundary) < 150:
                   target.axis_pos[0] = target.x_boundary + ((256 - 10) * -target.direction)
                   opponent.fight_distance = False
                   opponent.look_at_direction()
                   opponent.timer = 0
                   opponent.current_state = 'scroll_background'
                   opponent.change_animation('walk_forward')
                   game_event.events.remove(self)
                   game_event.wait = True
                   target.points -= 1
               global right_pit, left_pit    
               if abs(opponent.axis_pos[0] - self.target.x_boundary) < 150 \
               or self.target.direction == -1 and right_pit \
               or self.target.direction == 1 and left_pit:
                  if target.direction == -1:
                     target.axis_pos[0] = 204 + 256
                     if right_pit:
                        target.points -= 1
                        opponent.current_state = 'win'
                        opponent.change_animation('win')
                        game_event.add_event('happy_lady')
                        game_event.wait = False
                     else:
                        if target.points <= 1: 
                        #if background_pos[0] <= -768:                       
                           right_pit = True
                           right_pit_pos[0] = (256 * 2) - 40
                           right_pit_old_pos[0] = (256 * 2) - 40
                        if left_pit:
                           left_pit_pos[0] = 256
                  elif target.direction == 1:
                     target.axis_pos[0] = -204
                     if left_pit:
                        target.points -= 1
                        opponent.current_state = 'win'
                        opponent.change_animation('win')
                        game_event.add_event('happy_lady')
                        game_event.wait = False
                     else:
                        if target.points <= 1: 
                        #if background_pos[0] >= -256:
                           left_pit = True
                           left_pit_pos[0] = -256
                           left_pit_old_pos[0] = -256            
                        if right_pit:
                           right_pit_pos[0] = -40
               target.axis_pos[1] = ground_y_pos
               target.fight_distance = False
               target.change_animation('stand')                           
            else:
               game_event.events.remove(self)
         
     def arrest(self):
         if self.timer < 0:
            self.timer += 1
            if self.timer < -15:
               if self.policeman_pos[0] > self.image_pos[0] + 9:
                  self.policeman_pos[0] -= 2
               if self.policeman_pos[1] > self.image_pos[1]:
                  self.policeman_pos[1] -= 2
            elif self.timer > -15:
               if self.policeman_pos[0] < self.image_pos[0] + 18:
                  self.policeman_pos[0] += 2
               if self.policeman_pos[1] < self.image_pos[1] + 8:
                  self.policeman_pos[1] += 2    
         else:
            if self.target.axis_pos[1] < 160:
               self.target.axis_pos[1] += 1
               self.timer += 1
               if self.timer > 3:
                  self.timer = 0
                  self.target.switch_sprites()
                  self.target.change_animation('caught')   
            else:
               self.target.look_at_direction()
               self.target.axis_pos[0] = -100 
               self.current_phase = 'patrol'
               self.draw_policeman = False
               self.target_arrested = True
               opponent = self.target.opponent
               global right_pit, left_pit
               if self.target.direction == -1 and right_pit \
               or self.target.direction == 1 and left_pit:
                  opponent.current_state = 'wait'
                  opponent.change_animation('stand')
               else:   
                  if abs(opponent.axis_pos[0] - self.target.x_boundary) > 150:
                     opponent.look_at_direction()
                     opponent.current_state = 'auto_walk'
                     opponent.change_animation('walk_forward')
                     opponent.xvel = walk_speed * opponent.direction
                           
     def scroll(self, x):
         self.image_pos[0] += x
               
     def draw(self, surface):
         if self.draw_policeman:
            surface.blit(self.policeman_image, self.policeman_pos) 
         surface.blit(self.image, self.image_pos)
        

class Player():
    def __init__(self, image, sprite_file, animation_file, axis_pos, character='guy1'):
        self.left_side_sprites = self.get_sprites(image, sprite_file)
        self.right_side_sprites = self.get_right_side_sprites(self.left_side_sprites)
        if character == 'guy1':
           self.sprites = self.left_side_sprites
           self.direction = 1
           self.x_boundary = 43
           self.FORWARD = K_RIGHT
           self.BACKWARD = K_LEFT
           self.UP = K_UP
           self.DOWN = K_DOWN
           self.BUTTON1 = K_h
           self.BUTTON2 = K_j
        elif character == 'guy2':
           self.sprites = self.right_side_sprites
           self.direction = -1
           self.x_boundary = 212
           self.FORWARD = K_a
           self.BACKWARD = K_d
           self.UP = K_w
           self.DOWN = K_s
           self.BUTTON1 = K_r
           self.BUTTON2 = K_t         
        self.animations = self.get_animations(animation_file, character)
        self.axis_pos = axis_pos
        self.current_animation = self.animations['stand']
        self.animation_frame = 0
        self.max_anim_time = 5
        self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        self.image_pos=[
        self.axis_pos[0] + self.current_sprite['axis_shift'][0],
        self.axis_pos[1] + self.current_sprite['axis_shift'][1]]
        self.anim_time = 0
        self.opponent = None
        self.attack_type = None
        self.hit_connect = False
        self.up = False
        self.down = False
        self.forward = False
        self.backward = False
        self.button1 = False
        self.button2 = False
        self.fight_distance = False
        self.fight_stance = 'high'
        self.timer = 0
        self.xvel = 0
        self.yvel = 0
        self.hit_freeze_time = 0
        self.stamina = 200
        self.points = 3
        self.rounds = 1
        self.current_state = 'stand'
        self.states = {'stand':self.stand, 'walk':self.walk, 'attack':self.attack, 'hurt':self.hurt,
                       'evade':self.evade, 'auto_walk':self.auto_walk, 'dizzy':self.dizzy,
                       'fool_police':self.fool_police,
                       'scroll_background':self.scroll_background, 'wait':self.wait, 'win':self.win,
                       'knocked_up':self.knocked_up, 'knocked_down':self.knocked_down, 'fall':self.fall}

    def get_sprites(self, image, player_sprite_file):
        sprites = []
        sprites_data = load_sprite_data(player_sprite_file)
        for i in range(len(sprites_data['rect'])):
            sprites.append({'image':image.subsurface(sprites_data['rect'][i]),
                            'axis_shift':sprites_data['axis_shift'][i],
                            'offense_box':sprites_data['offense_box'][i],
                            'defense_box':sprites_data['defense_box'][i]})
        return sprites
                            
    def get_animations(self, player_animation_file, character='guy1'):
        animations = {}
        animations_data = load_animation_data(player_animation_file)
        if character == 'guy1':
           animations['stand'] = animations_data[0]
           animations['walk_forward'] = animations_data[1]
           animations['walk_backward'] = animations_data[14]
           animations['fight_stance1'] = animations_data[2]
           animations['fight_stance2'] = animations_data[4]
           animations['high_attack1'] = animations_data[3]
           animations['high_attack2'] = animations_data[15]
           animations['low_attack1'] = animations_data[5]
           animations['low_attack2'] = animations_data[16]
           animations['evade'] = animations_data[9]
           animations['hurt1'] = animations_data[6]
           animations['hurt2'] = animations_data[7]
           animations['knocked_up1'] = animations_data[36]
           animations['knocked_up2'] = animations_data[37]
           animations['knocked_down'] = animations_data[8]
           animations['roll'] = animations_data[38]
           animations['win'] = animations_data[11]
           animations['dizzy'] = animations_data[10]
           animations['caught'] = animations_data[13]
           animations['look_up'] = animations_data[12]           
        elif character == 'guy2':
           animations['stand'] = animations_data[17]
           animations['walk_forward'] = animations_data[18]
           animations['walk_backward'] = animations_data[19]
           animations['fight_stance1'] = animations_data[20]
           animations['fight_stance2'] = animations_data[21]
           animations['high_attack1'] = animations_data[22]
           animations['high_attack2'] = animations_data[23]
           animations['low_attack1'] = animations_data[24]
           animations['low_attack2'] = animations_data[25]
           animations['evade'] = animations_data[29]
           animations['hurt1'] = animations_data[26]
           animations['hurt2'] = animations_data[27]
           animations['knocked_up1'] = animations_data[34]
           animations['knocked_up2'] = animations_data[35]
           animations['knocked_down'] = animations_data[28]
           animations['roll'] = animations_data[39]
           animations['win'] = animations_data[31]
           animations['dizzy'] = animations_data[30]
           animations['caught'] = animations_data[33]
           animations['look_up'] = animations_data[32]
        return animations
                            
    def get_right_side_sprites(self, sprites):
        right_side_sprites=[]
        for sprite in sprites:
            image_width, image_height = sprite['image'].get_size()             
            right_side_sprite={
            'image':pygame.transform.flip(sprite['image'], True, False),    
            'axis_shift':[-(image_width + sprite['axis_shift'][0]), sprite['axis_shift'][1]],
            'offense_box':sprite['offense_box'],
            'defense_box':sprite['defense_box']}
            if sprite['offense_box'] != [0,0,0,0]:
               offense_box = sprite['offense_box']
               right_side_offense_box = [image_width - (offense_box[0] + offense_box[2]),
                                        offense_box[1], offense_box[2], offense_box[3]]
               right_side_sprite['offense_box'] = right_side_offense_box
            if sprite['defense_box'] != [0,0,0,0]:
               defense_box = sprite['defense_box']
               right_side_defense_box = [image_width - (defense_box[0] + defense_box[2]),
                                        defense_box[1], defense_box[2], defense_box[3]]
               right_side_sprite['defense_box'] = right_side_defense_box
            right_side_sprites.append(right_side_sprite)            
        return right_side_sprites
    
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
        self.current_animation = self.animations[animation]
        self.anim_time = 0
        self.animation_frame = 0
        self.current_sprite = self.sprites[self.current_animation[self.animation_frame]]
        self.image = self.current_sprite['image']
        
    def end_of_animation(self):
        return self.animation_frame == 0 and self.anim_time == 0
                           
    def scroll_background(self):
        global right_pit, left_pit
        if self.timer < 128:
           self.timer += 1
           self.update_animation()
           if self.anim_time > 0:
              self.anim_time = self.max_anim_time 
           dx = -2 * self.direction
           #if self.timer == 66:
              #self.change_animation('stand')
           #elif self.timer > 66:
              #self.axis_pos[0] += dx
           x_offset = background_pos[0] % (256 * self.direction)
           if x_offset != 0:
              if (self.axis_pos[0] - (self.x_boundary + x_offset)) * self.direction > 10:
                 self.change_animation('stand')
                 self.axis_pos[0] += dx
           background_pos[0] += dx
           self.opponent.axis_pos[0] += dx
           if right_pit:
              right_pit_pos[0] += dx
              right_pit_old_pos[0] += dx
           if left_pit:
              left_pit_pos[0] += dx
              left_pit_old_pos[0] += dx
           game_event.scroll(dx)
        else: 
           self.timer = 0
           self.rounds += 1
           self.current_state = 'stand'
           self.reset_buttons()
           self.stamina = 200
           self.opponent.stamina = 200
           self.opponent.reset_buttons()
           self.opponent.current_state = 'stand'
           if right_pit:
              right_pit_old_pos[0] = right_pit_pos[0]
           if left_pit:
              left_pit_old_pos[0] = left_pit_pos[0]
           global time, timer
           time= 99
           timer = 0
           game_event.clear()
        
    def stand(self):
        self.update_animation()
        if self.backward:
           if (self.fight_distance and self.opponent.fight_distance):
              self.timer = 0 
              self.current_state = 'evade'
              self.change_animation('evade')
           else:
              if not self.out_of_boundary(self.axis_pos[0]): 
                 self.current_state = 'walk'
                 self.change_animation('walk_backward')
                 self.xvel = -walk_speed * self.direction
              else:
                 self.change_animation('stand')
        elif self.forward:
           if not (self.fight_distance and self.opponent.fight_distance):
              self.current_state = 'walk'
              self.change_animation('walk_forward')
              self.xvel = walk_speed * self.direction
        if self.up:
           if self.fight_stance != 'high':
              self.fight_stance = 'high'
              if self.fight_distance:
                 self.change_animation('fight_stance1')
        elif self.down:
           if self.fight_stance != 'low':
              self.fight_stance = 'low'
              if self.fight_distance:
                 self.change_animation('fight_stance2')
        if self.button1:
           self.button1 = False
           self.current_state = 'attack'
           self.attack_type = "normal"
           if self.fight_stance == 'high':
              self.change_animation('high_attack1')
           elif self.fight_stance == 'low':
              self.change_animation('low_attack1')              
        elif self.button2:
           self.button2 = False
           self.current_state = 'attack'
           self.attack_type = "strong"      
           if self.fight_stance == 'high':
              self.change_animation('high_attack2')
           elif self.fight_stance == 'low':
              self.change_animation('low_attack2')              
           
    def walk(self):
        self.axis_pos[0] += self.xvel
        if self.out_of_boundary(self.axis_pos[0]) and self.backward:
           self.axis_pos[0] = self.x_boundary
           self.current_state = 'stand'
           self.change_animation('stand')
        if not (self.fight_distance and self.opponent.fight_distance):
           if abs(self.axis_pos[0] - self.opponent.axis_pos[0]) <= fight_distance:
              self.fight_distance = True
              self.opponent.fight_distance = True
              self.axis_pos[0] = self.opponent.axis_pos[0] - fight_distance * self.direction
              self.current_state = 'stand'
              if self.fight_stance == 'high':
                 self.change_animation('fight_stance1')
              elif self.fight_stance == 'low':
                 self.change_animation('fight_stance2') 
              self.xvel = 0
              if not self.opponent.current_state in ('attack', 'dizzy'):
                 if self.opponent.current_state == 'evade':
                    self.opponent.timer = 0
                    self.opponent.backward = False
                 self.opponent.current_state = 'stand'
                 if self.opponent.fight_stance == 'high':
                    self.opponent.change_animation('fight_stance1')
                 elif self.opponent.fight_stance == 'low':
                    self.opponent.change_animation('fight_stance2')               
                 self.opponent.xvel = 0                      
        self.update_animation()
        if self.anim_time > 0:
           self.anim_time = self.max_anim_time 
        if not (self.backward or self.forward):
           self.current_state = 'stand'
           self.change_animation('stand')
           self.xvel = 0
        if self.button1:
           self.button1 = False
           self.current_state = 'attack'
           self.attack_type = "normal"
           self.change_animation('high_attack1')
        elif self.button2:
           self.button1 = False
           self.current_state = 'attack'
           self.attack_type = "strong"      
           self.change_animation('high_attack2')
           
    def auto_walk(self):
        self.update_animation()
        if self.anim_time > 0:
           self.anim_time = self.max_anim_time         
        self.axis_pos[0] += self.xvel
        if not (self.fight_distance and self.opponent.fight_distance):
           if abs(self.axis_pos[0] - self.opponent.axis_pos[0]) <= fight_distance:
              self.fight_distance = True
              self.opponent.fight_distance = True
              self.axis_pos[0] = self.opponent.axis_pos[0] - fight_distance * self.direction
              self.current_state = 'stand'
              if self.fight_stance == 'high':
                 self.change_animation('fight_stance1')
              elif self.fight_stance == 'low':
                 self.change_animation('fight_stance2') 
              self.xvel = 0
              if not self.opponent.current_state in ('attack', 'dizzy'):
                 if self.opponent.current_state == 'evade':
                    self.opponent.timer = 0
                    self.opponent.backward = False
                 self.opponent.current_state = 'stand'
                 if self.opponent.fight_stance == 'high':
                    self.opponent.change_animation('fight_stance1')
                 elif self.opponent.fight_stance == 'low':
                    self.opponent.change_animation('fight_stance2')               
                 self.opponent.xvel = 0
              
    def out_of_boundary(self, x_pos):
        return (x_pos - self.x_boundary) * self.direction <= 0
       
    def evade(self):
        if self.timer < 10:
           self.timer += 1
        elif self.timer >= 10 and self.backward \
        and not self.out_of_boundary(self.axis_pos[0] - (8 * self.direction)):
           self.update_animation()
           if self.animation_frame == 1 and self.anim_time == 0:
              self.axis_pos[0] -= 8 * self.direction
              self.fight_distance = False
           if self.end_of_animation():
              self.timer = 0
              self.update_animation()
              self.current_state = 'walk'
              self.change_animation('walk_backward')
              self.xvel = -walk_speed * self.direction
        else:
           self.timer = 0
           self.backward = False
           self.current_state = 'stand'
           if self.fight_distance:
              if self.fight_stance == 'high':
                 self.change_animation('fight_stance1')
              elif self.fight_stance == 'low':
                 self.change_animation('fight_stance2')
           else:
              self.change_animation('stand')

    def attack(self):
        self.update_animation()
        if self.end_of_animation():
           if self.stamina > 0: 
              self.stamina -= 1
           self.current_state = 'stand'
           if self.fight_distance:
              if self.fight_stance == 'high':
                 self.change_animation('fight_stance1')
              elif self.fight_stance == 'low':
                 self.change_animation('fight_stance2')                 
           else:
              if self.hit_connect and self.attack_type != "strong":
                 self.current_state = 'auto_walk'
                 self.change_animation('walk_forward')
                 self.xvel = walk_speed * self.direction
              else:
                 self.change_animation('stand')
           self.hit_connect = False
           self.attack_type = None                 
           self.button1 = False
           self.button2 = False
              
    def reset(self):
        self.reset_buttons()
        self.look_at_direction()
        self.current_state = 'stand'
        self.change_animation('stand')
        self.axis_pos[0] = self.x_boundary + (18 * self.direction)
        self.axis_pos[1] = ground_y_pos
        self.stamina = 200
        self.points = 3
        self.rounds = 1
        self.timer = 0
        self.xvel = 0
        self.yvel = 0
        self.hit_freeze_time = 0
        self.attack_type = None
        self.hit_connect = False
        self.fight_distance = False
        self.fight_stance = 'high'
        
    def reset_buttons(self):
        self.button1 = False
        self.button2 = False
        
    def hurt(self):
        if self.xvel != 0:
           self.axis_pos[0] += self.xvel
           self.xvel = 0
           self.attack_type = None
           self.hit_connect = False
           self.reset_buttons()
        self.update_animation()
        if self.end_of_animation():
           self.attack_type = None
           self.hit_connect = False
           self.current_state = 'stand'
           self.change_animation('stand')
           self.reset_buttons()
                      
    def knocked_up(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        self.yvel -= 0.5
        if self.current_animation[self.animation_frame + 1] != -1:   
           self.update_animation()
        if self.axis_pos[1] >= ground_y_pos:
           if ((right_pit and self.direction == -1)
           or (left_pit and self.direction == 1)) \
           and self.out_of_boundary(self.axis_pos[0]):
             if abs(self.axis_pos[0] - self.x_boundary) < 10:
                self.axis_pos[0] -= 10 * self.direction 
             self.fight_distance = False              
             self.current_state = 'fall'
             self.change_animation('knocked_down')
             self.opponent.current_state = 'wait'
           else:   
              self.axis_pos[1] = ground_y_pos
              #self.xvel = 1 * -self.direction
              self.yvel = 0
              self.fight_distance = False
              self.current_state = 'knocked_down'
              self.change_animation('knocked_down')
           
    def knocked_down(self):
        global right_pit, left_pit
        self.axis_pos[0] += self.xvel
        self.update_animation()
        if self.end_of_animation():
           self.xvel = 0
           self.attack_type = None
           self.hit_connect = False
           self.reset_buttons()
           if self.out_of_boundary(self.axis_pos[0]) \
           and not ((right_pit and self.direction == -1)
           or (left_pit and self.direction == 1)):
              if self.direction == -1  and self.axis_pos[0] < 266 \
              or self.direction == 1  and self.axis_pos[0] > -10:   
                 self.xvel = 1 * -self.direction
                 self.current_state = 'knocked_down'
                 self.change_animation('roll')
                 self.opponent.current_state = 'wait'
                 game_event.wait = True
              else:
                 self.points -= 1
                 if self.direction == -1:
                    self.axis_pos[0] = 204 + 256
                    #if background_pos[0] <= -768:
                    if self.points <= 1:
                       right_pit = True
                       right_pit_pos[0] = (256 * 2) - 40
                       right_pit_old_pos[0] = (256 * 2) - 40
                    if left_pit:
                       left_pit_pos[0] = 256
                 elif self.direction == 1:
                    self.axis_pos[0] = -204
                    #if background_pos[0] >= -256:
                    if self.points <= 1:    
                       left_pit = True
                       left_pit_pos[0] = -256
                       left_pit_old_pos[0] = -256            
                    if right_pit:
                       right_pit_pos[0] = -40    
                 self.current_state = 'wait'
                 self.change_animation('stand')
                 self.opponent.timer = 0
                 self.opponent.current_state = 'scroll_background'
                 self.opponent.change_animation('walk_forward')
           else:
              self.current_state = 'stand'
              self.change_animation('stand')
      
    def fall(self):
        self.axis_pos[0] += self.xvel
        self.axis_pos[1] -= self.yvel
        if self.axis_pos[1] > 180:
           self.axis_pos[0] = -100
           self.axis_pos[1] = -100
           self.current_state = 'wait'
           self.opponent.current_state = 'win'
           self.opponent.change_animation('win')
           self.opponent.timer = 0
           game_event.add_event('happy_lady')
           global timer
           timer = -1000
           
    def win(self):
        self.timer += 1
        if self.timer > 20:
           self.timer = 0
           self.switch_sprites()
           self.change_animation('win')
        
    def wait(self):
        pass

    def dizzy(self):
        if self.current_animation[self.animation_frame + 1] != -1:
           self.update_animation()
        self.anim_time += 1
        if self.anim_time >= self.max_anim_time:
           self.anim_time = 0
           self.switch_sprites()
           self.current_sprite = self.sprites[self.current_animation[self.animation_frame]] 
           self.image = self.current_sprite['image']
           self.timer += 1
           if self.timer >= 13:
              self.timer = 0
              self.reset_buttons()
              self.look_at_direction()
              self.current_state = 'stand'
              if self.fight_distance:
                 if self.fight_stance == 'high':
                    self.change_animation('fight_stance1')
                 elif self.fight_stance == 'low':
                    self.change_animation('fight_stance2')
              else:
                 self.change_animation('stand')
                 
    def fool_police(self):
        if not self.out_of_boundary(self.axis_pos[0]):
           self.axis_pos[0] += self.xvel
           self.update_animation()
           if self.out_of_boundary(self.axis_pos[0]):
              self.change_animation('stand')
              self.timer = 40
        else:
           if game_event.police.image_pos[0] < 200:
              self.timer += 1
              if self.timer > 40:
                 self.timer = 0
                 self.switch_sprites()
                 self.change_animation('look_up')
           if game_event.police not in game_event.events:
              self.reset_buttons() 
              self.look_at_direction()
              self.current_state = 'stand'
              self.change_animation('stand')
              
    def switch_sprites(self):
        if self.sprites == self.left_side_sprites:
           self.sprites = self.right_side_sprites
        elif self.sprites == self.right_side_sprites:
           self.sprites = self.left_side_sprites
           
    def look_at_direction(self):
        if self.direction == 1:
           self.sprites = self.left_side_sprites
        elif self.direction == -1:
           self.sprites = self.right_side_sprites                 
        
    def draw(self, surface):
        self.image_pos[0] = self.axis_pos[0] + self.current_sprite['axis_shift'][0]
        self.image_pos[1] = self.axis_pos[1] + self.current_sprite['axis_shift'][1]
        surface.blit(self.image, self.image_pos)
        
        #offense_box = self.current_sprite['offense_box']
        #offense_box = [self.image_pos[0] + offense_box[0],
                      #self.image_pos[1] + offense_box[1],
                      #offense_box[2], offense_box[3]]
        #pygame.draw.rect(surface, RED, offense_box, 2)
        
        #defense_box = self.current_sprite['defense_box']
        #defense_box = [self.image_pos[0] + defense_box[0],
                      #self.image_pos[1] + defense_box[1],
                      #defense_box[2], defense_box[3]]
        #pygame.draw.rect(surface, GREEN, defense_box, 2)        
        
        
def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode(SCREEN_SIZE,) #add RESIZABLE or FULLSCREEN
    display_surface = pygame.Surface(NES_RESOLUTION).convert()
    scaled_display_surface = pygame.transform.scale(display_surface,(640,480))
    #Title
    pygame.display.set_caption("Urban Champion")
    #icon
    icon = pygame.Surface((1, 1))
    icon.set_alpha(0)
    pygame.display.set_icon(icon)    
    #font
    font=pygame.font.SysFont('Arial', 30)
    #clock
    clock = pygame.time.Clock()

    #images
    image = pygame.image.load('data\\NES - Urban Champion - Characters.png').convert()
    background = pygame.image.load('data\\NES - Urban Champion - Street Map.gif').convert()
    pit1 = pygame.image.load('data\\pit1.png').convert()
    pit2 = pygame.image.load('data\\pit2.png').convert()
    image.set_colorkey(image.get_at((0,150)))
    #head_up_display
    hud1 = image.subsurface([256, 0, 256, 71])
    hud2 = image.subsurface([256, 73, 256, 71])
    uc_font = UC_Font(image)
    #icon
    icon = image.subsurface([160, 32, 64, 48])
    pygame.display.set_icon(icon)
    #variables
    global walk_speed, ground_y_pos, background_pos, sounds, fight_distance, x_min, x_max, left_pit, right_pit
    global left_pit_pos, right_pit_pos, left_pit_old_pos, right_pit_old_pos, game_event, time, timer, game_mode
    left_pit_pos = [0, 136]
    right_pit_pos = [216, 136]
    left_pit_old_pos = [0, 136]
    right_pit_old_pos = [216, 136]
    walk_speed = 2  #1.5
    ground_y_pos = 140
    fight_distance = 24
    x_min = 29
    x_max = 198
    left_pit = False
    right_pit = False
    #sounds = load_sounds()
    player = Player(image, 'data\\sprite_info.spr', 'data\\animation_info.anm', [61, ground_y_pos])#61
    opponent = Player(image, 'data\\sprite_info.spr', 'data\\animation_info.anm', [194, ground_y_pos], 'guy2')#194
    player.opponent = opponent
    opponent.opponent = player
    game_event = Game_Event(image, player, opponent)
    background_width, background_height = background.get_size()
    background_pos = [-512, 0]  #[-512-256*2, 0]
    game_mode = P1_VS_P2
    time = 99
    timer = 0
    game_mode = title_screen(image, screen, display_surface, uc_font)

        
    #pygame.key.set_repeat(400, 30)

    while True:
        #loop speed limitation
        #30 frames per second is enought
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  game_mode = TITLE_SCREEN 
               elif event.key == K_p:
                  pause(screen, uc_font)
            if game_mode != COM_VS_COM:
               handle_controls(player, event)
            if game_mode == P1_VS_P2:
               handle_controls(opponent, event)
            

        game_event.update()
                      
        if player.fight_distance and opponent.fight_distance:
           collisions(player, opponent)
           collisions(opponent, player)
                                         
        if player.hit_freeze_time < 1:
           player.states[player.current_state]()
           if game_mode == COM_VS_COM:
              ai(player)
        else:
           player.hit_freeze_time -= 1

        if opponent.hit_freeze_time < 1:
           opponent.states[opponent.current_state]()
           if game_mode != P1_VS_P2:
              ai(opponent)
        else:
           opponent.hit_freeze_time -= 1

        timer += 1
        if timer >= 30:
           timer = 0
           if time > 0 and not game_event.wait:
              time -= 1
              if time < 0:
                 time = 0
        if time <= 0 and player.axis_pos[1] == ground_y_pos \
        and opponent.axis_pos[1] == ground_y_pos:
           if player.current_state in ('stand', 'walk', 'auto_walk'):
              player.current_state = 'wait'
              player.change_animation('stand')
           if opponent.current_state in ('stand', 'walk', 'auto_walk'):
              opponent.current_state = 'wait'
              opponent.change_animation('stand')
           if not game_event.police in game_event.events:
              game_event.add_event("police")
              game_event.police.target_arrested = True
              distance1 = abs(player.axis_pos[0] - player.x_boundary)
              distance2 = abs(opponent.axis_pos[0] - opponent.x_boundary)
              if distance1 >= distance2:
                 game_event.police.target = opponent
              else:
                 game_event.police.target = player


        if game_mode == TITLE_SCREEN :
           game_mode = title_screen(image, screen, display_surface, uc_font)
           time = 99
           timer = 0
           player.reset()
           opponent.reset()
           background_pos[0] = -512
           game_event.clear()
           left_pit = False
           right_pit = False


        #draw everything
        display_surface.fill(BLACK)
        display_surface.blit(background, background_pos)
        if right_pit:
           display_surface.blit(pit1, right_pit_pos)
           display_surface.blit(pit1, right_pit_old_pos)
        if left_pit:
           display_surface.blit(pit1, left_pit_pos)
           display_surface.blit(pit1, left_pit_old_pos)
        player.draw(display_surface)
        opponent.draw(display_surface)
        if right_pit:
           display_surface.blit(pit2, (right_pit_pos[0], 145))
        if left_pit:
           display_surface.blit(pit2, (left_pit_pos[0], 145))
        game_event.draw(display_surface)
        draw_hud(display_surface, hud1, hud2, uc_font, player, opponent)
        scaled_display_surface = pygame.transform.scale(display_surface, SCREEN_SIZE)
        screen.blit(scaled_display_surface, (0,0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
