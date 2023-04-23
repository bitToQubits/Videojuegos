import pygame,sys
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
HALF_SCREEN_WIDTH=int(SCREEN_WIDTH/2)
HALF_SCREEN_HEIGHT=int(SCREEN_HEIGHT/2)
SPRITE_FILE_NAME = "data//sprite_info.spr"
ANIMATION_FILE_NAME = "data//animation_info.anm"
SPRITE_SHEET = "data//NES - Urban Champion - Characters.png"



def scale_image(image, scale):
    return pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale)).convert()

def scale_sprite(image, sprite_rect, scale):
    sprite = image.subsurface(sprite_rect)
    if image_transparency:
       sprite.set_colorkey(alpha_color)
    return pygame.transform.scale(sprite, (sprite.get_width()*scale, sprite.get_height()*scale)).convert()

def scale_rect(rect, scale):
    rect.x *= scale
    rect.y *= scale
    rect.width *= scale
    rect.height *= scale

def center_rect(rect, center):
    sprite_pos = [0,0]
    sprite_pos[0] = center[0] - int(rect.width / 2)
    sprite_pos[1] = center[1] - int(rect.height / 2)
    return sprite_pos

def save_data(sprites, animations):
    with open(SPRITE_FILE_NAME, 'w') as file:
         data = ""
         for i in range(len(sprites['rect'])):
             data += str(sprites['rect'][i][0]) + " "
             data += str(sprites['rect'][i][1]) + " "
             data += str(sprites['rect'][i][2]) + " "
             data += str(sprites['rect'][i][3]) + ","                              
             data += str(sprites['axis_shift'][i][0]) + " "
             data += str(sprites['axis_shift'][i][1]) + ","
             data += str(sprites['offense_box'][i][0]) + " "
             data += str(sprites['offense_box'][i][1]) + " "
             data += str(sprites['offense_box'][i][2]) + " "
             data += str(sprites['offense_box'][i][3]) + ","
             data += str(sprites['defense_box'][i][0]) + " "
             data += str(sprites['defense_box'][i][1]) + " "
             data += str(sprites['defense_box'][i][2]) + " "
             data += str(sprites['defense_box'][i][3]) + ";"
         file.write(data)
    with open(ANIMATION_FILE_NAME, 'w') as file:
         data = ""
         for i in range(len(animations)):
             anim_length = len(animations[i])
             if anim_length > 0:
                for j in range(anim_length):
                    data += str(animations[i][j])
                    if j + 1 != anim_length:
                       data += " "
                data += ","
             else:
                data += "-1," 
         file.write(data)
         
