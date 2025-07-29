import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the game window

WIDTH = 1600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello Pygame")

#load sprite sheet
sprite_sheet = pygame.image.load(os.path.join("thelastdrop", "assets", "prototype_character.png")).convert_alpha()

sprite_width = 16
sprite_height = 16

def get_sprite(sheet, row, col):
    rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
    image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    return image

idle_frames = [get_sprite(sprite_sheet, 0, col) for col in range(2)]               #idle frames
walk_up = [get_sprite(sprite_sheet, 6, col) for col in range(4)]                   #walking up frames
walk_down = [get_sprite(sprite_sheet, 4, col) for col in range(4)]                 #walking down frames
walk_right = [get_sprite(sprite_sheet, 5, col) for col in range(4)]                #walking right
walk_left = [pygame.transform.flip(frame, True, False) for frame in walk_right]    #walking left
 
sprite = walk_down[0]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fill screen with white
    screen.blit(sprite, (100, 100))  # Draw the sprite at position (100, 100)
    pygame.display.update()  # Update the screen

# Quit Pygame
pygame.quit()