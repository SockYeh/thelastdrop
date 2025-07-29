import pygame, os, math, random

pygame.init()
pygame.font.init()

FPS = 60
MOVE_SPEED = 5
WIDTH = 1600
HEIGHT = 800

FONT = pygame.font.SysFont("comicsans", 50)

# Load assets
CHAR_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "char_temp.jpg"))
BACKGROUND = pygame.image.load(os.path.join("thelastdrop", "assets", "bg.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
PIPE_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "pipe.png"))
BOTTLE_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "bottle.png"))
BG_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "title.png"))
pygame.mixer.music.load(os.path.join("thelastdrop", "assets", "watermusic.mp3"))

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("The Last Drop")

# Load sprite sheet
sprite_sheet = pygame.image.load(
    os.path.join("thelastdrop", "assets", "prototype_character.png")
).convert_alpha()
shadow_sprite = pygame.image.load(
    os.path.join("thelastdrop", "assets", "prototype_character_shadow.png")
).convert_alpha()

sheet_width, sheet_height = sprite_sheet.get_size()
sprite_width = sheet_width // 4
sprite_height = sheet_height // 12

shadow_sprite_scaled = pygame.transform.scale(
    shadow_sprite, (sprite_width * 3, sprite_height * 3)
)


def get_sprite(sheet, row, col):
    rect = pygame.Rect(
        col * sprite_width, row * sprite_height, sprite_width, sprite_height
    )
    image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    return image


character = pygame.Rect(200, 300, sprite_width, sprite_height)


def draw_bottle(x, y):
    bottle_rect = pygame.Rect(x, y, 50, 50)
    return bottle_rect


def spawn_random_bottles(count):
    bottles = []
    for _ in range(count):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        bottles.append(draw_bottle(x, y))
    return bottles


SCORE = 0


def draw_score(score):
    global SCORE
    SCORE += score
    score_text = FONT.render(f"Score: {SCORE}", 1, (255, 255, 255))
    SCREEN.blit(score_text, (1100 - len(f"Score: {SCORE}") * 50, 10))


def handle_collision(character, bottles):
    for bottle in bottles[:]:
        if character.colliderect(bottle):
            bottles.remove(bottle)
            return True
    return False


# Animation frames
idle_frames = [get_sprite(sprite_sheet, 0, col) for col in range(4)]
walk_up = [get_sprite(sprite_sheet, 5, col) for col in range(4)]
walk_down = [get_sprite(sprite_sheet, 3, col) for col in range(4)]
walk_right = [get_sprite(sprite_sheet, 4, col) for col in range(4)]
walk_left = [pygame.transform.flip(frame, True, False) for frame in walk_right]

current_frame = 0
animation_speed = 60
last_update = pygame.time.get_ticks()
anim = idle_frames

# Game objects
bottles = spawn_random_bottles(5)
cameras = [
    {
        "pos": (400, 200),
        "beam_length": 180,
        "beam_angle": 60,
        "rotation_speed": 1.2,
        "angle": 0,
        "color": (255, 0, 0, 80),  # Red
    },
    {
        "pos": (800, 400),
        "beam_length": 150,
        "beam_angle": 45,
        "rotation_speed": -0.8,
        "angle": 90,
        "color": (0, 255, 0, 80),  # Green
    },
    {
        "pos": (1200, 300),
        "beam_length": 200,
        "beam_angle": 50,
        "rotation_speed": 1.5,
        "angle": 180,
        "color": (0, 0, 255, 80),  # Blue
    },
    {
        "pos": (600, 600),
        "beam_length": 160,
        "beam_angle": 55,
        "rotation_speed": -1.0,
        "angle": 270,
        "color": (255, 255, 0, 80),  # Yellow
    },
    {
        "pos": (300, 500),
        "beam_length": 140,
        "beam_angle": 40,
        "rotation_speed": 0.9,
        "angle": 45,
        "color": (255, 0, 255, 80),  # Magenta
    },
    {
        "pos": (1000, 150),
        "beam_length": 170,
        "beam_angle": 50,
        "rotation_speed": -1.3,
        "angle": 315,
        "color": (0, 255, 255, 80),  # Cyan
    },
    {
        "pos": (1400, 600),
        "beam_length": 130,
        "beam_angle": 35,
        "rotation_speed": 1.8,
        "angle": 135,
        "color": (255, 128, 0, 80),  # Orange
    },
    {
        "pos": (100, 100),
        "beam_length": 120,
        "beam_angle": 65,
        "rotation_speed": -0.6,
        "angle": 225,
        "color": (128, 0, 255, 80),  # Purple
    },
]


