import sys
import pygame as pg

import othello_ai

WIDTH = HEIGHT = 600
SQUARE_SIZE = HEIGHT // 8
MAX_FPS = 60
IMAGES = {token: pg.transform.scale(pg.image.load("images/" + token + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) for token in
          {"x", "o"}}
MOVE_STK = []
PLAYER_TOKEN = "x"
MAX_DEPTH = 2


def next_player(black_to_move):
    return ("o", False) if black_to_move else ("x", True)


def draw_state(screen, state, possible_moves):
    draw_board(screen)
    highlight_possible_moves(screen, possible_moves)
    draw_tokens(screen, state)


def draw_board(screen):
    colors = (pg.Color("dark green"), pg.Color("gray"))

    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]

            pg.draw.rect(screen, color, pg.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_tokens(screen, board):
    for i, cell in enumerate(board):
        if cell != ".":
            r, c = i // 8, i % 8

            if cell == "o":
                pg.draw.circle(screen, pg.Color("white"),
                               (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                               SQUARE_SIZE // 2.5)
            elif cell == "x":
                pg.draw.circle(screen, pg.Color("black"),
                               (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                               SQUARE_SIZE // 2.5)


def highlight_possible_moves(screen, possible_moves):
    s = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
    s.set_alpha(100)
    s.fill(pg.Color("yellow"))

    for move in possible_moves:
        screen.blit(s, (move % 8 * SQUARE_SIZE, move // 8 * SQUARE_SIZE))


def highlight_last_move():
    if len(MOVE_STK) > 0:
        s = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(pg.Color("blue"))
        screen.blit(s, (MOVE_STK[-1] % 8 * SQUARE_SIZE, MOVE_STK[-1] // 8 * SQUARE_SIZE))


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(pg.Color("white"))

board = othello_ai.START_STATE
token, black_to_move = next_player(False)

while True:
    possible_moves = othello_ai.possible_moves(board, token)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN and token == PLAYER_TOKEN:
            x, y = pg.mouse.get_pos()
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
            move = 8 * row + col

            if move in possible_moves or len(possible_moves) == 0:
                if len(possible_moves) > 0:
                    board = othello_ai.make_move(board, token, move)
                    MOVE_STK.append(move)

                token, black_to_move = next_player(black_to_move)

    if token != PLAYER_TOKEN:
        move = othello_ai.find_next_move(board, token, MAX_DEPTH)

        if move != -1:
            MOVE_STK.append(move)
            board = othello_ai.make_move(board, token, move)

        token, black_to_move = next_player(black_to_move)

    draw_state(screen, board, possible_moves)
    highlight_last_move()

    clock.tick(MAX_FPS)
    pg.display.flip()
