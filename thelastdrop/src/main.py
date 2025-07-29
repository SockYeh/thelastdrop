import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the game window

WIDTH = 1600
HEIGHT = 800
MOVE_SPEED = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Hello Pygame")

#load sprite sheet
sprite_sheet = pygame.image.load(os.path.join("thelastdrop", "assets", "prototype_character.png")).convert_alpha()
shadow_sprite = pygame.image.load(os.path.join("thelastdrop", "assets", "prototype_character_shadow.png")).convert_alpha()

sheet_width, sheet_height = sprite_sheet.get_size()
sprite_width = sheet_width // 4   # since 4 columns
sprite_height = sheet_height // 12  # since 10 rows

shadow_sprite_scaled = pygame.transform.scale(shadow_sprite, (sprite_width * 3, sprite_height * 3))

def get_sprite(sheet, row, col):
    character = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
    image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), character)
    return image

idle_frames = [get_sprite(sprite_sheet, 0, col) for col in range(2)]               #idle frames
walk_up = [get_sprite(sprite_sheet, 5, col) for col in range(4)]                   #walking up frames
walk_down = [get_sprite(sprite_sheet, 3, col) for col in range(4)]                 #walking down frames
walk_right = [get_sprite(sprite_sheet, 4, col) for col in range(4)]                #walking right
walk_left = [pygame.transform.flip(frame, True, False) for frame in walk_right]    #walking left

current_frame = 0
animation_speed = 100  # milliseconds per frame (0.3 seconds)
last_update = pygame.time.get_ticks()

anim = walk_right

x=100
y=100

# Game loop
running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if now - last_update > animation_speed:
        current_frame = (current_frame + 1) % len(anim)
        last_update = now

    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
       anim = walk_left
       x-= MOVE_SPEED
    elif keys[pygame.K_RIGHT]:
        anim = walk_right
        x += MOVE_SPEED
    elif keys[pygame.K_UP]:
       anim = walk_up
       y -= MOVE_SPEED
    elif keys[pygame.K_DOWN]:
        anim = walk_down
        y += MOVE_SPEED


    sprite = pygame.transform.scale(anim[current_frame], (sprite_width*3,sprite_height*3))
    screen.fill((255, 255, 255))  # Fill screen with white

    screen.blit(shadow_sprite_scaled, (x, y)) 

    screen.blit(sprite, (x, y))  # Draw the sprite at position (x and y)
    pygame.display.update()  # Update the screen    

    clock.tick(60) 
    

# Quit Pygame
pygame.quit()