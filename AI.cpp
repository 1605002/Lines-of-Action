#include<bits/stdc++.h>
using namespace std;
#define M 13
typedef pair<int, int> pii;
typedef pair<pii, pii> ppp;

const int INF = 1000000000;

int MAX_DEPTH = 4;
int dx[] = {-1, -1, -1, 0, 1, 1, 1, 0};
int dy[] = {-1, 0, 1, 1, 1, 0, -1, -1};

int halfx[] = {0, 1, 1, 1};
int halfy[] = {1, 1, 0, -1};

int con_vals[] = {0, 10000000, 500, 350, 200, 150, 125, 50, 40, 35, 30, 25, 20};

int pieceSquareTable8[8][8] =
{
{-80, -25, -20, -20, -20, -20, -25,  -80},
{-25,  10,  10,  10,  10,  10,  10,  -25},
{-20,  10,  25,  25,  25,  25,  10,  -20},
{-20,  10,  25,  50,  50,  25,  10,  -20},
{-20,  10,  25,  50,  50,  25,  10,  -20},
{-20,  10,  25,  25,  25,  25,  10,  -20},
{-25,  10,  10,  10,  10,  10,  10,  -25},
{-80, -25, -20, -20, -20, -20, -25,  -80}
};

int pieceSquareTable6[6][6] =
{
{-80, -25, -20, -20, -25,  -80},
{-25,  20,  20,  20,  20,  -25},
{-20,  20,  50,  50,  20,  -20},
{-20,  20,  50,  50,  20,  -20},
{-25,  20,  20,  20,  20,  -25},
{-80, -25, -20, -20, -25,  -80}
};

int n;
int piece_n;

int board[M][M];
int col[M][M];

pii pieces[3][M];
int ulta[M][M];

ppp best_move;

ofstream fout("logAI.txt");

void init(int sz)
{
    memset(board, 0, sizeof(board));
    memset(col, 0, sizeof(board));
    memset(ulta, 0, sizeof(board));
    for(int j = 0; j < 3; j++)
    {
        for(int i = 0; i < M; i++) pieces[j][i] = {0, 0};
    }

    n = sz, piece_n = (sz-2)*2;

    int bn = 0, wn = 0;
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            if((i == 0 || i == n-1) && j > 0 && j < n-1)
            {
                board[i][j] = 1;
                ulta[i][j] = bn;
                pieces[1][bn++] = {i, j};
            }
            else if((j == 0 || j == n-1) && i > 0 && i < n-1)
            {
                board[i][j] = 2;
                ulta[i][j] = wn;
                pieces[2][wn++] = {i, j};
            }
            else board[i][j] = 0;
        }
    }

    assert(wn == bn && wn == piece_n);
}

bool bhitore(int i, int j) { return i >= 0 && i < n && j >= 0 && j < n; }

bool in_range(int x, int y, int z)
{
    if(x == y || z == -1) return true;
    if(y > x) return y <= z;
    if(y < x) return y >= z;
}

void dfs(int i, int j)
{
    col[i][j] = 1;

    for(int k = 0; k < 8; k++)
    {
        int ni = i+dx[k], nj = j+dy[k];
        if(!bhitore(ni, nj) || col[ni][nj] || board[ni][nj] != board[i][j]) continue;

        dfs(ni, nj);
    }
}

pii components()
{
    int a[] = {0, 0, 0};

    for(int j = 1; j <= 2; j++)
    {
        for(int i = 0; i < piece_n; i++)
        {
            int x = pieces[j][i].first, y = pieces[j][i].second;
            if(x != -1 && !col[x][y]) a[j]++, dfs(x, y);
        }
    }

    for(int j = 1; j <= 2; j++)
    {
        for(int i = 0; i < piece_n; i++)
        {
            int x = pieces[j][i].first, y = pieces[j][i].second;
            if(x != -1) col[x][y] = 0;
        }
    }

    return {a[1], a[2]};
}

int winning(int a, int b, int move)
{
    assert(a > 0 && b > 0 && a <= piece_n && b <= piece_n && move > 0 && move < 3);

    if(a > 1 && b > 1) return 0;
    if(b > 1 || (a == 1 && move == 2)) return 1;
    return 2;
}

