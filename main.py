import pygame
from pygame.locals import *
import random
from sprites.bird import Bird
from sprites.pipe import Pipe
from sprites.button import Button

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# define font
font = pygame.font.SysFont("Bauhaus 93", 60)

# define colour
white = (255, 255, 255)

# game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frquency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frquency
score = 0
pass_pipe = False

# load images
bg = pygame.image.load("./img/bg.png")
ground_img = pygame.image.load("./img/ground.png")
button_img = pygame.image.load("./img/restart.png")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


# sprites
flappy = Bird(100, int(screen_height / 2))

# groups
bird_group = pygame.sprite.Group()
bird_group.add(flappy)

pipe_group = pygame.sprite.Group()

# restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:

    clock.tick(fps)

    # Draw background
    screen.blit(bg, (0, 0))

    # draw amd update bird
    bird_group.draw(screen)
    bird_group.update(flying, game_over)

    # draw amd update pipe
    pipe_group.draw(screen)

    # draw the ground
    screen.blit(ground_img, (ground_scroll, 768))

    # check the score
    if len(pipe_group) > 0:
        if (
            bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right
            and pass_pipe == False
        ):
            pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    # look for collision
    group_collision = pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
    if group_collision or flappy.rect.top < 0:
        game_over = True

    # check if bird has hit the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        # generate the pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frquency:
            pipe_height = random.randint(-100, 100)

            btm_pipe = Pipe(
                screen_width, int(screen_height / 2) + pipe_height, -1, pipe_gap
            )
            top_pipe = Pipe(
                screen_width, int(screen_height / 2) + pipe_height, 1, pipe_gap
            )
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update(scroll_speed)

    # check for game over and reset
    if game_over == True:
        if button.draw(screen) == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and flying == False
            and game_over == False
        ):
            flying = True

    pygame.display.update()

pygame.quit()
