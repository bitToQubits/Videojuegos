import pygame


pygame.init()
pygame.mixer.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teclado para el arcade")


font = pygame.font.SysFont('comicsansms', 24)


#key_sound = pygame.mixer.Sound('key_sound.wav')


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
buttons = letters + numbers + [' ', 'BORRAR']

button_rects = {}
x, y = 50, 50
for button in buttons:
    text = font.render(button, True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = (x, y)
    button_rects[button] = rect
    x += 50
    if x > 750:
        x = 50
        y += 50


cursor_position = 0


def draw_screen():
    for button in buttons:
        if button == 'BORRAR':
            text = font.render(button, True, (255, 0, 0))
        else:
            text = font.render(button, True, (255, 255, 255))
        rect = button_rects[button]
        screen.blit(text, rect)
    pygame.display.update()


running = True
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cursor_position -= 1
                if cursor_position < 0:
                    cursor_position = len(buttons) - 1
            elif event.key == pygame.K_RIGHT:
                cursor_position += 1
                if cursor_position >= len(buttons):
                    cursor_position = 0
            elif event.key == pygame.K_UP:
                cursor_position -= 10
                if cursor_position < 0:
                    cursor_position = len(buttons) - 1
            elif event.key == pygame.K_DOWN:
                cursor_position += 10
                if cursor_position >= len(buttons):
                    cursor_position = 0
            elif event.key == pygame.K_RETURN:
                selected_button = buttons[cursor_position]