def sprite_editor(screen, sprites, animations, original_image):
    global image_transparency
    image = original_image.copy()
    animations_length = len(animations)
    animations_index = 0
    sprites_length = len(sprites['rect'])
    sprites_index = 0
    sprite_pos = [0,0]
    sprite_center =[HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT]
    sprite_original_move_speed = 5
    sprite_move_speed = sprite_original_move_speed
    sprite_rect = Rect([0, 0, 0, 0])
    scale = 1
    scale_max = 7    
    if sprites_length > sprites_index:
       sprite_rect = Rect(sprites['rect'][sprites_index])
       sprite_pos = center_rect(sprite_rect, sprite_center)
       current_sprite = scale_sprite(original_image, sprite_rect, scale)
    clock=pygame.time.Clock()
    font=pygame.font.SysFont('Arial', 30)
    info_font = pygame.font.SysFont('Arial', 20, bold=True)
    sprite_info = info_font.render("sprite: {}/{}".format(sprites_index, sprites_length-1), True, YELLOW)
    sprite_info_pos = [SCREEN_WIDTH - sprite_info.get_width()-5, 5]
    animation_info = info_font.render("animation: {}/{}".format(animations_index, animations_length-1), True, YELLOW)
    message = "Sprite Editor "
    message_time = 50
    text=font.render(message, True, YELLOW)
    text_pos = [0,0]
    text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
    text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
    gripping_start_pos = [0, 0]
    collision_rect_gripping = False
    collision_box = None
    show_hit_box = True
    
    
    pygame.key.set_repeat(400, 30)

    while True:
        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #keyboard commands    
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                   #go to the next sprite 
                   sprites_index += 1
                   if sprites_index >= sprites_length:
                      sprites_index = sprites_length-1
                   if sprites_length > sprites_index:
                      sprite_rect = Rect(sprites['rect'][sprites_index])
                      current_sprite = scale_sprite(original_image, sprite_rect, scale)
                      scale_rect(sprite_rect, scale)
                      sprite_pos = center_rect(sprite_rect, sprite_center)
                      sprite_info = info_font.render("sprite: {}/{}".format(sprites_index, sprites_length-1), True, YELLOW)
                      sprite_info_pos = [SCREEN_WIDTH - sprite_info.get_width()-5, 5]
                elif event.key == K_LEFT:
                   #go to the previous sprite 
                   sprites_index -= 1              
                   if sprites_index < 0:
                      sprites_index = 0
                   if sprites_length > sprites_index:
                      sprite_rect = Rect(sprites['rect'][sprites_index])
                      current_sprite = scale_sprite(original_image, sprite_rect, scale)
                      scale_rect(sprite_rect, scale)
                      sprite_pos = center_rect(sprite_rect, sprite_center)
                      sprite_info = info_font.render("sprite: {}/{}".format(sprites_index, sprites_length-1), True, YELLOW)
                      sprite_info_pos = [SCREEN_WIDTH - sprite_info.get_width()-5, 5]
                elif event.key == K_UP:
                   #scale up the sprite 
                   if scale <  scale_max:
                      scale+=1
                   else:
                      scale = scale_max
                   #sprite_move_speed = sprite_original_move_speed * scale
                   #image = scale_image(original_image, scale)
                   sprite_rect = Rect(sprites['rect'][sprites_index])
                   current_sprite = scale_sprite(original_image, sprite_rect, scale)
                   #scale_rect(sprite_rect, scale)
                   scale_rect(sprite_rect, scale)
                   sprite_pos = center_rect(sprite_rect, sprite_center)
                elif event.key == K_DOWN:
                   #scale down the sprite 
                   if scale >  1:
                      scale -= 1
                   else:
                      scale = 1
                   #sprite_move_speed = sprite_original_move_speed * scale
                   #image = scale_image(original_image, scale)
                   sprite_rect = Rect(sprites['rect'][sprites_index])
                   current_sprite = scale_sprite(original_image, sprite_rect, scale)
                   scale_rect(sprite_rect, scale)
                   sprite_pos = center_rect(sprite_rect, sprite_center)
                elif event.key == K_o:
                   #set the sprite's position to origin
                   sprite_center[0] = int(sprite_rect[2] / 2)
                   sprite_center[1] = int(sprite_rect[3] / 2)
                   sprite_pos = center_rect(sprite_rect, sprite_center)
                elif event.key == K_c:
                   #center the sprite
                   sprite_center =[HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT]
                   sprite_pos = center_rect(sprite_rect, sprite_center)
                elif event.key == K_y:
                   #show or hide the hit_boxes 
                   if not show_hit_box:
                      show_hit_box = True
                   else:
                      show_hit_box = False
                elif event.key == K_t:
                   #toggle on/off the sprite's background color transparency 
                   if not image_transparency:
                      image_transparency = True
                   else:
                      image_transparency = False
                   current_sprite = scale_sprite(original_image, sprite_rect, scale)
                elif event.key == K_d:
                   #delete the current sprite
                   if sprites_length > 0:
                      del(sprites['rect'][sprites_index])
                      del(sprites['axis_shift'][sprites_index])
                      del(sprites['offense_box'][sprites_index])
                      del(sprites['defense_box'][sprites_index])
                      sprites_length = len(sprites['rect'])
                      if sprites_index > sprites_length-1:
                         sprites_index = sprites_length-1
                      if sprites_length > 0:
                         sprite_rect = Rect(sprites['rect'][sprites_index])
                         current_sprite = scale_sprite(original_image, sprite_rect, scale)
                         scale_rect(sprite_rect, scale)
                         sprite_pos = center_rect(sprite_rect, sprite_center)
                      message = "sprite deleted " +  str(sprites_length) + " remained"
                      message_time = 50
                      text=font.render(message, True, YELLOW)
                      text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                      text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
                      sprite_info = info_font.render("sprite: {}/{}".format(sprites_index, sprites_length-1), True, YELLOW)
                      sprite_info_pos = [SCREEN_WIDTH - sprite_info.get_width()-5, 5]
                elif event.key == K_RETURN:
                     #save changes to a file
                     save_data(sprites, animations) 
                     message = "changes saved"
                     message_time = 50
                     text = font.render("changes saved", True, YELLOW)
                     text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                     text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
                elif event.key == K_n:
                   #go to next animation 
                   animations_index += 1
                   if animations_index >= animations_length:
                      animations_index = animations_length-1
                   animation_info = info_font.render("animation: {}/{}".format(animations_index, animations_length-1), True, YELLOW)
                elif event.key == K_v:
                   #go to previous animation 
                   animations_index -= 1
                   if animations_index < 0:
                      animations_index = 0
                   animation_info = info_font.render("animation: {}/{}".format(animations_index, animations_length-1), True, YELLOW)
                elif event.key == K_SPACE:
                   #add the current sprite to the selected animation 
                   animations[animations_index].append(sprites_index)
                   message = "sprite {} added to animation {}".format(sprites_index, animations_index)
                   message_time = 50
                   text=font.render(message, True, YELLOW)
                   text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                   text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)                    
                elif event.key == K_s:
                   #exit the sprite editor
                   return
            if event.type == MOUSEBUTTONDOWN:
               #set the starting point for the hitbox
               if event.button == 1: 
                  collision_box = sprites['offense_box'][sprites_index]
                  gripping_start_pos[0] =  event.pos[0] - sprite_pos[0]
                  gripping_start_pos[1] =  event.pos[1] - sprite_pos[1]
                  collision_box[0] =  event.pos[0] - sprite_pos[0]
                  collision_box[1] =  event.pos[1] - sprite_pos[1]
                  collision_box[2] = 0
                  collision_box[3] = 0
                  collision_rect_gripping = True
               elif event.button == 3:
                  collision_box = sprites['defense_box'][sprites_index]
                  gripping_start_pos[0] =  event.pos[0] - sprite_pos[0]
                  gripping_start_pos[1] =  event.pos[1] - sprite_pos[1]
                  collision_box[0] =  event.pos[0] - sprite_pos[0]
                  collision_box[1] =  event.pos[1] - sprite_pos[1]
                  collision_box[2] = 0
                  collision_box[3] = 0
                  collision_rect_gripping = True
            elif event.type == MOUSEBUTTONUP:
               #finish from drawing the hitbox 
               if collision_rect_gripping:
                  collision_rect_gripping = False
                  collision_box[0] =  gripping_start_pos[0]
                  collision_box[1] =  gripping_start_pos[1]
                  collision_box[2] = event.pos[0] - sprite_pos[0] - collision_box[0]
                  collision_box[3] = event.pos[1] - sprite_pos[1] - collision_box[1]
                  collision_box[0] = int(collision_box[0] / scale)
                  collision_box[1] = int(collision_box[1] / scale)
                  collision_box[2] = int(collision_box[2] / scale)
                  collision_box[3] = int(collision_box[3] / scale)
                  if collision_box[2] < 0:
                     collision_box[2] *= -1
                     collision_box[0] -= collision_box[2]
                  if collision_box[3] < 0:
                     collision_box[3] *= -1
                     collision_box[1] -= collision_box[3]                
            elif event.type == MOUSEMOTION:
               #draw the hitbox
               if collision_rect_gripping:
                  collision_box[0] =  gripping_start_pos[0]
                  collision_box[1] =  gripping_start_pos[1]
                  collision_box[2] = event.pos[0] - sprite_pos[0] - collision_box[0]
                  collision_box[3] = event.pos[1] - sprite_pos[1] - collision_box[1]
                  collision_box[0] = int(collision_box[0] / scale)
                  collision_box[1] = int(collision_box[1] / scale)
                  collision_box[2] = int(collision_box[2] / scale)
                  collision_box[3] = int(collision_box[3] / scale)
                  if collision_box[2] < 0:
                     collision_box[2] *= -1
                     collision_box[0] -= collision_box[2]
                  if collision_box[3] < 0:
                     collision_box[3] *= -1
                     collision_box[1] -= collision_box[3]

                  
        #move the sprite
        keys = pygame.key.get_pressed()
        if keys[K_u]:
           sprite_center[1] -= sprite_move_speed
           sprite_pos = center_rect(sprite_rect, sprite_center)
        elif keys[K_j]:
           sprite_center[1] += sprite_move_speed
           sprite_pos = center_rect(sprite_rect, sprite_center)
        if keys[K_h]:
           sprite_center[0] -= sprite_move_speed
           sprite_pos = center_rect(sprite_rect, sprite_center)
        elif keys[K_k]:
           sprite_center[0] += sprite_move_speed
           sprite_pos = center_rect(sprite_rect, sprite_center)
              
                    
        #draw everything
        screen.fill(BLACK)
        if sprites_length > 0:
           #screen.blit(image, sprite_pos, sprite_rect)
           screen.blit(current_sprite, sprite_pos)
           if show_hit_box:
              temp_rect = sprites['defense_box'][sprites_index]
              rect = [sprite_pos[0]+temp_rect[0]*scale,sprite_pos[1]+temp_rect[1]*scale,
                      temp_rect[2]*scale,temp_rect[3]*scale]
              pygame.draw.rect(screen, GREEN, rect,5)
              temp_rect = sprites['offense_box'][sprites_index]
              rect = [sprite_pos[0]+temp_rect[0]*scale,sprite_pos[1]+temp_rect[1]*scale,
                      temp_rect[2]*scale,temp_rect[3]*scale]
              pygame.draw.rect(screen, RED, rect,5)
           screen.blit(sprite_info, sprite_info_pos)
           screen.blit(animation_info, (5, 455))
           offense_box_info = info_font.render("offense box: {}, {}, {}, {}".format(*sprites['offense_box'][sprites_index]), True, YELLOW)
           defense_box_info = info_font.render("defense box: {}, {}, {}, {}".format(*sprites['defense_box'][sprites_index]), True, YELLOW)
           screen.blit(offense_box_info, (300, 435))
           screen.blit(defense_box_info, (300, 455))
        if message_time > 0:
           message_time -= 1
           if message_time < 0:
              message_time = 0
           text=font.render(message, True, YELLOW)
           screen.blit(text, text_pos)           
        pygame.display.flip()


