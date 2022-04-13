class Piece:
    def __init__(self):
        pass

    @staticmethod
    def checkBoundaries(new_row, new_col):
        return 0 <= new_row <= 7 and 0 <= new_col <= 7

    @staticmethod
    def checkColorTurn(color, white_to_move):
        return (color == 'w' and white_to_move) or (color == 'b' and not white_to_move)

    @staticmethod
    def checkCapturedColor(color_of_moved, color_of_captured):
        return color_of_moved != color_of_captured

    @staticmethod
    def checkOccupied(new_row, new_col, game_state):
        return game_state[new_row, new_col] is not None


class King(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 100

    def getLegalMoves(self, game_state, white_to_move):
        legal_moves = []
        start_pos = [self.row, self.col]
        if self.checkColorTurn(self.color, white_to_move):
            rows_add = [1, -1, 0, 0, 1, 1, -1, -1]
            cols_add = [0, 0, 1, -1, 1, -1, 1, -1]
            # iterate through two lists
            for row_add, col_add in zip(rows_add, cols_add):
                new_row = self.row+row_add
                new_col = self.col+col_add
                if self.checkBoundaries(new_row, new_col):
                    # TODO: check if the move would result in a check (check if this square is a legal move for all other pieces)
                    if self.checkOccupied(new_row, new_col, game_state):
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
                    else:
                        legal_moves.append([new_row, new_col])
        return start_pos, legal_moves


class Queen(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 9

    def getLegalMoves(self, game_state, white_to_move):
        legal_moves = []
        start_pos = [self.row, self.col]
        if self.checkColorTurn(self.color, white_to_move):
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
        return start_pos, legal_moves


class Rook(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 5

    def getLegalMoves(self, game_state, white_to_move):
        legal_moves = []
        start_pos = [self.row, self.col]
        if self.checkColorTurn(self.color, white_to_move):
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
        return start_pos, legal_moves


class Knight(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 3

    def getLegalMoves(self, game_state, white_to_move):
        legal_moves = []
        start_pos = [self.row, self.col]
        if self.checkColorTurn(self.color, white_to_move):
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
        return start_pos, legal_moves


class Bishop(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 3

    def getLegalMoves(self, game_state, white_to_move):
        legal_moves = []
        start_pos = [self.row, self.col]
        if self.checkColorTurn(self.color, white_to_move):
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
        return start_pos, legal_moves


class Pawn(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.start_row = row
        self.value = 1

    def getLegalMoves(self, game_state, white_to_move):
        legal_moves = []
        start_pos = [self.row, self.col]
        # TODO: add en passant
        if self.checkColorTurn(self.color, white_to_move):
            if self.start_row == 1:
                if self.row == self.start_row:
                    for i in range(2):
                        new_row = self.row+i+1
                        new_col = self.col
                        if self.checkBoundaries(new_row, new_col):
                            if not game_state[new_row][new_col]:  # only move to empty squares when moving straight
                                legal_moves.append([new_row, new_col])
                else:
                    new_row = self.row+1
                    new_col = self.col
                    if self.checkBoundaries(new_row, new_col):
                        if not game_state[new_row][new_col]:  # only move to empty squares when moving straight
                            legal_moves.append([new_row, new_col])
                # capture
                new_row = self.row+1
                new_col = self.col+1
                if self.checkBoundaries(new_row, new_col):
                    if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                        legal_moves.append([new_row, new_col])

            elif self.start_row == 6:
                if self.row == self.start_row:
                    for i in range(2):
                        new_row = self.row-i-1
                        new_col = self.col
                        if self.checkBoundaries(new_row, new_col):
                            if not game_state[new_row][new_col]:  # only move to empty squares when moving straight
                                legal_moves.append([new_row, new_col])
                else:
                    new_row = self.row-1
                    new_col = self.col
                    if self.checkBoundaries(new_row, new_col):
                        if not game_state[new_row][new_col]:  # only move to empty squares when moving straight
                            legal_moves.append([new_row, new_col])
                # capture
                new_row = self.row-1
                new_col = self.col-1
                if self.checkBoundaries(new_row, new_col):
                    if game_state[new_row][new_col]:  # diagonal is only allowed when enemy captured
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])
        return start_pos, legal_moves
