import pygame, sys
from globals import *
from constants import *
from utilities import *
from game_components import *
from players import *

def show_intro_page():

    hvh = ButtonText("Human vs Human", HVH_POS)
    hvai = ButtonText("Human vs AI", HVI_POS)
    aivh = ButtonText("AI vs Human", AVI_POS)
    bsz = PlainText("Board Size: 6 x 6", BSZ_POS)
    ctc = ButtonText("(Click here to change)", CTC_POS)

    buttons = [hvh, hvai, aivh, ctc]

    screen.blit(background, ORIGIN)

    game_n = 6
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print(-1, flush = True)
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if ctc.is_hovering(event.pos):
                    game_n = 14-game_n
                    bsz.text = "Board Size: "+str(game_n)+" x "+str(game_n)

                if hvh.is_hovering(event.pos):
                    return (game_n, 1)
                if hvai.is_hovering(event.pos):
                    return (game_n, 2)
                if aivh.is_hovering(event.pos):
                    return (game_n, 3)

        pos = pygame.mouse.get_pos()
        hovering = False

        for button in buttons:
            if button.is_hovering(pos):
                button.draw(True)
                hovering = True
            else:
                button.draw()
        bsz.draw()

        pygame.display.update()

        if hovering:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


def show_game_page(game_tp):
    screen.blit(background, ORIGIN)
    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    game_n = game_tp[0]
    board = []
    for i in range(game_n):
        board.append([])
        for j in range(game_n):
            if (i == 0 or i == game_n-1) and j > 0 and j < game_n-1:
                board[i].append(1)
            elif (j == 0 or j == game_n-1) and i > 0 and i < game_n-1:
                board[i].append(2)
            else:
                board[i].append(0)

            cell_color = LIGHT_CREAM if (i+j)%2 == 0 else DARK_CREAM
            cell_rect = pygame.Rect(get_cell_pos(i, j), CELL_SIZE)
            pygame.draw.rect(screen, cell_color, cell_rect)

    game_mode = game_tp[1]

    last_move[0], last_move[1], last_move[2], last_move[3] = -1, -1, -1, -1

    player1 = Human(1, board) if game_mode == 1 or game_mode == 2 else AI(1, board)
    player2 = Human(2, board) if game_mode == 1 or game_mode == 3 else AI(2, board)

    if game_mode == 2 or game_mode == 3:
        print(str(game_n)+" "+str(4-game_mode), flush = True)
        logpy.write(str(game_n)+" "+str(4-game_mode)+"\n")

    is_ai[0] = (game_mode == 2 or game_mode == 3)

    for piece in player1.pieces:
        piece.draw()
    for piece in player2.pieces:
        piece.draw()

    pygame.display.update()

    cur_turn = 1
    ended = False

    while True:
        if cur_turn == 1:
            ended = player1.make_move()
        else:
            ended = player2.make_move()
        if ended:
            return

        cur_turn = 3-cur_turn


while True:
    game_tp = show_intro_page()
    show_game_page(game_tp)