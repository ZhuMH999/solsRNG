import pygame
from snippets.constants import EFFECTS, EFFECT_SIZE

def split_sprites():
    sprites = []

    for i in range(EFFECT_SIZE[1]):
        for j in range(EFFECT_SIZE[0]):
            sprites.append(_get_sprite(EFFECTS, j * EFFECT_SIZE[2], i * EFFECT_SIZE[2], EFFECT_SIZE[2], EFFECT_SIZE[2]))

    return sprites

def _get_sprite(sheet, x, y, w, h):
    sprite = pygame.Surface((w, h), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, w, h))
    return sprite