int connected_h(int a, int b, int winner)
{
    if(winner == 1) return con_vals[1];
    if(winner == 2) return -con_vals[1];
    return con_vals[a]-con_vals[b]; 
}

int quad_h()
{
    int bh = 0, wh = 0;

    for(int i = 0; i+1 < n; i++)
    {
        for(int j = 0; j+1 < n; j++)
        {
            int c1 = (board[i][j] == 1)+(board[i][j+1] == 1)+(board[i+1][j] == 1)+(board[i+1][j+1] == 1);
            int c2 = (board[i][j] == 2)+(board[i][j+1] == 2)+(board[i+1][j] == 2)+(board[i+1][j+1] == 2);

            if(c1 >= 3) bh++;
            else if(c2 >= 3) wh++;
        }
    }

    return (bh-wh);
}

int density_h()
{
    int bcomx = 0, bcomy = 0, wcomx = 0, wcomy = 0;
    int btot = 0, wtot = 0;

    for(int j = 1; j <= 2; j++)
    {
        for(int i = 0; i < piece_n; i++)
        {
            if(pieces[j][i].first != -1)
            {
                if(j == 1) bcomx += pieces[j][i].first, bcomy += pieces[j][i].second, btot++;
                else wcomx += pieces[j][i].first, wcomy += pieces[j][i].second, wtot++;
            }
        }
    }

    int baod = 0, waod = 0;

    for(int j = 1; j <= 2; j++)
    {
        for(int i = 0; i < piece_n; i++)
        {
            if(pieces[j][i].first != -1)
            {
                if(j == 1) baod += abs(pieces[j][i].first-bcomx)+abs(pieces[j][i].second-bcomy);
                else waod += abs(pieces[j][i].first-wcomx)+abs(pieces[j][i].second-wcomy);
            }
        }
    }
    baod /= btot, waod /= wtot;

    return (waod-baod);
}

int piece_square_h()
{
    int h = 0;
    for(int j = 1; j <= 2; j++)
    {
        for(int i = 0; i < piece_n; i++)
        {
            if(pieces[j][i].first != -1)
            {
                int x = pieces[j][i].first, y = pieces[j][i].second;

                if(j == 1) h += (n == 8)? pieceSquareTable8[x][y]: pieceSquareTable6[x][y];
                else h -= (n == 8)? pieceSquareTable8[x][y]: pieceSquareTable6[x][y];
            }
        }
    }

    return h;
}

int count_pcs(int k, int move, int cur_x, int cur_y, int &op_x, int &op_y, int dir)
{
    int tot = 0;

    while(true)
    {
        cur_x += dir*halfx[k], cur_y += dir*halfy[k];
        if(!bhitore(cur_x, cur_y)) return tot;

        if(board[cur_x][cur_y])
        {
            tot++;
            if(board[cur_x][cur_y] != move && op_x == -1) op_x = cur_x, op_y = cur_y;
        }
    }
}

void move_to(int i, int move, int x, int y, int nx, int ny, int &onno)
{
    if(board[nx][ny]) onno = ulta[nx][ny];

    board[x][y] = 0, board[nx][ny] = move;
    pieces[move][i] = {nx, ny};
    if(onno != -1) pieces[3-move][onno] = {-1, -1};
    ulta[nx][ny] = i;
}

void go_back(int i, int move, int x, int y, int nx, int ny, int onno)
{
    board[x][y] = move, board[nx][ny] = (onno != -1)? 3-move: 0;
    pieces[move][i] = {x, y};
    if(onno != -1) pieces[3-move][onno] = {nx, ny};
    ulta[x][y] = i, ulta[nx][ny] = onno;
}

