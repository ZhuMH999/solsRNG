import pygame
from model import Model
from visuals import Visuals
from constants import WIDTH, HEIGHT

pygame.init()

class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.model = Model()
        self.visuals = Visuals(self.win, self.model)
        pygame.display.set_caption('Sol\'s RNG in Python')

    def run(self):
        self.visuals.initialize_window()

        running = True
        while running:
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.model.check_where_clicked(x, y)

            self.visuals.draw(x, y)

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    c = Controller()
    c.run()