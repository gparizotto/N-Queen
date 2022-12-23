import numpy as np

size = 15
board = np.full((size, size), False, object)


def try_position(line, column):
    # check if a queen is attacking the line
    for i in range(size):
        if i != line and board[i][column]:
            return False
    # check if a queen is attacking the column
    for i in range(size):
        if i != column and board[line][i]:
            return False
    # check if a queen is attacking the principal diagonal
    line_aux = line
    column_aux = column
    while line_aux < size and column_aux < size:
        if board[line_aux][column_aux]:
            return False
        line_aux += 1
        column_aux += 1
    line_aux = line
    column_aux = column
    while line_aux >= 0 and column_aux >= 0:
        if board[line_aux][column_aux]:
            return False
        line_aux -= 1
        column_aux -= 1
    # check if a queen is attacking the secondary diagonal
    line_aux = line
    column_aux = column
    while line_aux >= 0 and column_aux < size:
        if board[line_aux][column_aux]:
            return False
        line_aux -= 1
        column_aux += 1
    line_aux = line
    column_aux = column
    while line_aux < size and column_aux >= 0:
        if board[line_aux][column_aux]:
            return False
        line_aux += 1
        column_aux -= 1
    # if there isn't any attack, mark the position as true (queen placed) and return true
    board[line][column] = True
    return True

def solution(line, column, previous_line, previous_column, number_of_queens):
    for i in range(line, size):
        check = False  # checks if there's a line without any queen -> can't be a solution
        for j in range(column, size):
            if try_position(i, j):  # try to place the queen
                check = True
                ans = solution(i+1, 0, i, j, number_of_queens + 1)
                if not ans:
                    check = False
                elif ans == 2:
                    return 2
        if not check:
            break
    if number_of_queens != size:  # if you can't place any more queens and there isn't N queens on the board, return false
        board[previous_line][previous_column] = False
        return False
    return 2

var = solution(0, 0, 0, 0, 0)
if var:
    print(board)
else:
    print("No solution found!")    
    
