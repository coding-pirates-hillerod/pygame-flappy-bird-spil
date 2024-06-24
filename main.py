import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# game variables
ground_scroll = 0
scroll_speed = 4

# load images
bg = pygame.image.load("./img/bg.png")
ground_img = pygame.image.load("./img/ground.png")


# flappy bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.vel = 0

        # load all flappy bird images for animation
        for num in range(1, 4):
            img = pygame.image.load(f"./img/bird{num}.png")
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # handle velocity change
        self.vel += 0.5
        if self.vel > 8:
            self.vel = 8

        if self.rect.bottom < 768:
            self.rect.y += int(self.vel)

        # handle the animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

run = True
while run:

    clock.tick(fps)

    # Draw background
    screen.blit(bg, (0, 0))

    # draw bird
    bird_group.draw(screen)

    # update bird
    bird_group.update()

    # Draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 768))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
