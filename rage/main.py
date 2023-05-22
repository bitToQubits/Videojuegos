import pygame
import sys

def _main():
    print("Elison")
    # Initialize Pygame
    pygame.init()

    # Get the dimensions of the display
    screen_info = pygame.display.Info()
    WIDTH = screen_info.current_w
    HEIGHT = screen_info.current_h
    window_size = (WIDTH, HEIGHT)

    # Create the game window
    window = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
    pygame.display.set_caption("Image Display")

    # Load the image
    image_path = "rage/Elison pixel (1).png"  # Replace with the path to your image
    image = pygame.image.load(image_path)

    # Define the Lorem ipsum text
    lorem_ipsum = "Lorem ipsum"

    # Define the font and size for the text
    font = pygame.font.Font(None, 24)
    running = True

    while running:
        print("Elison")
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    import menu
                    menu.main_menu()()

        # Fill the window with a white background
        window.fill((255, 255, 255))

        # Display the image at the center of the window
        image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(image, image_rect)

        # Render the Lorem ipsum text
        text = font.render(lorem_ipsum, True, (0, 0, 0))

        # Position the text below the image
        text_rect = text.get_rect(center=(WIDTH // 2, image_rect.bottom + 50))
        window.blit(text, text_rect)

        # Update the display
        pygame.display.flip()