int alpha_beta_pruning(int alpha, int beta, int depth, int move)
{
    assert(alpha < beta);

    pii p = components();
    int a = p.first, b = p.second;

    int winner = winning(a, b, move);
    if(winner || depth == MAX_DEPTH)
    {
        return connected_h(a, b, winner)/2+quad_h()*300+density_h()+300+piece_square_h()*4;
    }

    pii half[] = {{0, 1}, {1, 1}, {1, 0}, {1, -1}};
    random_shuffle(half, half+4);

    for(int i = 0; i < piece_n; i++)
    {
        pii p = pieces[move][i];
        int x = p.first, y = p.second;
        if(x == -1) continue;

        for(int k = 0; k < 4; k++)
        {
            int pos_x = -1, pos_y = -1;
            int neg_x = -1, neg_y = -1;

            halfx[k] = half[k].first, halfy[k] = half[k].second;
            
            int tot = 1;
            tot += count_pcs(k, move, x, y, pos_x, pos_y, 1);
            tot += count_pcs(k, move, x, y, neg_x, neg_y, -1);

            int nx = x+tot*halfx[k], ny = y+tot*halfy[k];
            if(bhitore(nx, ny) && board[nx][ny] != board[x][y] && in_range(x, nx, pos_x) && in_range(y, ny, pos_y))
            {
                int onno = -1;
                
                move_to(i, move, x, y, nx, ny, onno);
                int res = alpha_beta_pruning(alpha, beta, depth+1, 3-move);
                go_back(i, move, x, y, nx, ny, onno);

                bool flag = false;

                if(move == 1 && res > alpha) alpha = res, flag = true;
                else if(move == 2 && res < beta) beta = res, flag = true;

                if(depth == 0 && flag) best_move = {{x, y}, {nx, ny}};
                if(alpha >= beta) return move == 1? alpha: beta;
            }

            halfx[k] = half[k].first, halfy[k] = half[k].second;
            nx = x-tot*halfx[k], ny = y-tot*halfy[k];

            if(bhitore(nx, ny) && board[nx][ny] != board[x][y] && in_range(x, nx, neg_x) && in_range(y, ny, neg_y))
            {
                int onno = -1;

                move_to(i, move, x, y, nx, ny, onno);
                int res = alpha_beta_pruning(alpha, beta, depth+1, 3-move);
                go_back(i, move, x, y, nx, ny, onno);

                bool flag = false;

                if(move == 1 && res > alpha) alpha = res, flag = true;
                else if(move == 2 && res < beta) beta = res, flag = true;

                if(depth == 0 && flag) best_move = {{x, y}, {nx, ny}};
                if(alpha >= beta) return move == 1? alpha: beta;
            }
        }
    }

    return (move == 1)? alpha: beta;
}

void play_game(int sz, int turn_no)
{
    init(sz);
    MAX_DEPTH = 4+(sz == 6);

    int move = 1, dummy = -1;

    while(true)
    {
        if(move == turn_no)
        {
            alpha_beta_pruning(-INF, INF, 0, move);

            pii fst = best_move.first, lst = best_move.second;
            int x = fst.first, y = fst.second, nx = lst.first, ny = lst.second;

            dummy = -1;
            move_to(ulta[x][y], move, x, y, nx, ny, dummy);

            printf("%d %d %d %d\n", x, y, nx, ny);
            fflush(stdout);

            fout<<"My move: "<<x<<" "<<y<<" "<<nx<<" "<<ny<<endl;
        }
        else if(move != turn_no)
        {
            int x, y, nx, ny;
            scanf("%d", &x);

            fout<<x<<endl;

            if(x == -1) exit(0);
            if(x == -2) return;
            scanf("%d %d %d", &y, &nx, &ny);

            fout<<"Her move: "<<x<<" "<<y<<" "<<nx<<" "<<ny<<endl;

            dummy = -1;
            move_to(ulta[x][y], move, x, y, nx, ny, dummy);
        }
        
        move = 3-move;
    }
}

int main()
{
    srand(time(NULL));

    string buf;
    getline(cin, buf);
    fout<<buf<<endl;
    getline(cin, buf);
    fout<<buf<<endl;
    
    while(true)
    {
        int choice;
        scanf("%d", &choice);

        fout<<choice<<endl;

        if(choice == -1) exit(0);

        assert(choice == 6 || choice == 8);

        int turn_no;
        scanf("%d", &turn_no);

        fout<<turn_no<<endl;

        play_game(choice, turn_no);
    }

    return 0;
}