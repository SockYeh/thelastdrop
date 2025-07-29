import pygame, os , math

pygame.init()
pygame.font.init()

FPS = 60
MOVE_SPEED = 5


FONT = pygame.font.SysFont("comicsans", 30)

CHAR_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "char_temp.jpg"))
MENU_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "bg.png"))
PIPE_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "pipe.png"))
BOTTLE_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "bottle.png"))
BG_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "title.png"))


WIDTH = 1600
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("The Last Drop")


# load sprite sheet
sprite_sheet = pygame.image.load(
    os.path.join("thelastdrop", "assets", "prototype_character.png")
).convert_alpha()
shadow_sprite = pygame.image.load(
    os.path.join("thelastdrop", "assets", "prototype_character_shadow.png")
).convert_alpha()

sheet_width, sheet_height = sprite_sheet.get_size()
sprite_width = sheet_width // 4  # since 4 columns
sprite_height = sheet_height // 12  # since 10 rows

shadow_sprite_scaled = pygame.transform.scale(
    shadow_sprite, (sprite_width * 3, sprite_height * 3)
)


def get_sprite(sheet, row, col):
    character = pygame.Rect(
        col * sprite_width, row * sprite_height, sprite_width, sprite_height
    )
    image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), character)
    return image


character = pygame.Rect(100, 100, sprite_width, sprite_height)


def draw_bottle(x, y):
    bottle_rect = pygame.Rect(x, y, 50, 50)
    SCREEN.blit(
        pygame.transform.scale(BOTTLE_SPRITE, (50, 50)), (bottle_rect.x, bottle_rect.y)
    )
    return bottle_rect


def draw_window():
    global bottles


SCORE = 0


def draw_score(score):
    global SCORE
    SCORE += score
    score_text = FONT.render(f"Score: {SCORE}", 1, (255, 255, 255))
    SCREEN.blit(score_text, (10, 10))


bottles = []


def handle_collision(character, bottles):
    for bottle in bottles:
        if character.colliderect(bottle):
            bottles.remove(bottle)
            return True
    return False


idle_frames = [get_sprite(sprite_sheet, 0, col) for col in range(4)]  # idle frames
walk_up = [get_sprite(sprite_sheet, 5, col) for col in range(4)]  # walking up frames
walk_down = [
    get_sprite(sprite_sheet, 3, col) for col in range(4)
]  # walking down frames
walk_right = [get_sprite(sprite_sheet, 4, col) for col in range(4)]  # walking right
walk_left = [
    pygame.transform.flip(frame, True, False) for frame in walk_right
]  # walking left

current_frame = 0
animation_speed = 60  # milliseconds per frame
last_update = pygame.time.get_ticks()

anim = idle_frames

def draw_menu():
    SCREEN.blit(pygame.transform.scale(scaled_bg, (1800, 1000)), (-100, -150))
    button_text = FONT.render("Click Here to Start", 1, (255, 255, 255))
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT*0.85))
    pygame.draw.rect(SCREEN, (50, 50, 250), button_rect.inflate(20, 20))
    SCREEN.blit(button_text, button_rect)
    pygame.display.update()
    return button_rect

game_state = "menu"
running = True
button_rect = None

# Game loop
running = True
bottles.append(draw_bottle(300, 300))
while running:
    now = pygame.time.get_ticks()
    pulsate_speed = 0.005  # change this for faster/slower pulsation
    scale_factor = 1 + 0.9 * math.sin(now * pulsate_speed)  # oscillates between 
    scaled_width = int(WIDTH * scale_factor)
    scaled_height = int(HEIGHT * scale_factor)
    scaled_bg = pygame.transform.scale(BG_SPRITE, (scaled_width, scaled_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect and button_rect.collidepoint(event.pos):
                    game_state = "game"
        elif game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC to go back to menu
                    game_state = "menu"

    keys = pygame.key.get_pressed()

    if game_state == "menu":
        button_rect = draw_menu()

    elif game_state == "game":
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            anim = walk_left
            character.x -= MOVE_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            anim = walk_right
            character.x += MOVE_SPEED
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            anim = walk_up
            character.y -= MOVE_SPEED
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            anim = walk_down
            character.y += MOVE_SPEED
        else:
            anim = idle_frames

        if now - last_update > animation_speed:
            current_frame = (current_frame + 1) % len(anim)
            last_update = now

        sprite = pygame.transform.scale(
            anim[current_frame], (sprite_width * 3, sprite_height * 3)
        )

        SCREEN.blit(pygame.transform.scale(MENU_SPRITE, (1600, 800)), (0, 0))

        SCREEN.blit(shadow_sprite_scaled, (character.x, character.y))
        SCREEN.blit(
            sprite, (character.x, character.y)
        )  # Draw the sprite at position (x and y)

        draw_score(0)  # Placeholder for score, can be updated later
        for bottle in bottles:
            SCREEN.blit(
                pygame.transform.scale(BOTTLE_SPRITE, (50, 50)), (bottle.x, bottle.y)
            )
        if handle_collision(character, bottles):
            print("Collision detected!")
            draw_score(10)
            try:
                bottles.remove(bottle)
            except ValueError:
                print("Bottle already removed or not found.")
            # remove bottle from SCREEN
        pygame.display.set_caption(f"The Last Drop - Score: {SCORE}")
        pygame.display.update()  # Update the SCREEN

        clock.tick(60)


# Quit Pygame
pygame.quit()
