import pygame
import os
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
width, height = 500, 500
image_size = 100, 100
size = width, height
screen = pygame.display.set_mode(size)
coords = pygame.sprite.Group()


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb2.png")
    image = pygame.transform.scale(image, image_size)
    image_boom = load_image("boom.png", -1)
    image_boom = pygame.transform.scale(image_boom, image_size)

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - image_size[0])
        self.rect.y = random.randrange(height - image_size[0])
        while pygame.sprite.spritecollideany(self, coords):
            self.rect.x = random.randrange(width - image_size[0])
            self.rect.y = random.randrange(height - image_size[0])
        self.add(coords)

    def update(self, *args):
        # self.rect = self.rect.move(random.randrange(3) - 1, random.randrange(3) - 1)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom

    def get_event(self):
        if self.rect.collidepoint(event.pos):
            self.image = self.image_boom


all_sprites = pygame.sprite.Group()
bomb_image = load_image("bomb2.png")
bomb_image = pygame.transform.scale(bomb_image, image_size)

for _ in range(10):
    Bomb(all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                bomb.get_event()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
