from tkinter.messagebox import YES
import pygame

class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
            
pygame.init()

pygame.display.set_caption("Tetris")

game = Tetris(20, 10)

screen = pygame.display.set_mode((500,600))

screen.fill((0,0,0))

do = True

time = pygame.time.Clock()

while do:
    game.__init__(20 , 10)
    pygame.display.flip()
    time.tick(25)
    
