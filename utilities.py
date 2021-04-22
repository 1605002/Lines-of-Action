from globals import *
from constants import *
from queue import Queue

def get_cell_pos(i, j):
    return (BOARD_START_X+j*CELL_LENGTH, BOARD_START_Y+i*CELL_LENGTH)

def is_inside_cell(idx, pos):
    cell_rect = pygame.Rect(get_cell_pos(idx[0], idx[1]), CELL_SIZE)
    return cell_rect.collidepoint(pos)

def is_allowed(board, src_x, src_y, dest_x, dest_y):
    game_n = len(board)

    if dest_x < 0 or dest_x >= game_n or dest_y < 0 or dest_y >= game_n:
        return False
    if board[dest_x][dest_y] == board[src_x][src_y]:
        return False
    
    while dest_x != src_x or dest_y != src_y:
        if dest_x < src_x:
            dest_x += 1
        elif dest_x > src_x:
            dest_x -= 1

        if dest_y < src_y:
            dest_y += 1
        elif dest_y > src_y:
            dest_y -= 1

        if board[dest_x][dest_y] == 3-board[src_x][src_y]:
            return False

    return True
    

def get_clickable_cells(board, src_x, src_y):
    game_n = len(board)
    hor, ver, pos_diag, neg_diag = 0, 0, 0, 0

    for i in range(game_n):
        for j in range(game_n):
            if board[i][j] > 0:
                if i == src_x:
                    hor += 1
                if j == src_y:
                    ver += 1
                if i+j == src_x+src_y:
                    pos_diag += 1
                if i-j == src_x-src_y:
                    neg_diag += 1

    dest_cells = [(src_x, src_y)]
    dir_x = [0, 0, ver, -ver, pos_diag, -pos_diag, neg_diag, -neg_diag]
    dir_y = [hor, -hor, 0, 0, -pos_diag, pos_diag, neg_diag, -neg_diag]
    
    for i in range(8):
        if is_allowed(board, src_x, src_y, src_x+dir_x[i], src_y+dir_y[i]):
            dest_cells.append((src_x+dir_x[i], src_y+dir_y[i]))

    return dest_cells

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(str(board[i][j])+" ", end = " ")
        print()
    print()

def bfs(board, src_i, src_j):
    game_n = len(board)

    col = [[False] * game_n for i in range(game_n)]
    qu = Queue(0)
    dir_i = [-1, -1, -1, 0, 1, 1, 1, 0]
    dir_j = [-1, 0, 1, 1, 1, 0, -1, -1]

    qu.put(src_i)
    qu.put(src_j)
    col[src_i][src_j] = True
    tot = 1

    while qu.empty() == False:
        cur_i = qu.get()
        cur_j = qu.get()

        for k in range(8):
            nxt_i, nxt_j = cur_i+dir_i[k], cur_j+dir_j[k]
            if nxt_i < 0 or nxt_i >= game_n or nxt_j < 0 or nxt_j >= game_n:
                continue
            if board[nxt_i][nxt_j] != board[src_i][src_j] or col[nxt_i][nxt_j]:
                continue

            qu.put(nxt_i)
            qu.put(nxt_j)
            col[nxt_i][nxt_j] = True
            tot += 1

    return tot


def is_finished(board):
    res, game_n, tot_1, tot_2 = 0, len(board), 0, 0
    paise_1, paise_2, flag_1, flag_2 = 0, 0, True, True

    for i in range(game_n):
        for j in range(game_n):
            if board[i][j] == 1:
                tot_1 += 1
                if flag_1:
                    paise_1, flag_1 = bfs(board, i, j), False
            elif board[i][j] == 2:
                tot_2 += 1
                if flag_2:
                    paise_2, flag_2 = bfs(board, i, j), False

    if paise_1 == tot_1:
        res += 1
    if paise_2 == tot_2:
        res += 2

    return res
