import pygame as p
import numpy as np

p.init()

width = height = 512
dimension = 8
rect_size = width // dimension
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (211, 211, 211)
red = (255, 0, 0)
blue = (0, 0, 255)
beige = (245, 245, 220)
green = (0, 171, 65)
cream = (255, 253, 208)

r = -1
c = -1
turn = 0
valid_moves = []
white_king = None
black_king = None
update_pawn = False
# font = p.font.SysFont(None, 20)

clock = p.time.Clock()
fps = 60

chess_board = np.empty((8, 8), dtype=object)

screen = p.display.set_mode((width, height))

p.display.set_caption("Chess")
p.display.update()

exit_game = False
game_over = False


class Pawn:
    def __init__(self, y, x, color):
        pawn = p.image.load(fr'images\{color}_pawn.svg')
        self.image = p.transform.scale(pawn, (120, 120))
        self.col = y
        self.row = x
        self.color = color
        self.is_moved = False
        self.name = 'Pawn'

    def available_moves(self):
        if self.color == 'white':
            valid_move = []

            if not self.is_moved:
                if chess_board[self.row+1][self.col] is None:
                    valid_move.append((self.col, self.row+1))

                    if chess_board[self.row+2][self.col] is None:
                        valid_move.append((self.col, self.row+2))

            elif self.row+1 <= 7 and chess_board[self.row+1][self.col] is None:
                valid_move.append((self.col, self.row+1))

            if self.row + 1 <= 7 and self.col + 1 <= 7 and chess_board[self.row+1][self.col+1] is not None:
                if chess_board[self.row+1][self.col+1].color == 'black':
                    valid_move.append((self.col + 1, self.row + 1))

            if self.row + 1 <= 7 and self.col - 1 >= 0 and chess_board[self.row+1][self.col-1] is not None:
                if chess_board[self.row+1][self.col-1].color == 'black':
                    valid_move.append((self.col - 1, self.row + 1))

            return valid_move

        elif self.color == 'black':
            valid_move = []

            if not self.is_moved:
                if chess_board[self.row-1][self.col] is None:
                    valid_move.append((self.col, self.row-1))

                    if chess_board[self.row-2][self.col] is None:
                        valid_move.append((self.col, self.row-2))

            elif self.row-1 >= 0 and chess_board[self.row-1][self.col] is None:
                valid_move.append((self.col, self.row-1))

            if self.row - 1 >= 0 and self.col + 1 <= 7 and chess_board[self.row-1][self.col+1] is not None:
                if chess_board[self.row-1][self.col+1].color == 'white':
                    valid_move.append((self.col + 1, self.row - 1))

            if self.row - 1 >= 0 and self.col - 1 >= 0 and chess_board[self.row-1][self.col-1] is not None:
                if chess_board[self.row-1][self.col-1].color == 'white':
                    valid_move.append((self.col - 1, self.row - 1))

            return valid_move

    def possible_moves(self):
        if self.color == 'white':
            # if not self.is_moved:
            #     if chess_board[self.row+1][self.col] is None:
            #         possible_move.append((self.col, self.row+1))
            #
            #         if chess_board[self.row+2][self.col] is None:
            #             possible_move.append((self.col, self.row+2))

            # elif self.row+1 <= 7 and chess_board[self.row+1][self.col] is None:
            #     possible_move.append((self.col, self.row+1))

            possible_move = []

            if self.row + 1 <= 7 and self.col + 1 <= 7:
                possible_move.append((self.col + 1, self.row + 1))

            if self.row + 1 <= 7 and self.col - 1 >= 0:
                possible_move.append((self.col - 1, self.row + 1))

            return possible_move

        elif self.color == 'black':
            possible_move = []

            # if not self.is_moved:
            #     if chess_board[self.row-1][self.col] is None:
            #         possible_move.append((self.col, self.row-1))
            #
            #     if chess_board[self.row-2][self.col] is None:
            #         possible_move.append((self.col, self.row-2))
            #
            # elif self.row-1 >= 0 and chess_board[self.row-1][self.col] is None:
            #     possible_move.append((self.col, self.row-1))

            if self.row - 1 >= 0 and self.col + 1 <= 7:
                possible_move.append((self.col + 1, self.row - 1))

            if self.row - 1 >= 0 and self.col - 1 >= 0:
                possible_move.append((self.col - 1, self.row - 1))

            return possible_move


