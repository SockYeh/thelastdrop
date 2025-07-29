import pygame, os

pygame.init()
pygame.font.init()

FPS = 60
MOVE_SPEED = 25


FONT = pygame.font.SysFont("comicsans", 30)
CHAR_SPRITE = pygame.image.load(os.path.join("thelastdrop", "assets", "char_temp.jpg"))
BG = pygame.image.load(os.path.join("thelastdrop", "assets", "bg.jpg"))


SCREEN = pygame.display.set_mode((1600, 800))
pygame.display.set_caption("Hello Pygame")

character = pygame.Rect(100, 100, 50, 50)


def draw_window():
    SCREEN.blit(pygame.transform.scale(BG, (1600, 800)), (0, 0))
    SCREEN.blit(
        pygame.transform.scale(CHAR_SPRITE, (50, 50)), (character.x, character.y)
    )
    pygame.display.update()


running = True
while running:
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_LEFT]:
        if character.x - MOVE_SPEED < 0:
            character.x = 0
            continue
        character.x -= MOVE_SPEED
    elif keys[pygame.K_RIGHT]:
        if character.x + MOVE_SPEED > 1600 - 50:
            character.x = 1600 - 50
            continue
        character.x += MOVE_SPEED
    elif keys[pygame.K_UP]:
        if character.y - MOVE_SPEED < 0:
            character.y = 0
            continue
        character.y -= MOVE_SPEED
    elif keys[pygame.K_DOWN]:
        if character.y + MOVE_SPEED > 800 - 50:
            character.y = 800 - 50
            continue
        character.y += MOVE_SPEED
    draw_window()

pygame.quit()