def animation_editor(screen, sprites, animations, original_image):
    global image_transparency
    image = original_image.copy()
    animations_length = len(animations)
    animations_index = 0
    current_animation = animations[animations_index]
    current_animation_length = len(current_animation)
    anim_time = 0
    max_anim_time = 5
    play_animation = True
    current_sprite = None
    frame_index = 0
    axis_pos = [200, 400]
    clock=pygame.time.Clock()
    font=pygame.font.SysFont('Arial', 30)
    info_font = pygame.font.SysFont('Arial', 20, bold=True)    
    scale = 1
    scale_max = 7    
    if current_animation_length > 0:
       current_frame = current_animation[frame_index]
       sprite_rect = Rect(sprites['rect'][current_frame])
       axis_shift = sprites['axis_shift'][current_frame]
       sprite_pos = [axis_shift[0]+axis_pos[0],axis_shift[1]+axis_pos[1]]        
       current_sprite = scale_sprite(original_image, sprite_rect, scale)
       axis_shift_info = info_font.render("axis shift: x {} y {}".format(*axis_shift), True, YELLOW)
    animation_info = info_font.render("animation: {}/{}".format(animations_index, animations_length-1), True, YELLOW)
    frame_info = info_font.render("frame: {}/{}".format(frame_index, current_animation_length-1), True, YELLOW)
    message = "Animation Editor "
    message_time = 50
    text=font.render(message, True, YELLOW)
    text_pos = [0,0]
    text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
    text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
    image_gripping = False
    dragging_start_pos = [0, 0]
    dragging_end_pos = [0, 0]
    show_hit_box = False

    
    pygame.key.set_repeat(400, 30)

    while True:
        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #keyboard commands    
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                   #go to the next animation 
                   animations_index += 1
                   if animations_index >= animations_length:
                      animations_index = animations_length-1
                   animation_info = info_font.render("animation: {}/{}".format(animations_index, animations_length-1), True, YELLOW)
                   current_animation = animations[animations_index]
                   current_animation_length = len(current_animation)
                   if current_animation_length > 0:
                      frame_index = 0 
                      current_frame = current_animation[frame_index]
                      sprite_rect = Rect(sprites['rect'][current_frame])
                      axis_shift = sprites['axis_shift'][current_frame]
                      sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]                           
                      current_sprite = scale_sprite(original_image, sprite_rect, scale)
                      axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)
                   else:
                      current_sprite = None
                elif event.key == K_LEFT:
                   #go to the previous animation 
                   animations_index -= 1              
                   if animations_index < 0:
                      animations_index = 0
                   animation_info = info_font.render("animation: {}/{}".format(animations_index, animations_length-1), True, YELLOW)
                   current_animation = animations[animations_index]
                   current_animation_length = len(current_animation)
                   if current_animation_length > 0:
                      frame_index = 0 
                      current_frame = current_animation[frame_index]
                      sprite_rect = Rect(sprites['rect'][current_frame])
                      axis_shift = sprites['axis_shift'][current_frame]
                      sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]                           
                      current_sprite = scale_sprite(original_image, sprite_rect, scale)
                      axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)
                   else:
                      current_sprite = None                      
                elif event.key == K_UP:
                   #go to the next frame in the current animation 
                   play_animation = False
                   frame_index += 1
                   if frame_index >= current_animation_length:
                      frame_index = current_animation_length-1
                   if current_animation_length > 0:
                      current_frame = current_animation[frame_index]
                      sprite_rect = Rect(sprites['rect'][current_frame])
                      axis_shift = sprites['axis_shift'][current_frame]
                      sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]                           
                      current_sprite = scale_sprite(original_image, sprite_rect, scale)
                      frame_info = info_font.render("frame: {}/{}".format(frame_index, current_animation_length-1), True, YELLOW)
                      axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)
                elif event.key == K_DOWN:
                   #go to the previous frame in the current animation  
                   play_animation = False 
                   frame_index -= 1              
                   if frame_index < 0:
                      frame_index = 0
                   if current_animation_length > 0:   
                      current_frame = current_animation[frame_index]
                      sprite_rect = Rect(sprites['rect'][current_frame])
                      axis_shift = sprites['axis_shift'][current_frame]
                      sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]                           
                      current_sprite = scale_sprite(original_image, sprite_rect, scale)
                      frame_info = info_font.render("frame: {}/{}".format(frame_index, current_animation_length-1), True, YELLOW)
                      axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)
                elif event.key == K_i:
                   #scale up the sprite 
                   if scale <  scale_max:
                      scale+=1
                   else:
                      scale = scale_max
                   sprite_rect = Rect(sprites['rect'][current_frame])
                   current_sprite = scale_sprite(original_image, sprite_rect, scale)
                   axis_shift = sprites['axis_shift'][current_frame]
                   sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]                           
                elif event.key == K_j:
                   #scale down the sprite 
                   if scale >  1:
                      scale -= 1
                   else:
                      scale = 1
                   sprite_rect = Rect(sprites['rect'][current_frame])
                   current_sprite = scale_sprite(original_image, sprite_rect, scale)
                   axis_shift = sprites['axis_shift'][current_frame]
                   sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]
                elif event.key == K_c:
                   #center the sprite
                   axis_shift 
                   w, h = sprite_rect[2], sprite_rect[3]
                   axis_shift[0] = -int(w / 2)
                   axis_shift[1] = -h
                   sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]
                   axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)
                elif event.key == K_p:
                   #pause or unpause the animation
                   if not play_animation:
                      play_animation = True
                   else:
                      play_animation = False
                elif event.key == K_y:
                   #show or hide the hit_boxes 
                   if not show_hit_box:
                      show_hit_box = True
                   else:
                      show_hit_box = False
                elif event.key == K_t:
                   #toggle on/off the sprite's background color transparency 
                   if not image_transparency:
                      image_transparency = True
                   else:
                      image_transparency = False
                   current_sprite = scale_sprite(original_image, sprite_rect, scale)
                elif event.key == K_d:
                   #delete the current frame
                   if current_animation_length > 0 and not play_animation:
                      del(current_animation[frame_index])
                      current_animation_length = len(current_animation)
                      if frame_index > current_animation_length-1:
                         frame_index = current_animation_length-1
                      if current_animation_length > 0:
                         current_frame = current_animation[frame_index]
                         sprite_rect = Rect(sprites['rect'][current_frame])
                         axis_shift = sprites['axis_shift'][current_frame]
                         sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]                           
                         current_sprite = scale_sprite(original_image, sprite_rect, scale)
                      else:
                         current_sprite = None
                      message = "frame deleted " +  str(current_animation_length) + " remained"
                      message_time = 50
                      text=font.render(message, True, YELLOW)
                      text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                      text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
                      frame_info = info_font.render("frame: {}/{}".format(frame_index, current_animation_length-1), True, YELLOW)
                elif event.key == K_RETURN:
                     #save changes to a file
                     if image_gripping:
                        axis_shift[0] = int(axis_shift[0])
                        axis_shift[1] = int(axis_shift[1]) 
                     save_data(sprites, animations) 
                     message = "changes saved"
                     message_time = 50
                     text = font.render("changes saved", True, YELLOW)
                     text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                     text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
                elif event.key == K_x:
                   #exit the animation editor
                   return
            if event.type == MOUSEBUTTONDOWN:
               #grab the sprite 
               if event.button == 1:
                  rect = Rect(sprite_pos , current_sprite.get_size())
                  if rect.collidepoint(event.pos):
                     image_gripping = True
                     dragging_start_pos = event.pos
                     play_animation = False
            elif event.type == MOUSEBUTTONUP:
               #drop the sprite
               if image_gripping:
                  image_gripping = False
                  axis_shift[0] = int(axis_shift[0])
                  axis_shift[1] = int(axis_shift[1])
                  sprite_rect = Rect(sprites['rect'][current_frame])
                  current_sprite = scale_sprite(original_image, sprite_rect, scale)
                  sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]
                  axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)
            elif event.type == MOUSEMOTION:
               #drag the sprite
               if image_gripping:
                  dragging_end_pos = event.pos
                  axis_shift[0] += (dragging_end_pos[0] - dragging_start_pos[0]) / scale
                  axis_shift[1] += (dragging_end_pos[1] - dragging_start_pos[1]) / scale
                  dragging_start_pos = event.pos
                  sprite_rect = Rect(sprites['rect'][current_frame])
                  current_sprite = scale_sprite(original_image, sprite_rect, scale)
                  sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]
                  axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)
                  
        #update the animation
        if play_animation and current_animation_length > 0:
           anim_time+=1
           if anim_time>=max_anim_time:
              anim_time=0
              frame_index+=1
              if frame_index >= current_animation_length:
                 frame_index=0
              current_frame = current_animation[frame_index]
              sprite_rect = Rect(sprites['rect'][current_frame])
              axis_shift = sprites['axis_shift'][current_frame]
              sprite_pos = [axis_shift[0]*scale+axis_pos[0],axis_shift[1]*scale+axis_pos[1]]                           
              current_sprite = scale_sprite(original_image, sprite_rect, scale)
              frame_info = info_font.render("frame: {}/{}".format(frame_index, current_animation_length-1), True, YELLOW)
              axis_shift_info = info_font.render("axis shift: x {} y {}".format(int(axis_shift[0]), int(axis_shift[1])), True, YELLOW)

          
        #draw everything
        screen.fill(BLACK)
        if current_sprite:
           screen.blit(current_sprite, sprite_pos)
           if show_hit_box:
              temp_rect = sprites['defense_box'][frame_index]
              rect = [sprite_pos[0]+temp_rect[0]*scale,sprite_pos[1]+temp_rect[1]*scale,
                      temp_rect[2]*scale,temp_rect[3]*scale]
              pygame.draw.rect(screen, GREEN, rect,5)
              temp_rect = sprites['offense_box'][frame_index]
              rect = [sprite_pos[0]+temp_rect[0]*scale,sprite_pos[1]+temp_rect[1]*scale,
                      temp_rect[2]*scale,temp_rect[3]*scale]
              pygame.draw.rect(screen, RED, rect,5)
           screen.blit(axis_shift_info,(420,455))
        pygame.draw.line(screen,BLUE,(axis_pos[0]-15,axis_pos[1]),
                        (axis_pos[0]+15,axis_pos[1]),5)
        pygame.draw.line(screen,BLUE,(axis_pos[0],axis_pos[1]-15),
                        (axis_pos[0],axis_pos[1]+15),5)
        screen.blit(animation_info, (5, 455))
        if current_animation_length > 0:
           screen.blit(frame_info, (250, 455))
        if message_time > 0:
           message_time -= 1
           if message_time < 0:
              message_time = 0
           text=font.render(message, True, YELLOW)
           screen.blit(text, text_pos)           
        pygame.display.flip()

    