class Knight:
    def __init__(self, y, x, color):
        knight = p.image.load(fr'images\{color}_knight.svg')
        self.image = p.transform.scale(knight, (120, 120))
        self.col = y
        self.row = x
        self.color = color
        self.is_moved = False
        self.name = 'Knight'

    def available_moves(self):
        valid_move = []

        if self.row+2 <= 7 and self.col+1 <= 7 and (chess_board[self.row+2][self.col+1] is None or chess_board[self.row+2]
           [self.col+1].color != self.color):
            valid_move.append((self.col+1, self.row+2))

        if self.row+2 <= 7 and self.col-1 >= 0 and (chess_board[self.row+2][self.col-1] is None or chess_board[self.row+2]
           [self.col-1].color != self.color):
            valid_move.append((self.col-1, self.row+2))

        if self.row+1 <= 7 and self.col+2 <= 7 and (chess_board[self.row+1][self.col+2] is None or chess_board[self.row+1]
           [self.col+2].color != self.color):
            valid_move.append((self.col+2, self.row+1))

        if self.row+1 <= 7 and self.col-2 >= 0 and (chess_board[self.row+1][self.col-2] is None or chess_board[self.row+1]
           [self.col-2].color != self.color):
            valid_move.append((self.col-2, self.row+1))

        if self.row-1 >= 0 and self.col+2 <= 7 and (chess_board[self.row-1][self.col+2] is None or chess_board[self.row-1]
           [self.col+2].color != self.color):
            valid_move.append((self.col+2, self.row-1))

        if self.row-1 >= 0 and self.col-2 >= 0 and (chess_board[self.row-1][self.col-2] is None or chess_board[self.row-1]
           [self.col-2].color != self.color):
            valid_move.append((self.col-2, self.row-1))

        if self.row-2 >= 0 and self.col+1 <= 7 and (chess_board[self.row-2][self.col+1] is None or chess_board[self.row-2]
           [self.col+1].color != self.color):
            valid_move.append((self.col+1, self.row-2))

        if self.row-2 >= 0 and self.col-1 >= 0 and (chess_board[self.row-2][self.col-1] is None or chess_board[self.row-2]
           [self.col-1].color != self.color):
            valid_move.append((self.col-1, self.row-2))

        return valid_move


class Bishops:
    def __init__(self, y, x, color):
        bishop = p.image.load(fr'images\{color}_bishop.svg')
        self.image = p.transform.scale(bishop, (120, 120))
        self.col = y
        self.row = x
        self.color = color
        self.is_moved = False
        self.name = 'Bishop'

    def available_moves(self):
        valid_move = []

        for i in range(4):
            a, b = self.row, self.col

            if i == 0:
                print(a)
                print(b)
                while a-1 >= 0 and b-1 >= 0 and (chess_board[a-1][b-1] is None or chess_board[a-1][b-1].color != self.color):
                    if chess_board[a-1][b-1] is not None:
                        valid_move.append((b-1, a-1))
                        break

                    else:
                        valid_move.append((b-1, a-1))
                        a = a-1
                        b = b-1

            elif i == 1:
                while a + 1 <= 7 and b-1 >= 0 and (chess_board[a+1][b-1] is None or chess_board[a+1][b-1].color != self.color):
                    if chess_board[a+1][b-1] is not None:
                        valid_move.append((b-1, a + 1))
                        break

                    else:
                        valid_move.append((b-1, a + 1))
                        a = a + 1
                        b = b - 1

            elif i == 2:
                while a-1 >= 0 and b + 1 <= 7 and (chess_board[a-1][b+1] is None or chess_board[a-1][b+1].color != self.color):
                    if chess_board[a-1][b+1] is not None:
                        valid_move.append((b+1, a-1))
                        break

                    else:
                        valid_move.append((b+1, a-1))
                        b = b + 1
                        a = a - 1

            elif i == 3:
                while a+1 <= 7 and b + 1 <= 7 and (chess_board[a+1][b+1] is None or chess_board[a+1][b+1].color != self.color):
                    if chess_board[a+1][b+1] is not None:
                        valid_move.append((b+1, a+1))
                        break

                    else:
                        valid_move.append((b+1, a+1))
                        b = b + 1
                        a = a + 1

        return valid_move


