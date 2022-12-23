import pygame as p
import threading
from backtracking import *

WIDTH = HEIGHT = 512
rect_size = HEIGHT / size
FPS = 15
QUEEN = p.image.load("bQ.png")
QUEEN = p.transform.smoothscale(QUEEN, (rect_size, rect_size))


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for row in range(size):
        for column in range(size):
            color = colors[(row+column) % 2]
            p.draw.rect(screen, color, p.Rect(column * rect_size,
                        row * rect_size, rect_size, rect_size))
            if board[row][column]:
                screen.blit(QUEEN, p.Rect(column*rect_size,
                            row*rect_size, rect_size, rect_size))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    QUEEN = p.image.load("bQ.png").convert_alpha()
    QUEEN = p.transform.scale(QUEEN, (rect_size, rect_size))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(FPS)
        p.display.flip()
        drawBoard(screen)


if __name__ == "__main__":
    main()
