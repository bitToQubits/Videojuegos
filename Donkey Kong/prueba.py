'''import pygame

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Hello World")
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

while True:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            break
        if event.type == pygame.JOYBUTTONUP:
            print(event)'''