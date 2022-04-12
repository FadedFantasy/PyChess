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
        if self.checkColorTurn(self.color, white_to_move):
            rows_add = [1, -1, 0, 0, 1, 1, -1, -1]
            cols_add = [0, 0, 1, -1, 1, -1, 1, -1]
            # iterate through two lists
            for row_add, col_add in zip(rows_add, cols_add):
                new_row = self.row+row_add
                new_col = self.col+col_add
                if self.checkBoundaries(new_row, new_col):
                    # TOO: check if the move would result in a check (check if this square is a legal move for all other pieces)
                    if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                        legal_moves.append([new_row, new_col])
        return legal_moves


class Queen(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 9

    def getLegalMoves(self, game_state):
        legal_moves = []
        return legal_moves


class Rook(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 5

    def getLegalMoves(self, game_state):
        legal_moves = []
        return legal_moves


class Knight(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 3

    def getLegalMoves(self, game_state):
        legal_moves = []
        return legal_moves


class Bishop(Piece):
    def __init__(self, row, col, color, name):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.value = 3

    def getLegalMoves(self, game_state):
        legal_moves = []
        return legal_moves


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

                new_row = self.row-1
                new_col = self.col-1
                if self.checkBoundaries(new_row, new_col):
                    if game_state[new_row][new_col]:  # diagonal is only allowed when enemy captured
                        if self.checkCapturedColor(game_state[new_row][new_col].color, self.color):
                            legal_moves.append([new_row, new_col])

        return legal_moves