class Rook:
    def __init__(self, y, x, color):
        rook = p.image.load(fr'images\{color}_rook.svg')
        self.image = p.transform.scale(rook, (120, 120))
        self.col = y
        self.row = x
        self.color = color
        self.is_moved = False
        self.name = 'Rook'

    def available_moves(self):
        valid_move = []

        for i in range(4):
            a, b = self.row, self.col

            if i == 0:
                while a-1 >= 0 and (chess_board[a-1][b] is None or chess_board[a-1][b].color != self.color):
                    if chess_board[a-1][b] is not None:
                        valid_move.append((b, a-1))
                        break

                    else:
                        valid_move.append((b, a-1))
                        a = a-1

            elif i == 1:
                while a + 1 <= 7 and (chess_board[a+1][b] is None or chess_board[a+1][b].color != self.color):
                    if chess_board[a+1][b] is not None:
                        valid_move.append((b, a + 1))
                        break

                    else:
                        valid_move.append((b, a + 1))
                        a = a + 1

            elif i == 2:
                while b - 1 >= 0 and (chess_board[a][b-1] is None or chess_board[a][b-1].color != self.color):
                    if chess_board[a][b-1] is not None:
                        valid_move.append((b-1, a))
                        break

                    else:
                        valid_move.append((b-1, a))
                        b = b - 1

            elif i == 3:
                while b + 1 <= 7 and (chess_board[a][b+1] is None or chess_board[a][b+1].color != self.color):
                    if chess_board[a][b+1] is not None:
                        valid_move.append((b+1, a))
                        break

                    else:
                        valid_move.append((b+1, a))
                        b = b + 1

        return valid_move


class Queen:
    def __init__(self, y, x, color):
        queen = p.image.load(fr'images\{color}_queen.svg')
        self.image = p.transform.scale(queen, (120, 120))
        self.col = y
        self.row = x
        self.color = color
        self.is_moved = False
        self.name = 'Queen'

    def available_moves(self):
        valid_move = []
        b = Bishops(self.col, self.row, self.color)
        valid_move.extend(b.available_moves())
        ro = Rook(self.col, self.row, self.color)
        valid_move.extend(ro.available_moves())
        return valid_move


