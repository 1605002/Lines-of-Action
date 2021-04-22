import pygame, sys
from globals import *
from constants import *
from game_components import *
from utilities import *

class Player:
    def __init__(self, turn_no, board):
        self.turn_no = turn_no
        self.board = board

        move_text = "Black's move" if turn_no == 1 else "White's move"
        self.move_text_label = PlainText(move_text, MOVE_TEXT_POS)
        self.no_move_button = PlainText("No valid move!", NO_MOVE_POS)
        self.main_menu_button = ButtonText("Go back to main menu", MAIN_MENU_POS)

        self.pieces = []
        piece_color = LIGHT_BLACK if turn_no == 1 else WHITE
        
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == turn_no:
                    piece_pos = get_cell_pos(i, j)
                    piece_rect = pygame.Rect(piece_pos, CELL_SIZE)
                    self.pieces.append(Piece(piece_color, i, j, piece_rect))

    def init_pieces(self):
        new_pieces = []
        for piece in self.pieces:
            if self.board[piece.cell_i][piece.cell_j] == self.turn_no:
                new_pieces.append(piece)

        self.move_text_label.draw()
        self.main_menu_button.draw()
        pygame.display.update()

        self.pieces = []
        for piece in new_pieces:
            self.pieces.append(piece)

    def move_to(self, i, j, ni, nj):
        moving_piece = None
        for piece in self.pieces:
            if piece.cell_i == i and piece.cell_j == j:
                moving_piece = piece

        self.board[i][j] = 0
        self.board[ni][nj] = self.turn_no

        moving_piece.go_to(get_cell_pos(ni, nj))
        moving_piece.cell_i , moving_piece.cell_j = ni, nj

        screen.blit(background, self.move_text_label.rect, self.move_text_label.rect)
        pygame.display.update()

        last_move[0], last_move[1], last_move[2], last_move[3] = i, j, ni, nj

    def make_move(self):
        pass

    def finish_game(self, ended):

        if ended == 1 or (self.turn_no == 1 and ended == 3):
            self.move_text_label.text = "Black has won!"
        else:
            self.move_text_label.text = "White has won!"

        self.move_text_label.draw()
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print(-1, flush = True)
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.main_menu_button.is_hovering(event.pos):
                            if is_ai[0]:
                                print(-2, flush = True)
                            return True

            pos = pygame.mouse.get_pos()
            if self.main_menu_button.is_hovering(pos):
                self.main_menu_button.draw(True)
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.main_menu_button.draw()
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()

class Human(Player):
    def __init__(self, turn_no, board):
        super().__init__(turn_no, board)

    def get_clicked_cell(self, cells):
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print(-1, flush = True)
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.main_menu_button.is_hovering(event.pos):
                            if is_ai[0]:
                                print(-2, flush = True)
                            return (-1, -1)
                        for cell in cells:
                            if is_inside_cell(cell, event.pos):
                                return cell

            pos = pygame.mouse.get_pos()
            if self.main_menu_button.is_hovering(pos):
                self.main_menu_button.draw(True)
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.main_menu_button.draw()
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()

    def make_move(self):

        self.init_pieces()

        own_cells = []
        for piece in self.pieces:
            own_cells.append((piece.cell_i, piece.cell_j))

        while True:
            (clicked_i, clicked_j) = self.get_clicked_cell(own_cells)
            if clicked_i == -1:
                return True

            destinations = get_clickable_cells(self.board, clicked_i, clicked_j)

            if len(destinations) == 1:
                self.no_move_button.draw()
                continue
            else:
                self.no_move_button.erase()

            cur_surface = pygame.Surface(GAME_SIZE)
            cur_surface.blit(screen, ORIGIN)

            src_x, src_y = get_cell_pos(clicked_i, clicked_j)
            src_x, src_y = src_x+CELL_LENGTH/2, src_y+CELL_LENGTH/2

            for i in range(1, len(destinations)):
                dest_i, dest_j = destinations[i]
                dest_x, dest_y = get_cell_pos(dest_i, dest_j)
                dest_x, dest_y = dest_x+CELL_LENGTH/2, dest_y+CELL_LENGTH/2

                pygame.draw.line(screen, RED, (src_x, src_y), (dest_x, dest_y), 3)
            
            pygame.display.update()

            (new_i, new_j) = self.get_clicked_cell(destinations)
            if new_i == -1:
                return True

            screen.blit(cur_surface, ORIGIN)
            pygame.display.update()

            if new_i == clicked_i and new_j == clicked_j:
                continue

            self.move_to(clicked_i, clicked_j, new_i, new_j)

            ended = is_finished(self.board)
            if ended == 0:
                return False

            self.finish_game(ended)
            return True


class AI(Player):

    def __init__(self, turn_no, board):
        super().__init__(turn_no, board)

    def make_move(self):

        self.init_pieces()

        if last_move[0] != -1:
            logpy.write("My move: "+" ".join([str(s) for s in last_move])+"\n")
            print(" ".join([str(s) for s in last_move]), flush = True)
        
        i, j, ni, nj = tuple(map(int, input().split()))
        logpy.write("His move: "+" ".join(map(str, [i, j, ni, nj]))+"\n")

        if i < 0 or i >= len(self.board) or j < 0 or j >= len(self.board) or ni < 0 or ni >= len(self.board) or nj < 0 or nj >= len(self.board):
            logpy.write("Baje move: "+" ".join(map(str, [i, j, ni, nj]))+"\n")

        self.move_to(i, j, ni, nj)

        ended = is_finished(self.board)
        if ended == 0:
            return False

        self.finish_game(ended)
        return True

