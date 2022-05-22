class Piece:
    def __init__(self):
        pass

    @staticmethod
    def checkBoundaries(row, col):
        """
        checks if a square is inside the 8x8 board
        :param(int) row: row of the square
        :param(int) col: col of the square
        :return(bool): if the square is inside boundary (valid square)
        """
        return 0 <= row <= 7 and 0 <= col <= 7

    @staticmethod
    def checkColorTurn(color, color_to_move):
        """
        checks if the right colored piece wants to move when choosing a piece
        :param(str) color: color of the chosen piece
        :param(bool) color_to_move: bool that determines if it is whites turn
        :return(bool): True if right piece is to move
        """
        return color == color_to_move

    @staticmethod
    def checkCapturedColor(color_of_moved, color_of_captured):
        return color_of_moved != color_of_captured

    @staticmethod
    def checkOccupied(row, col, game_state):
        """
        checks if a square is occupied and return True if it is
        :param(int) row: row of the square
        :param(int) col: col of the square
        :param game_state: the whole board with the current pieces as an 8x8 matrix
        :return(bool): if square is occupied
        """
        return game_state[row, col] is not None


class King(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 100
        self.was_moved = False

    def getLegalMoves(self, game_state, color_to_move):
        legal_moves = []
        if self.checkColorTurn(self.color, color_to_move):
            rows_add = [1, -1, 0, 0, 1, 1, -1, -1]
            cols_add = [0, 0, 1, -1, 1, -1, 1, -1]
            # iterate through two lists
            for row_add, col_add in zip(rows_add, cols_add):
                new_row = self.row+row_add
                new_col = self.col+col_add
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                    else:
                        legal_moves.append([new_row, new_col])
        return legal_moves

    def addCastlingMoves(self, player_color, game_state, pieces_list, legal_moves):
        if not self.was_moved:
            rook_short = None
            rook_long = None
            if player_color == 'w':
                # get rooks
                for piece in pieces_list:
                    if piece.name[1] == 'R' and piece.name[2] == '2' and piece.color == self.color:
                        rook_short = piece
                    if piece.name[1] == 'R' and piece.name[2] == '1' and piece.color == self.color:
                        rook_long = piece
                cols_short = [1, 2]
                cols_long = [-1, -2, -3]
            else:
                # get rooks
                for piece in pieces_list:
                    if piece.name[1] == 'R' and piece.name[2] == '2' and piece.color == self.color:
                        rook_long = piece
                    if piece.name[1] == 'R' and piece.name[2] == '1' and piece.color == self.color:
                        rook_short = piece
                cols_long = [1, 2]
                cols_short = [-1, -2, -3]

            if rook_short:
                if not rook_short.was_moved:
                    short_occupied = False
                    for col_short in cols_short:
                        new_col = self.col + col_short
                        if self.checkOccupied(self.row, new_col, game_state):
                            short_occupied = True
                    if not short_occupied:
                        if player_color == 'w':
                            legal_moves.append([self.row, self.col + 2])
                        else:
                            legal_moves.append([self.row, self.col - 2])

            if rook_long:
                if not rook_long.was_moved:
                    long_occupied = False
                    for col_long in cols_long:
                        new_col = self.col + col_long
                        if self.checkOccupied(self.row, new_col, game_state):
                            long_occupied = True
                    if not long_occupied:
                        if player_color == 'w':
                            legal_moves.append([self.row, self.col - 2])
                        else:
                            legal_moves.append([self.row, self.col + 2])
        return legal_moves


class Queen(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 9
        self.was_moved = False

    def getLegalMoves(self, game_state, color_to_move):
        legal_moves = []
        if self.checkColorTurn(self.color, color_to_move):
            # copied from Rook
            # move right until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col + 1 + i
                new_row = self.row
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move left until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col - 1 - i
                new_row = self.row
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move down until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col
                new_row = self.row + 1 + i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move up until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col
                new_row = self.row - 1 - i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # copied from Bishop
            # move right up until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col + 1 + i
                new_row = self.row - 1 - i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move right down until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col + 1 + i
                new_row = self.row + 1 + i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move left up until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col - 1 - i
                new_row = self.row - 1 - i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move left down until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col - 1 - i
                new_row = self.row + 1 + i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
        return legal_moves


class Rook(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 5
        self.was_moved = False

    def getLegalMoves(self, game_state, color_to_move):
        legal_moves = []
        if self.checkColorTurn(self.color, color_to_move):
            # move right until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col+1+i
                new_row = self.row
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move left until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col-1-i
                new_row = self.row
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move down until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col
                new_row = self.row+1+i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move up until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col
                new_row = self.row-1-i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
        return legal_moves


class Knight(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 3
        self.was_moved = False

    def getLegalMoves(self, game_state, color_to_move):
        legal_moves = []
        start_pos = [self.row, self.col]
        if self.checkColorTurn(self.color, color_to_move):
            # move two squares in each direction
            rows_add = [2, -2, 0, 0]
            cols_add = [0, 0, 2, -2]
            # move one squares left or right
            adds_2 = [1, -1]
            for row_add, col_add in zip(rows_add, cols_add):
                if col_add == 0:
                    for add_2 in adds_2:
                        new_row = self.row + row_add
                        new_col = self.col + col_add + add_2
                        if self.checkBoundaries(new_row, new_col):
                            if self.checkOccupied(new_row, new_col, game_state):
                                if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                                    legal_moves.append([new_row, new_col])
                            else:
                                legal_moves.append([new_row, new_col])
                elif row_add == 0:
                    for add_2 in adds_2:
                        new_row = self.row + row_add + add_2
                        new_col = self.col + col_add
                        if self.checkBoundaries(new_row, new_col):
                            if self.checkOccupied(new_row, new_col, game_state):
                                if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                                    legal_moves.append([new_row, new_col])
                            else:
                                legal_moves.append([new_row, new_col])
        return legal_moves


class Bishop(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 3
        self.was_moved = False

    def getLegalMoves(self, game_state, color_to_move):
        legal_moves = []
        if self.checkColorTurn(self.color, color_to_move):
            # move right up until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col + 1 + i
                new_row = self.row - 1 - i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move right down until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col + 1 + i
                new_row = self.row + 1 + i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move left up until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col - 1 - i
                new_row = self.row - 1 - i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
            # move left down until other piece or boundary
            for i in range(7):  # maximum
                new_col = self.col - 1 - i
                new_row = self.row + 1 + i
                if self.checkBoundaries(new_row, new_col):
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                            break
                        else:
                            break
                    else:
                        legal_moves.append([new_row, new_col])
                else:
                    break
        return legal_moves


class Pawn(Piece):
    def __init__(self, row, col, color, name, start_row):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.start_row = start_row
        self.value = 1
        self.was_moved = False

    def getLegalMoves(self, game_state, color_to_move):
        legal_moves = []
        # TODO: add en passant
        if self.checkColorTurn(self.color, color_to_move):
            if self.start_row == 1:
                if self.row == self.start_row:
                    for i in range(2):
                        new_row = self.row+i+1
                        new_col = self.col
                        if self.checkBoundaries(new_row, new_col):
                            if not self.checkOccupied(new_row, new_col, game_state):  # only move to empty squares when moving straight
                                legal_moves.append([new_row, new_col])
                            else:
                                break
                else:
                    new_row = self.row+1
                    new_col = self.col
                    if self.checkBoundaries(new_row, new_col):
                        if not self.checkOccupied(new_row, new_col, game_state):  # only move to empty squares when moving straight
                            legal_moves.append([new_row, new_col])
                # capture
                rows_add = [1, 1]
                cols_add = [1, -1]
                for row_add, col_add in zip(rows_add, cols_add):
                    new_row = self.row+row_add
                    new_col = self.col+col_add
                    if self.checkBoundaries(new_row, new_col):
                        if self.checkOccupied(new_row, new_col, game_state):  # diagonal is only allowed when enemy captured
                            if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                                legal_moves.append([new_row, new_col])

            elif self.start_row == 6:
                if self.row == self.start_row:
                    for i in range(2):
                        new_row = self.row-i-1
                        new_col = self.col
                        if self.checkBoundaries(new_row, new_col):
                            if not self.checkOccupied(new_row, new_col, game_state):  # only move to empty squares when moving straight
                                legal_moves.append([new_row, new_col])
                            else:
                                break
                else:
                    new_row = self.row-1
                    new_col = self.col
                    if self.checkBoundaries(new_row, new_col):
                        if not self.checkOccupied(new_row, new_col, game_state):  # only move to empty squares when moving straight
                            legal_moves.append([new_row, new_col])
                # capture
                rows_add = [-1, -1]
                cols_add = [1, -1]
                for row_add, col_add in zip(rows_add, cols_add):
                    new_row = self.row + row_add
                    new_col = self.col + col_add
                    if self.checkBoundaries(new_row, new_col):
                        if self.checkOccupied(new_row, new_col, game_state):  # diagonal is only allowed when enemy captured
                            if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                                legal_moves.append([new_row, new_col])
        return legal_moves