class King:
    def __init__(self, y, x, color):
        king = p.image.load(fr'images\{color}_king.svg')
        self.image = p.transform.scale(king, (120, 120))
        self.col = y
        self.row = x
        self.color = color
        self.is_moved = False
        self.name = 'King'

    def available_moves(self, opposite_valid_moves):
        valid_move = []
        if self.col-1 >= 0 and (chess_board[self.row][self.col-1] is None or chess_board[self.row][self.col-1].color != self.color):
            if (self.col-1, self.row) not in opposite_valid_moves:
                valid_move.append((self.col-1, self.row))

            if not self.is_moved and chess_board[self.row][self.col-1] is None:
                if self.chaseling(opposite_valid_moves, 'left'):
                    valid_move.append((self.col-2, self.row))

        if self.col+1 <= 7 and (chess_board[self.row][self.col+1] is None or chess_board[self.row][self.col+1].color != self.color):
            if (self.col+1, self.row) not in opposite_valid_moves:
                valid_move.append((self.col+1, self.row))

            if not self.is_moved and chess_board[self.row][self.col+1] is None:
                if self.chaseling(opposite_valid_moves, 'right'):
                    valid_move.append((self.col+2, self.row))

        if self.row-1 >= 0 and ((chess_board[self.row-1][self.col] is None or chess_board[self.row-1][self.col].color != self.color)
                                and (self.col, self.row-1) not in opposite_valid_moves):
            valid_move.append((self.col, self.row-1))

        if (self.row-1 >= 0 and self.col-1 >= 0 and ((chess_board[self.row-1][self.col-1] is None or chess_board[self.row-1]
           [self.col-1].color != self.color) and (self.col-1, self.row-1) not in opposite_valid_moves)):
            valid_move.append((self.col-1, self.row-1))

        if (self.row-1 >= 0 and self.col+1 <= 7 and ((chess_board[self.row-1][self.col+1] is None or chess_board[self.row-1]
           [self.col+1].color != self.color) and (self.col+1, self.row-1) not in opposite_valid_moves)):
            valid_move.append((self.col+1, self.row-1))

        if (self.row+1 <= 7 and self.col-1 >= 0 and ((chess_board[self.row+1][self.col-1] is None or chess_board[self.row+1]
           [self.col-1].color != self.color) and (self.col-1, self.row+1) not in opposite_valid_moves)):
            valid_move.append((self.col-1, self.row+1))

        if (self.row+1 <= 7 and self.col+1 <= 7 and ((chess_board[self.row+1][self.col+1] is None or chess_board[self.row+1]
           [self.col+1].color != self.color) and (self.col+1, self.row+1) not in opposite_valid_moves)):
            valid_move.append((self.col+1, self.row+1))

        if self.row+1 <= 7 and ((chess_board[self.row+1][self.col] is None or chess_board[self.row+1][self.col].color != self.color)
                                and (self.col, self.row+1) not in opposite_valid_moves):
            valid_move.append((self.col, self.row+1))

        return valid_move

    def chaseling(self, opposite_valid_moves, direction):
        # left side
        if direction == 'left':
            left = False
            if (self.col - 2 >= 0 and (chess_board[self.row][self.col - 2] is None and
               (self.col - 2, self.row) not in opposite_valid_moves)):
                if chess_board[self.row][self.col-3] is not None:
                    if (self.col - 3 >= 0 and (chess_board[self.row][self.col - 3].color == self.color and
                       chess_board[self.row][self.col - 3].name == 'Rook')):
                        left = True

            return left

        if direction == 'right':
            right = False
            if (self.col + 2 <= 7 and chess_board[self.row][self.col + 2] is None and
               (self.col + 2, self.row) not in opposite_valid_moves):
                if self.col + 3 <= 7 and chess_board[self.row][self.col + 3] is None:
                    if chess_board[self.row][self.col + 4] is not None:
                        if (self.col + 4 <= 7 and chess_board[self.row][self.col + 4].color == self.color or chess_board[self.row][
                           self.col+4].name == 'Rook'):
                            right = True

            return right