class Sprite_Captor():
    def __init__(self):
        self.rect = Rect([0, 0, 0, 0])
        self.line_thickness = 5
        self.scale = 1
        self.font = pygame.font.SysFont('Arial', 25, bold=True)
        self.colors = [WHITE, GREEN, BLACK]
        self.colors_lenght = len(self.colors)-1
        self.color = self.colors[1]
        self.color_index = 0
        self.color_max_time = 15
        self.timer = 0
        self.increment = 1
        self.gripping = False
        self.rect_info = self.font.render("x:{}  y:{}  w:{}  h:{}".format(*self.rect), True, YELLOW)

    def update(self, event, image, image_pos):
        if event.type == MOUSEBUTTONDOWN:
           if event.button == 1:
              self.rect.x, self.rect.y = event.pos
              self.rect.width = 0
              self.rect.height = 0
              self.gripping = True
        elif event.type == MOUSEBUTTONUP:
           if event.button == 1: 
             self.gripping = False
             if self.rect.width < 0:
                self.rect.width *= -1
                self.rect.x -= self.rect.width
             if self.rect.height < 0:
                self.rect.height *= -1
                self.rect.y -= self.rect.height
             image_rect = image.get_rect()
             image_rect.topleft = image_pos
             #check for overflow
             if self.rect.right > image_rect.right \
             or self.rect.left < image_rect.left \
             or self.rect.bottom > image_rect.bottom \
             or self.rect.top < image_rect.top:
                self.rect.topleft = image_rect.topleft
                self.rect.size = (0,0)
             self.rect.x -= image_pos[0]
             self.rect.y -= image_pos[1]
             """#capture the whole image if we get nothing
             if not self.capture_sprite(image):
                self.rect.topleft = (0,0)
                self.rect.width = image.get_width() - 1
                self.rect.height = image.get_height() - 1
                self.capture_sprite(image)"""
             self.capture_sprite(image)
             self.rect.x += image_pos[0]
             self.rect.y += image_pos[1]
             recr_info = self.reset_to_origin(image_pos)
             self.rect_info = self.font.render("x:{}  y:{}  w:{}  h:{}".format(*recr_info), True, YELLOW)
        if event.type == MOUSEMOTION:
           if self.gripping:
              self.rect.width = event.pos[0]-self.rect.x
              self.rect.height = event.pos[1]-self.rect.y

    def capture_sprite(self, image):
        
        capturing_rect = Rect([0, 0, 0, 0])
        alpha_color = image.get_at(self.rect.topleft)
        other_color = False
        
        old_x = self.rect.x + self.rect.width
        for y in range(self.rect.y, self.rect.y + self.rect.height, 1):
            for x in range(self.rect.x, self.rect.x + self.rect.width, 1):
                if image.get_at((x,y)) != alpha_color:
                   other_color = True
                   if x < old_x:
                      old_x = x
                      capturing_rect.x = x
                      break
                    
        if other_color:
           old_x = self.rect.x
           for y in range(self.rect.y, self.rect.y + self.rect.height, 1):
               for x in range(self.rect.x + self.rect.width, self.rect.x-1, -1):
                   if image.get_at((x,y)) != alpha_color:
                      if x > old_x :
                         old_x = x 
                         if x > self.rect.x:
                            capturing_rect.width = (x+1) - capturing_rect.x
                         break
                        
           old_y = self.rect.y + self.rect.height             
           for x in range(self.rect.x, self.rect.x + self.rect.width, 1):
               for y in range(self.rect.y, self.rect.y + self.rect.height, 1):
                   if image.get_at((x,y)) != alpha_color:
                      if y < old_y:
                         old_y = y
                         capturing_rect.y = y
                         break
                        
           old_y = self.rect.y             
           for x in range(self.rect.x, self.rect.x + self.rect.width, 1):
               for y in range(self.rect.y + self.rect.height, self.rect.y-1, -1):
                   if image.get_at((x,y)) != alpha_color:
                      if y > old_y :
                         old_y = y 
                         if y > self.rect.y:
                            capturing_rect.height = (y+1) - capturing_rect.y
                         break
                        
           self.rect = capturing_rect
        #return other_color
    
    def reset_to_origin(self, image_pos):
        x = self.rect.x - image_pos[0]
        y = self.rect.y - image_pos[1]
        x = x / self.scale
        y = y / self.scale
        width = self.rect.width / self.scale
        height = self.rect.height / self.scale
        return Rect([x, y, width, height])

    def scale_rect(self, scale, image_pos):
        self.rect.x -= image_pos[0]
        self.rect.y -= image_pos[1]
        self.rect.x = self.rect.x/self.scale
        self.rect.y = self.rect.y/self.scale
        self.rect.width=self.rect.width/self.scale
        self.rect.height=self.rect.height/self.scale
        self.rect.x = self.rect.x*scale
        self.rect.y = self.rect.y*scale
        self.rect.width=self.rect.width*scale
        self.rect.height=self.rect.height*scale
        self.rect.x += image_pos[0]
        self.rect.y += image_pos[1]
        self.scale = scale

    def cycle_colors(self):
        self.timer += 1
        if self.timer >= self.color_max_time:
           self.timer = 0 
           self.color_index += self.increment
           if self.color_index >= self.colors_lenght:
              self.color_index = self.colors_lenght
              self.increment *= -1
           elif self.color_index <= 0:
              self.color_index = 0
              self.increment *= -1              
           self.color = self.colors[self.color_index]
        
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, self.line_thickness)
        surface.blit(self.rect_info, (5, 450))


