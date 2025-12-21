import pygame
from snippets.constants import GRAVITY, PLAYER_SPEED, JUMP_VELOCITY, WIDTH

class Player:
    def __init__(self):
        self.player_width = 28
        self.player_height = 40

        self.vel_y = 0
        self.on_ground = False

    def update(self, keys, model, world):
        dx = 0

        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            dx = PLAYER_SPEED

        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = JUMP_VELOCITY

        self.vel_y += GRAVITY
        if self.vel_y > 12:
            self.vel_y = 12

        dy = self.vel_y

        self._move(dx, dy, model, world.platforms)

        model.camera_x = model.player_x - WIDTH // 2
        model.camera_y = 0

    def _move(self, dx, dy, model, platforms):
        self.on_ground = False
        player_rect = pygame.Rect(model.player_x, model.player_y,
                                  self.player_width, self.player_height)

        # Horizontal collision
        player_rect.x += dx
        for p in platforms:
            if player_rect.colliderect(p):
                if dx > 0:
                    player_rect.right = p.left
                elif dx < 0:
                    player_rect.left = p.right

        # Vertical collision
        player_rect.y += dy
        for p in platforms:
            if player_rect.colliderect(p):
                if dy > 0:
                    player_rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:
                    player_rect.top = p.bottom
                    self.vel_y = 0

        model.player_x = player_rect.x
        model.player_y = player_rect.y