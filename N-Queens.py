import pygame as p
import sys
import numpy as np
import time
import threading

# pygame window configuration
p.init()
WIDTH = 512
HEIGHT = 550
font = p.font.Font(None, 30)
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("N-Queens")
clock = p.time.Clock()


class NQueens():
    def __init__(self, size, board):
        self.size = size
        self.board = board
        self.rect_size = WIDTH / self.size
        self.sleep = 0.05

    def try_position(self, row, column):
        # check if a queen is attacking the row
        for i in range(self.size):
            if i != row and self.board[i][column]:
                return False
        # check if a queen is attacking the column
        for i in range(self.size):
            if i != column and self.board[row][i]:
                return False
        # check if a queen is attacking the principal diagonal
        row_aux = row
        column_aux = column
        while row_aux >= 0 and column_aux >= 0:
            if self.board[row_aux][column_aux]:
                return False
            row_aux -= 1
            column_aux -= 1
        # check if a queen is attacking the secondary diagonal
        row_aux = row
        column_aux = column
        while row_aux >= 0 and column_aux < self.size:
            if self.board[row_aux][column_aux]:
                return False
            row_aux -= 1
            column_aux += 1
        return True

    def solution(self, row):
        # if row is greater or equal to size, all the queens are placed
        if row >= self.size:
            return True
        # try to put a queen in every column of the row
        for i in range(self.size):
            self.board[row][i] = True
            time.sleep(self.sleep)
            self.board[row][i] = False
            if self.try_position(row, i):
                self.board[row][i] = True
                if self.solution(row + 1):
                    return True
                self.board[row][i] = False


class Board():
    def __init__(self, size):
        self.width = 512
        self.height = 550
        self.size = size
        self.rect_size = WIDTH / self.size
        self.board = np.full((15, 15), False, object)
        queen = p.image.load("bQ.png")
        self.queen = p.transform.smoothscale(
            queen, (self.rect_size, self.rect_size))
        self.buttons = []

    def draw(self):
        queen = p.image.load("bQ.png")
        self.queen = p.transform.smoothscale(
            queen, (self.rect_size, self.rect_size))
        colors = ["white", "dark green"]
        for row in range(self.size):
            for column in range(self.size):
                color = colors[(row + column) % 2]
                p.draw.rect(screen, color, p.Rect(column * self.rect_size,
                            row * self.rect_size, self.rect_size, self.rect_size))
                if self.board[row][column]:
                    screen.blit(self.queen, p.Rect(column*self.rect_size,
                                row*self.rect_size, self.rect_size, self.rect_size))


class Button():
    def __init__(self, text, width, height, color, pos):
        self.pressed = False

        self.rect = p.Rect(pos, (width, height))
        self.color = color

        self.text = text
        self.text_surf = font.render(self.text, self.color, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        p.draw.rect(screen, self.color, self.rect, border_radius=30)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = p.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = "#D74B4B"
            if p.mouse.get_pressed()[0]:
                self.pressed = True
                return True
            elif self.pressed:
                self.pressed = False
        else:
            self.color = "#475F77"
        return False


class Label():
    def __init__(self, width, height, color, pos):
        self.width = width
        self.height = height
        self.color = color
        self.pos = pos

        self.rect = p.Rect((pos), (width, height))

    def draw(self):
        p.draw.rect(screen, self.color, self.rect)


def draw(board, label, buttons, nqueen):
    label.draw()
    board.draw()
    for button in buttons:
        button.draw()


def initialize_buttons(buttons):
    size = 12
    for i in range(12):
        button = Button(str(i+4), WIDTH / size, HEIGHT - WIDTH,
                        "#475F77", (i*(WIDTH / size), 512))
        buttons.append(button)


def change_board():
    chess_board.size = int(button.text)
    chess_board.rect_size = WIDTH / chess_board.size
    nqueen.size = chess_board.size
    nqueen.rect_size = chess_board.rect_size
    chess_board.board.fill(False)


chess_board = Board(8)
nqueen = NQueens(8, chess_board.board)
label = Label(WIDTH, 50, "brown", (0, 511))
buttons = []
initialize_buttons(buttons)

thread = threading.Thread(target=nqueen.solution, args=(0, ))
thread.start()

while (True):
    for event in p.event.get():
        if (event.type == p.QUIT):
            p.quit()
            sys.exit()
    screen.fill("white")
    draw(chess_board, label, buttons, nqueen)
    for button in buttons:
        if button.check_click():
            if thread.is_alive():
                nqueen.sleep = 0
            else:
                nqueen.sleep = 0.05
                thread = threading.Thread(target=nqueen.solution, args=(0, ))
                thread.start()
                change_board()
    p.display.update()
    clock.tick(15)