def point_in_cone(px, py, apex, p1, p2):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign((px, py), apex, p1) < 0.0
    b2 = sign((px, py), p1, p2) < 0.0
    b3 = sign((px, py), p2, apex) < 0.0
    return b1 == b2 == b3


def reset_game():
    global SCORE, bottles
    character.x = 200
    character.y = 300
    SCORE = 0
    bottles = spawn_random_bottles(5)


def draw_menu():
    SCREEN.blit(pygame.transform.scale(scaled_bg, (1800, 1000)), (-100, -150))
    button_text = FONT.render("Click Here to Start", 1, (255, 255, 255))
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT * 0.85))
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
    pulsate_speed = 0.0025  # change this for faster/slower pulsation
    scale_factor = 1 + 0.9 * math.sin(now * pulsate_speed)  # oscillates between
    scaled_width = int(WIDTH * scale_factor)
    scaled_height = int(HEIGHT * scale_factor)
    scaled_bg = pygame.transform.scale(BG_SPRITE, (scaled_width, scaled_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "menu":
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        else:  # game state
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
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
        keys = pygame.key.get_pressed()

        # Character movement and animation
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

        # Keep character on screen
        character.x = max(0, min(character.x, WIDTH - sprite_width * 3))
        character.y = max(0, min(character.y, HEIGHT - sprite_height * 3))

        # Update animation
        if now - last_update > animation_speed:
            current_frame = (current_frame + 1) % len(anim)
            last_update = now

        sprite = pygame.transform.scale(
            anim[current_frame], (sprite_width * 3, sprite_height * 3)
        )

        # Draw BACKGROUND
        SCREEN.blit(BACKGROUND, (0, 0))

        # Draw all camera vision cones
        player_center = (
            character.x + sprite_width * 1.5,
            character.y + sprite_height * 1.5,
        )

        caught_by_camera = False
        for camera in cameras:
            # Update camera angle
            camera["angle"] = (camera["angle"] + camera["rotation_speed"]) % 360
            start_angle_rad = math.radians(camera["angle"] - camera["beam_angle"] / 2)
            end_angle_rad = math.radians(camera["angle"] + camera["beam_angle"] / 2)

            cone_points = [
                camera["pos"],
                (
                    camera["pos"][0]
                    + camera["beam_length"] * math.cos(start_angle_rad),
                    camera["pos"][1]
                    + camera["beam_length"] * math.sin(start_angle_rad),
                ),
                (
                    camera["pos"][0] + camera["beam_length"] * math.cos(end_angle_rad),
                    camera["pos"][1] + camera["beam_length"] * math.sin(end_angle_rad),
                ),
            ]

            # Draw shadow/outline for vision cone (darker, offset)
            shadow_points = [
                (camera["pos"][0] + 3, camera["pos"][1] + 3),
                (
                    camera["pos"][0]
                    + 3
                    + camera["beam_length"] * math.cos(start_angle_rad),
                    camera["pos"][1]
                    + 3
                    + camera["beam_length"] * math.sin(start_angle_rad),
                ),
                (
                    camera["pos"][0]
                    + 3
                    + camera["beam_length"] * math.cos(end_angle_rad),
                    camera["pos"][1]
                    + 3
                    + camera["beam_length"] * math.sin(end_angle_rad),
                ),
            ]

            # Draw shadow first (behind the main cone)
            shadow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(
                shadow_surface, (0, 0, 0, 60), shadow_points
            )  # Dark shadow
            SCREEN.blit(shadow_surface, (0, 0))

            # Draw main vision cone
            vision_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(vision_surface, camera["color"], cone_points)
            SCREEN.blit(vision_surface, (0, 0))

            # Draw outline for better visibility
            pygame.draw.polygon(SCREEN, (0, 0, 0, 150), cone_points, 2)

            # Check collision with this camera
            if point_in_cone(player_center[0], player_center[1], *cone_points):
                caught_by_camera = True

        # Draw player and shadow
        SCREEN.blit(shadow_sprite_scaled, (character.x, character.y))
        SCREEN.blit(sprite, (character.x, character.y))

        # Draw bottles
        for bottle in bottles:
            SCREEN.blit(
                pygame.transform.scale(BOTTLE_SPRITE, (50, 50)), (bottle.x, bottle.y)
            )

        # Handle bottle collision
        if handle_collision(character, bottles):
            print("Bottle collected!")
            draw_score(10)

        # Check if all bottles collected
        if len(bottles) == 0:
            print("All bottles collected! Spawning new ones...")
            bottles = spawn_random_bottles(5)

        # Draw score
        draw_score(0)

        # Handle camera detection
        if caught_by_camera:
            print("Player caught by camera!")
            reset_game()

        pygame.display.set_caption(f"The Last Drop - Score: {SCORE}")
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
