import sys
import math

import numpy as np
import pygame


ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    board = np.zeros((6, 7))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid(board, col):
    return board[5][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r][c + 1] == piece and \
                    board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece and board[r + 1][c] == piece and \
                    board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and \
                    board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and \
                    board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def draw_board(board, screen):
    brd = np.flip(board, 0)
    for c in range(COLUMN_COUNT):
        for r in range(1, ROW_COUNT + 1):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if brd[r - 1][c] == 0:
                pygame.draw.circle(screen, BLACK,
                                   (c * SQUARE_SIZE + (SQUARE_SIZE // 2), r * SQUARE_SIZE + (SQUARE_SIZE // 2)), RADIUS)
            elif brd[r - 1][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (c * SQUARE_SIZE + (SQUARE_SIZE // 2), r * SQUARE_SIZE + (SQUARE_SIZE // 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW,
                                   (c * SQUARE_SIZE + (SQUARE_SIZE // 2), r * SQUARE_SIZE + (SQUARE_SIZE // 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

RADIUS = SQUARE_SIZE // 2 - 5

screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('monospace', 75)

# main game loop
while not game_over:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, SQUARE_SIZE // 2), SQUARE_SIZE // 2)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, SQUARE_SIZE // 2), SQUARE_SIZE // 2)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            col = posx // SQUARE_SIZE
            # Player 1 input
            if turn == 0:
                if is_valid(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    turn = 1
                    if winning_move(board, 1):
                        label = font.render("Player 1 Wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True

            # Player 2 input
            else:
                if is_valid(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    turn = 0
                    if winning_move(board, 2):
                        label = font.render("Player 2 Wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        game_over = True
        draw_board(board, screen)
        if game_over:
            pygame.time.wait(3000)