def initialize_class():
    global white_king
    global black_king

    w_rook_1 = Rook(0, 0, 'white')
    chess_board[0][0] = w_rook_1
    w_knight_1 = Knight(1, 0, 'white')
    chess_board[0][1] = w_knight_1
    w_bishop_1 = Bishops(2, 0, 'white')
    chess_board[0][2] = w_bishop_1
    w_king = King(3, 0, 'white')
    chess_board[0][3] = w_king
    white_king = chess_board[0][3]
    w_queen = Queen(4, 0, 'white')
    chess_board[0][4] = w_queen
    w_bishop_2 = Bishops(5, 0, 'white')
    chess_board[0][5] = w_bishop_2
    w_knight_2 = Knight(6, 0, 'white')
    chess_board[0][6] = w_knight_2
    w_rook_2 = Rook(7, 0, 'white')
    chess_board[0][7] = w_rook_2
    w_pawn_1 = Pawn(0, 1, 'white')
    chess_board[1][0] = w_pawn_1
    w_pawn_2 = Pawn(1, 1, 'white')
    chess_board[1][1] = w_pawn_2
    w_pawn_3 = Pawn(2, 1, 'white')
    chess_board[1][2] = w_pawn_3
    w_pawn_4 = Pawn(3, 1, 'white')
    chess_board[1][3] = w_pawn_4
    w_pawn_5 = Pawn(4, 1, 'white')
    chess_board[1][4] = w_pawn_5
    w_pawn_6 = Pawn(5, 1, 'white')
    chess_board[1][5] = w_pawn_6
    w_pawn_7 = Pawn(6, 1, 'white')
    chess_board[1][6] = w_pawn_7
    w_pawn_8 = Pawn(7, 1, 'white')
    chess_board[1][7] = w_pawn_8

    b_rook_1 = Rook(0, 7, 'black')
    chess_board[7][0] = b_rook_1
    b_knight_1 = Knight(1, 7, 'black')
    chess_board[7][1] = b_knight_1
    b_bishop_1 = Bishops(2, 7, 'black')
    chess_board[7][2] = b_bishop_1
    b_king = King(3, 7, 'black')
    chess_board[7][3] = b_king
    black_king = chess_board[7][3]
    b_queen = Queen(4, 7, 'black')
    chess_board[7][4] = b_queen
    b_bishop_2 = Bishops(5, 7, 'black')
    chess_board[7][5] = b_bishop_2
    b_knight_2 = Knight(6, 7, 'black')
    chess_board[7][6] = b_knight_2
    b_rook_2 = Rook(7, 7, 'black')
    chess_board[7][7] = b_rook_2
    b_pawn_1 = Pawn(0, 6, 'black')
    chess_board[6][0] = b_pawn_1
    b_pawn_2 = Pawn(1, 6, 'black')
    chess_board[6][1] = b_pawn_2
    b_pawn_3 = Pawn(2, 6, 'black')
    chess_board[6][2] = b_pawn_3
    b_pawn_4 = Pawn(3, 6, 'black')
    chess_board[6][3] = b_pawn_4
    b_pawn_5 = Pawn(4, 6, 'black')
    chess_board[6][4] = b_pawn_5
    b_pawn_6 = Pawn(5, 6, 'black')
    chess_board[6][5] = b_pawn_6
    b_pawn_7 = Pawn(6, 6, 'black')
    chess_board[6][6] = b_pawn_7
    b_pawn_8 = Pawn(7, 6, 'black')
    chess_board[6][7] = b_pawn_8


class Check:
    def __init__(self, color):
        global white_king
        global black_king

        self.color = color
        self.count = 0
        self.valid_move = []
        self.attacker_move = []
        if self.color == 'white':
            self.k = white_king

        else:
            self.k = black_king
        self.check = False
        self.checkmate = False
        self.chance = False

    def is_in_check(self):
        self.opposite_pieces_move()
        if self.check:
            print("Opposite Move: ", self.valid_move)
            king_move = self.k.available_moves(self.valid_move)
            print("King Moves: ", king_move)
            for move in king_move:
                if self.possible_move(self.k.row, self.k.col, move[1], move[0]):
                    self.chance = True

            if not self.chance:
                self.friends_pieces_move()

            if not self.chance:
                self.checkmate = True

    def opposite_pieces_move(self):
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] is not None and chess_board[i][j].color != self.color and chess_board[i][j].name != 'King':
                    if chess_board[i][j].name == 'Pawn':
                        v_move = chess_board[i][j].possible_moves()

                    else:
                        v_move = chess_board[i][j].available_moves()

                    if (self.k.col, self.k.row) in v_move:
                        self.count += 1
                        self.attacker_move.append((chess_board[i][j].col, chess_board[i][j].row))
                        self.attacker_move.extend(v_move)
                        self.check = True

                    self.valid_move.extend(v_move)

    def friends_pieces_move(self):
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] is not None and chess_board[i][j].color == self.color and chess_board[i][j].name != 'King':
                    v_move = chess_board[i][j].available_moves()

                    for move in v_move:
                        if move in self.attacker_move:
                            if self.possible_move(i, j, move[1], move[0]):
                                self.chance = True
                                break

                if self.chance:
                    break

            if self.chance:
                break

    def possible_move(self, i, j, ro, co):
        obj1 = chess_board[i][j]

        past_row = obj1.row
        past_col = obj1.col

        obj1.row = ro
        obj1.col = co

        obj2 = None
        if chess_board[ro][co] is not None:
            obj2 = chess_board[ro][co]

        chess_board[ro][co] = obj1
        chess_board[i][j] = None

        che = Check(obj1.color)
        che.opposite_pieces_move()

        obj1.row = past_row
        obj1.col = past_col

        if not che.check:
            chess_board[i][j] = obj1
            chess_board[ro][co] = obj2
            return True

        else:
            chess_board[i][j] = obj1
            chess_board[ro][co] = obj2
            return False


