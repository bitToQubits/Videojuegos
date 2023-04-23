import pygame

# Initialize pygame
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# Set up the screen
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("My Game")

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
            
    
    # Update the game
    
    # Draw the screen
    screen.fill((255, 255, 255))
    pygame.display.flip()

# Quit pygame
pygame.quit()