def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("Sprite Captor")
    #clock
    clock=pygame.time.Clock()
    #font
    font=pygame.font.SysFont('Arial', 30)

    #images
    original_image=pygame.image.load(SPRITE_SHEET).convert()
    image=original_image.copy()
    #variables
    global image_transparency, alpha_color
    image_transparency = False
    alpha_color = original_image.get_at((0, 150))
    image_pos=[0,0]
    image_original_move_speed = 5
    image_move_speed = image_original_move_speed
    scale=1
    scale_max=7
    sprite_captor=Sprite_Captor()
    sprites = {'rect':[], 'axis_shift':[], 'offense_box':[], 'defense_box':[]}
    animations = [[] for i in range(50)]
    try:
        with open(SPRITE_FILE_NAME, 'r') as file:
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
                 
        with open(ANIMATION_FILE_NAME, 'r') as file:
             data=file.read()
             data=data.split(',')
             del(data[-1])
             for i in range(len(data)):
                 data[i] = data[i].split(" ")
                 if data[i][0] == "-1":
                    del(data[i][0])
                 for j in range(len(data[i])):
                     data[i][j] = int(data[i][j])
             animations = data
    except FileNotFoundError:
        pass
    message = " "
    message_time = 0
    text=font.render(message, True, YELLOW)
    text_pos = [0,0]

    #pygame.key.set_repeat(400, 30)

    while True:
        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #keyboard commands    
            if event.type == KEYDOWN:
                if event.key == K_i:
                   #scale up the image and the sprite captor 
                   if scale <  scale_max:
                      scale+=1
                   else:
                      scale = scale_max
                   image_move_speed = image_original_move_speed * scale
                   image = scale_image(original_image, scale)
                   sprite_captor.scale_rect(scale, image_pos)
                elif event.key == K_j:
                   #scale down the image and the sprite captor 
                   if scale >  1:
                      scale -= 1
                   else:
                      scale = 1
                   image_move_speed = image_original_move_speed * scale
                   image = scale_image(original_image, scale)
                   sprite_captor.scale_rect(scale, image_pos)
                elif event.key == K_o:
                    #reset the image's and the sprite captor's positions to origin
                    sprite_captor.rect.x-=image_pos[0]
                    sprite_captor.rect.y-=image_pos[1]
                    image_pos[0]=0
                    image_pos[1]=0
                elif event.key == K_r:
                    #reset the image's and the sprite captor's positions and sizes to origin
                    sprite_captor.rect = sprite_captor.reset_to_origin(image_pos)
                    sprite_captor.scale = 1
                    image_pos[0]=0
                    image_pos[1]=0
                    image = scale_image(original_image, 1)
                    scale = 1
                    image_move_speed = image_original_move_speed
                elif event.key == K_c:
                    #center the captured sprite
                    move_x = HALF_SCREEN_WIDTH-sprite_captor.rect.centerx
                    move_y = HALF_SCREEN_HEIGHT-sprite_captor.rect.centery
                    sprite_captor.rect.x += move_x
                    sprite_captor.rect.y += move_y
                    image_pos[0] += move_x
                    image_pos[1] += move_y
                elif event.key == K_e:
                    #add the captured sprite's position and size to the list
                    x, y, w, h = sprite_captor.reset_to_origin(image_pos)
                    sprites['rect'].append([x, y, w, h])
                    sprites['axis_shift'].append([-int(w / 2), -h])
                    sprites['offense_box'].append([0, 0, 0, 0])
                    sprites['defense_box'].append([0, 0, 0, 0])
                    message = str(len(sprites['rect']))+" sprite added to the list"
                    message_time = 50
                    text=font.render(message, True, YELLOW)
                    text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                    text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
                elif event.key == K_RETURN:
                     #save changes to a file
                     save_data(sprites, animations) 
                     message = "changes saved"
                     message_time = 50
                     text = font.render("changes saved", True, YELLOW)
                     text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                     text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)                    
                elif event.key == K_s:
                    #enter the sprite editor
                    sprite_editor(screen, sprites, animations, original_image)
                    message = "Sprite Captor"
                    text=font.render(message, True, YELLOW)
                    text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                    text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
                    message_time = 50
                elif event.key == K_x:
                    #enter the animation editor
                    animation_editor(screen, sprites, animations, original_image)
                    message = "Sprite Captor"
                    text=font.render(message, True, YELLOW)
                    text_pos[0] = HALF_SCREEN_WIDTH - int(text.get_width() / 2)
                    text_pos[1] = HALF_SCREEN_HEIGHT - int(text.get_height() / 2)
                    message_time = 50
     
                    
            #update the sprite captor        
            sprite_captor.update(event, image, image_pos)
        sprite_captor.cycle_colors()  

                   
        #move the image and the sprite captor
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
           image_pos[1]-=image_move_speed
           sprite_captor.rect.y-=image_move_speed
        elif keys[K_DOWN]:
           image_pos[1]+=image_move_speed
           sprite_captor.rect.y+=image_move_speed
        if keys[K_LEFT]:
           image_pos[0]-=image_move_speed
           sprite_captor.rect.x-=image_move_speed
        elif keys[K_RIGHT]:
           image_pos[0]+=image_move_speed
           sprite_captor.rect.x+=image_move_speed


        #draw everything
        screen.fill(BLACK)
        screen.blit(image, image_pos)
        sprite_captor.draw(screen)
        if message_time > 0:
           message_time -= 1
           if message_time < 0:
              message_time = 0
           text=font.render(message, True, YELLOW)
           screen.blit(text, text_pos)           
        pygame.display.flip()

if __name__ == "__main__":
    main()