def draw_rectangular():
    y = 0
    turns = 0
    for row in range(8):
        x = 0
        for column in range(8):
            if turns == 0:
                if column % 2 == 0:
                    p.draw.rect(screen, green, [x, y, rect_size, rect_size])

                else:
                    p.draw.rect(screen, white, [x, y, rect_size, rect_size])

            else:
                if column % 2 == 0:
                    p.draw.rect(screen, white, [x, y, rect_size, rect_size])

                else:
                    p.draw.rect(screen, green, [x, y, rect_size, rect_size])
            x += rect_size

        turns = not turns
        y += rect_size


def place_select():
    for event in p.event.get():
        if event.type == p.QUIT:
            global exit_game
            exit_game = True

        if event.type == p.MOUSEBUTTONDOWN:
            # print(event)
            position = event.__getattribute__("pos")
            global c
            global r
            c = position[0] // 64
            r = position[1] // 64

            print("Row: ", r)
            print("Column: ", c)


def place_pieces():
    for i in range(8):
        for j in range(8):
            obj = chess_board[i][j]
            if obj is not None:
                screen.blit(obj.image, ((obj.col+0.17) * 64, (obj.row+0.17) * 64))


def possible_moves(valid_moves, color):
    if len(valid_moves) == 0:
        return

    else:
        for c, r in valid_moves:
            p.draw.circle(screen, color, ((c + 0.5) * 64, (r + 0.5) * 64), 5)


# def text_screen(text, color, x, y):
#     screen_text = font.render(text, True, color)
#     screen.blit(screen_text, [x, y])


def Update_Pawn(ob):
    global exit_game
    global turn

    print("1.Queen  2.Rook  3.Bishop  4.Knight")

    a = int(input("Enter The Number: "))

    if a == 1:
        chess_board[ob.row][ob.col] = None
        q = Queen(ob.col, ob.row, ob.color)
        chess_board[ob.row][ob.col] = q
        return q
        # print("Pawn Row: ", r)
        # print("Pawn Column: ", c)

    elif a == 2:
        chess_board[ob.row][ob.col] = None
        roo = Rook(ob.col, ob.row, ob.color)
        chess_board[ob.row][ob.col] = roo
        return roo
        # print("Pawn Row: ", r)
        # print("Pawn Column: ", c)

    elif a == 3:
        chess_board[ob.row][ob.col] = None
        b = Bishops(ob.col, ob.row, ob.color)
        chess_board[ob.row][ob.col] = b
        return b
        # print("Pawn Row: ", r)
        # print("Pawn Column: ", c)

    elif a == 4:
        chess_board[ob.row][ob.col] = None
        k = Knight(ob.col, ob.row, ob.color)
        chess_board[ob.row][ob.col] = k
        return k
        # print("Pawn Row: ", r)
        # print("Pawn Column: ", c)


