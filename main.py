import pygame
import asyncio
from model import Model
from visuals import Visuals
from snippets.constants import WIDTH, HEIGHT

pygame.init()

class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.model = Model()
        self.clock = pygame.time.Clock()
        self.visuals = Visuals(self.win, self.model, self.clock)
        pygame.display.set_caption('Sol\'s RNG in Python')

    async def main(self):
        self.visuals.initialize_window()

        running = True
        while running:
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.model.check_where_interact(x, y, self.visuals, event.button)

            self.visuals.draw(x, y)
            self.model.handle_game_tick(self.visuals)

            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)

        pygame.quit()

c = Controller()
asyncio.run(c.main())