def update_locations(co, ro, obj):
    global turn
    global exit_game

    obj1 = None
    if chess_board[ro][co] is not None:
        obj1 = chess_board[ro][co]

    col = obj.col
    row = obj.row

    obj.row = ro
    obj.col = co

    chess_board[row][col] = None
    chess_board[ro][co] = obj

    che = Check(obj.color)
    che.opposite_pieces_move()
    # print(che.valid_move)
    if che.check:
        print("It Check")
        obj.row = row
        obj.col = col
        chess_board[row][col] = obj
        if obj1 is not None:
            chess_board[ro][co] = obj1

        else:
            chess_board[ro][co] = None

    else:
        print("Not Check")
        if obj.name == 'King':
            # print("Yes")
            if((co == 1 and ro == 0 and chess_board[0][0] is not None and chess_board[0][0].name == 'Rook')
               or (co == 1 and ro == 7 and chess_board[7][0] is not None and chess_board[7][0].name == 'Rook')):
                rook = chess_board[ro][0]
                rook_row = rook.row
                rook_col = rook.col
                # print("Rook Row: ", rook_row)
                # print("Rook Col: ", rook_col)
                rook.row = ro
                rook.col = 2
                chess_board[ro][2] = rook
                chess_board[rook_row][0] = None

            elif((co == 5 and ro == 0 and chess_board[0][7] is not None and chess_board[0][7].name == 'Rook')
                 or (co == 5 and ro == 7 and chess_board[7][7] is not None and chess_board[7][7].name == 'Rook')):
                rook = chess_board[ro][7]
                rook_row = rook.row
                rook_col = rook.col
                # print("Rook Row: ", rook_row)
                # print("Rook Col: ", rook_col)
                rook.row = ro
                rook.col = 4
                chess_board[ro][4] = rook
                chess_board[rook_row][7] = None

        obj.is_moved = True

        if obj.color == 'white':
            black_che = Check('black')
            black_che.is_in_check()
            if black_che.checkmate:
                print("White is Win")
                exit_game = True

            turn = 1

        elif obj.color == 'black':
            white_che = Check('white')
            white_che.is_in_check()
            if white_che.checkmate:
                print("Black is Win")
                exit_game = True

            turn = 0


class Current:
    def __init__(self):
        self.piece = None
        self.valid_move = []
        self.co = -1
        self.ro = -1

    def update_details(self, ob, valid_moves):
        self.piece = ob
        self.valid_move = valid_moves

    def set_col_row(self,c, r):
        self.co = c
        self.ro = r


curr = Current()


if __name__ == '__main__':
    initialize_class()
    # print(chess_board)

    while not exit_game:
        screen.fill(black)
        draw_rectangular()
        place_pieces()

        place_select()

        color = None
        piece = None

        if turn == 0:
            obj = chess_board[r][c]
            if obj is not None and obj.color == 'white':
                if obj.name == 'King':
                    che = Check(obj.color)
                    che.opposite_pieces_move()
                    valid_moves = obj.available_moves(che.valid_move)

                else:
                    valid_moves = obj.available_moves()

                curr.update_details(obj, valid_moves)
                p.draw.rect(screen, blue, [c * 64, r * 64, rect_size, rect_size], 2)

            possible_moves(curr.valid_move, 'red')
            # print(curr.valid_move)
            # print(curr.piece)

            if (c, r) in curr.valid_move:
                # print("Yes")
                # update_locations(c, r, curr.piece)
                # curr.update_details(None, [])
                if curr.piece.name == 'Pawn' and (r == 0 or r == 7):
                    oj = Update_Pawn(curr.piece)
                    update_locations(c, r, oj)
                    curr.update_details(None, [])

                else:
                    update_locations(c, r, curr.piece)
                    curr.update_details(None, [])

            elif (c, r) not in curr.valid_move and obj is None:
                curr.update_details(None, [])

        else:
            obj = chess_board[r][c]
            if obj is not None and obj.color == 'black':
                if obj.name == 'King':
                    che = Check(obj.color)
                    che.opposite_pieces_move()
                    valid_moves = obj.available_moves(che.valid_move)

                else:
                    valid_moves = obj.available_moves()

                curr.update_details(obj, valid_moves)
                p.draw.rect(screen, blue, [c * 64, r * 64, rect_size, rect_size], 2)

            possible_moves(curr.valid_move, 'black')
            # print(curr.valid_move)
            # print(curr.piece)

            if (c, r) in curr.valid_move:
                # print("Yes")
                # update_locations(c, r, curr.piece)
                # curr.update_details(None, [])
                if curr.piece.name == 'Pawn' and (r == 0 or r == 7):
                    oj = Update_Pawn(curr.piece)
                    update_locations(c, r, oj)
                    curr.update_details(None, [])

                else:
                    update_locations(c, r, curr.piece)
                    curr.update_details(None, [])

            elif (c, r) not in curr.valid_move and obj is None:
                curr.update_details(None, [])

        p.display.update()
        clock.tick(fps)

    p.display.quit()
    quit()
