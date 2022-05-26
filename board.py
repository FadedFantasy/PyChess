import pygame as p
import numpy as np
from pieces import King, Queen, Pawn, Bishop, Knight, Rook, Piece
import copy


class Board:
    def __init__(self, window_width, window_height, player_color):
        self.width = window_width
        self.height = window_height
        self.sq_size = self.height // 8
        self.player_color = player_color
        self.game_state = self.initializeBoard()
        self.images = self.loadImages()
        self.pieces = self.initializePiecesAndReplaceGameState()
        self.color_to_move = 'w'
        self.b_king = None
        self.w_king = None
        self.move_log = []
        self.eval = 0.0

    def loadImages(self):
        """
        Initialize a global dict of images. This will be called exactly once
        """
        pieces_str = ['wp', 'wR', 'wN', 'wK', 'wQ', 'wB', 'bp', 'bR', 'bN', 'bK', 'bQ', 'bB']
        images = {}
        for piece_str in pieces_str:
            # transform scale: scales the image to (width, height)
            images[piece_str] = p.transform.scale(p.image.load(r'images/' + piece_str + '.png'), (self.sq_size, self.sq_size))
        return images

    def initializeBoard(self):
        if self.player_color == 'b':
            board = np.array([
                ['wR1', 'wN1', 'wB1', 'wK1', 'wQ1', 'wB2', 'wN2', 'wR2'],
                ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
                ['bR1', 'bN1', 'bB1', 'bK1', 'bQ1', 'bB2', 'bN2', 'bR2']
            ])
        else:  # white or multiplayer
            board = np.array([
                ['bR1', 'bN1', 'bB1', 'bQ1', 'bK1', 'bB2', 'bN2', 'bR2'],
                ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
                ['wR1', 'wN1', 'wB1', 'wQ1', 'wK1', 'wB2', 'wN2', 'wR2']
            ])
        return board

    def initializePiecesAndReplaceGameState(self):
        """
        pieces is a list that contains all piece objects/instances. Additionally, the game_state is updated the
        these objects instead of strings
        """
        pieces = []
        for row in range(self.game_state.shape[0]):
            for col in range(self.game_state.shape[1]):
                # everything that is not None
                if self.game_state[row][col]:
                    # second letter
                    if self.game_state[row][col][1] == 'p':
                        piece = Pawn(row, col, self.game_state[row][col][0], self.game_state[row][col], row)
                    elif self.game_state[row][col][1] == 'R':
                        piece = Rook(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'N':
                        piece = Knight(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'B':
                        piece = Bishop(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'K':
                        piece = King(row, col, self.game_state[row][col][0], self.game_state[row][col])
                        if self.game_state[row][col][0] == 'w':
                            self.w_king = piece
                        else:
                            self.b_king = piece
                    elif self.game_state[row][col][1] == 'Q':
                        piece = Queen(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    self.game_state[row][col] = piece
                    pieces.append(piece)
        return pieces

    def drawGameState(self, screen, start_pos, legal_moves):
        """
        controls the drawing work flow
        """
        self.drawSquares(screen)
        self.drawPieces(screen)
        if start_pos:
            self.drawFirstClickPos(screen, start_pos)
        if legal_moves:
            self.drawLegalMoves(screen, legal_moves)

    def drawSquares(self, screen):
        """
        draws the squares on board
        """
        colors = [p.Color('white'), p.Color('gray')]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                p.draw.rect(screen, color, p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def drawPieces(self, screen):
        """
        draws the pieces on the board using current game_state
        """
        for row in range(8):
            for col in range(8):
                piece = self.game_state[row][col]
                if piece:  # not an empty square
                    screen.blit(self.images[piece.name[:2]], p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def drawLegalMoves(self, screen, legal_moves):
        for legal_move in legal_moves:
            p.draw.circle(screen, [189, 0, 0], ((legal_move[1] * self.sq_size)+self.sq_size//2, (legal_move[0] * self.sq_size)+self.sq_size//2), self.sq_size//2, 3)

    def drawFirstClickPos(self, screen,  start_pos):
        p.draw.rect(screen, [189, 0, 0],
                    p.Rect(start_pos[1] * self.sq_size, start_pos[0] * self.sq_size, self.sq_size, self.sq_size), 3)

    def changeMovingColor(self):
        if self.color_to_move == 'w':
            self.color_to_move = 'b'
        else:
            self.color_to_move = 'w'

    def firstClickSelect(self):
        location = p.mouse.get_pos()  # (x,y) location of mouse
        col = location[0] // self.sq_size
        row = location[1] // self.sq_size
        square_name = self.getSquareName(row, col)
        pos = []
        piece = None
        legal_moves = []
        # select piece to move and piece is right color
        if Piece.checkOccupied(row, col, self.game_state) and self.game_state[row][col].color == self.color_to_move:
            pos = [row, col]
            piece = self.game_state[row][col]
            legal_moves = piece.getLegalMoves(self.game_state, self.color_to_move, self.move_log)
            if piece.name[1] == 'K':
                if self.color_to_move == 'w':
                    color_attacking = 'b'
                else:
                    color_attacking = 'w'
                if not self.isCheck(color_attacking):
                    legal_moves = piece.addCastlingMoves(self.player_color, self.game_state, self.pieces, legal_moves)
            legal_moves = self.checkKingCapture(legal_moves, piece)
            print(f'Piece to move: {piece}')
            print(f'Piece name: {piece.name}, Piece row: {piece.row}, Piece col: {piece.col}')
            print(f'legal_moves = {legal_moves}')
            print(f'Square name of selected piece: {square_name}')
        else:
            print(f'Square name of selected square: {square_name}')
        return pos, piece, legal_moves

    def secondClickSelect(self, legal_moves):
        location = p.mouse.get_pos()  # (x,y) location of mouse
        col = location[0] // self.sq_size
        row = location[1] // self.sq_size
        square_name = self.getSquareName(row, col)
        end_pos = []
        is_move = False
        if [row, col] in legal_moves:
            end_pos = [row, col]
            is_move = True
        print(f'Square name of end position square: {square_name}')
        return end_pos, is_move

    def performMove(self, piece, start_pos, end_pos):
        # pawn
        if piece.name[1] == 'p':
            # promote
            if end_pos[0] == 7 or end_pos[0] == 0:
                piece = Queen(end_pos[0], end_pos[1], piece.color, f'{piece.color}Q2')
            # en passant
            if not Piece.checkOccupied(end_pos[0], end_pos[1], self.game_state) and end_pos[1] != start_pos[1]:
                if piece.start_row == 1:
                    self.game_state[end_pos[0]-1][end_pos[1]] = None
                elif piece.start_row == 6:
                    self.game_state[end_pos[0]+1][end_pos[1]] = None
        # set move flag for castling
        piece.was_moved = True

        # move
        self.game_state[start_pos[0]][start_pos[1]] = None
        piece.row = end_pos[0]
        piece.col = end_pos[1]
        self.game_state[end_pos[0]][end_pos[1]] = piece

        # if king castling moves rook
        if piece.name[1] == 'K' and abs(start_pos[1]-end_pos[1]) > 1:
            rook, dir_of_king = self.getClosestRookToKing(piece)
            rook_initial_pos = [rook.row, rook.col]
            self.game_state[rook.row][rook.col] = None
            if dir_of_king == 'right':
                rook.row = piece.row
                rook.col = piece.col - 1
            if dir_of_king == 'left':
                rook.row = piece.row
                rook.col = piece.col + 1
            self.game_state[rook.row][rook.col] = rook
            self.move_log.append([piece.name, start_pos, end_pos, rook.name, rook_initial_pos, [rook.row, rook.col]])
        else:
            self.move_log.append([piece.name, start_pos, end_pos])

    def evaluatePosition(self):
        w_eval = 0
        b_eval = 0
        for piece in self.pieces:
            if piece.color == 'w':
                w_eval += piece.value
            else:
                b_eval += piece.value
        self.eval = w_eval-b_eval
        print(f'Evaluation: {self.eval}')

    def getClosestRookToKing(self, king):
        dir_of_king = ''
        rook = None
        for piece in self.pieces:
            if piece.name[1] == 'R' and piece.row == king.row:
                if abs(piece.col-king.col) <= 2:
                    if piece.col-king.col > 0:
                        dir_of_king = 'right'
                    else:
                        dir_of_king = 'left'
                    rook = piece
        return rook, dir_of_king

    def updatePiecesList(self):
        """
        Updates the pieces list that is used as a class variable
        :return:
        """
        self.pieces = []
        for row in range(self.game_state.shape[0]):
            for col in range(self.game_state.shape[1]):
                # everything that is not None
                if self.game_state[row][col]:
                    self.pieces.append(self.game_state[row][col])
                    if self.game_state[row][col].name[1] == 'K' and self.game_state[row][col].name[0] == 'w':
                        self.w_king = self.game_state[row][col]
                    if self.game_state[row][col].name[1] == 'K' and self.game_state[row][col].name[0] == 'b':
                        self.b_king = self.game_state[row][col]

    @staticmethod
    def updatePiecesListSimulated(game_state):
        """
        Updates the pieces list that is used as a class variable for a simulated move
        :return:
        """
        pieces = []
        for row in range(game_state.shape[0]):
            for col in range(game_state.shape[1]):
                # everything that is not None
                if game_state[row][col]:
                    pieces.append(game_state[row][col])
        return pieces

    def checkKingCapture(self, legal_moves, piece_to_move):
        """
        Removes the legal_moves that would result in a king capture. For that every move of legal moves will be
        simulated on a copy of self.game_state, self.pieces and the piece that would move (piece_to_move).
        Afterwards it will be checked if any legal_move of the enemy would result in a king capture
        :return:
        """
        # create deep copies of self.pieces and self.game_state to simulate the move
        piece_to_move_copy = copy.deepcopy(piece_to_move)
        legal_moves_copy = copy.deepcopy(legal_moves)

        for move in legal_moves:
            game_state_copy = copy.deepcopy(self.game_state)
            piece_to_move_copy = copy.deepcopy(piece_to_move)
            game_state_copy[piece_to_move_copy.row][piece_to_move_copy.col] = None
            piece_to_move_copy.row = move[0]
            piece_to_move_copy.col = move[1]
            game_state_copy[move[0]][move[1]] = piece_to_move_copy
            pieces_copy = self.updatePiecesListSimulated(game_state_copy)

            # get pos of own king
            for piece_copy_for_king in pieces_copy:
                if piece_copy_for_king.name[1] == 'K' and piece_copy_for_king.color == self.color_to_move:
                    king_pos = [piece_copy_for_king.row, piece_copy_for_king.col]
                    break

            for piece_copy in pieces_copy:
                if not self.color_to_move == piece_copy.color:
                    if self.color_to_move == 'w':
                        color_to_move_copy = 'b'
                    else:
                        color_to_move_copy = 'w'
                    legal_moves_piece = piece_copy.getLegalMoves(game_state_copy, color_to_move_copy, self.move_log)
                    if piece_copy.name[1] == 'K':
                        legal_moves_piece = piece_copy.addCastlingMoves(self.player_color, game_state_copy, pieces_copy, legal_moves_piece)
                    for legal_move_piece in legal_moves_piece:
                        if king_pos == legal_move_piece:
                            if move in legal_moves_copy:
                                # remove all castling move if next to king is illegal
                                if piece_to_move_copy.name[1] == 'K':
                                    if piece_to_move_copy.color == 'b':
                                        initial_col = self.b_king.col
                                        initial_row = self.b_king.row
                                    else:
                                        initial_col = self.w_king.col
                                        initial_row = self.b_king.row
                                    if initial_row == move[0] and abs(initial_col-move[1]) == 1:
                                        if move[1] - initial_col > 0:
                                            move_right = [move[0], move[1]+1]
                                            if move_right in legal_moves_copy:
                                                legal_moves_copy.remove(move_right)
                                        else:
                                            move_left = [move[0], move[1]-1]
                                            if move_left in legal_moves_copy:
                                                legal_moves_copy.remove(move_left)
                                legal_moves_copy.remove(move)
        return legal_moves_copy

    def isCheck(self, color_attacking):
        # get enemy king pos
        if color_attacking == 'w':
            enemy_king_pos = [self.b_king.row, self.b_king.col]
        else:
            enemy_king_pos = [self.w_king.row, self.w_king.col]
        for piece in self.pieces:
            if color_attacking == piece.color:
                legal_moves = piece.getLegalMoves(self.game_state, color_attacking, self.move_log)
                if piece.name[1] == 'K':
                    legal_moves = piece.addCastlingMoves(self.player_color, self.game_state, self.pieces, legal_moves)
                legal_moves = self.checkKingCapture(legal_moves, piece)
                if enemy_king_pos in legal_moves:
                    return True
        return False

    def checkCheckmate(self):
        legal_moves_all = []
        if self.color_to_move == 'w':
            color_attacking = 'b'
            color_defending = 'w'
        else:
            color_attacking = 'w'
            color_defending = 'b'
        for piece in self.pieces:
            if color_defending == piece.color:
                legal_moves = piece.getLegalMoves(self.game_state, color_defending, self.move_log)
                if piece.name[1] == 'K':
                    legal_moves = piece.addCastlingMoves(self.player_color, self.game_state, self.pieces, legal_moves)
                legal_moves = self.checkKingCapture(legal_moves, piece)
                legal_moves_all.extend(legal_moves)
        if not legal_moves_all:
            if self.isCheck(color_attacking):
                print(f'GAME OVER! {color_attacking} won by checkmate')
            else:
                print(f'GAME OVER! It is a stalemate')

    def getSquareName(self, row, col):
        if self.player_color == 'b':
            rows_to_ranks = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}
            cols_to_files = {0: 'h', 1: 'g', 2: 'f', 3: 'e', 4: 'd', 5: 'c', 6: 'b', 7: 'a'}
        else:
            rows_to_ranks = {7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7, 0: 8}
            cols_to_files = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        return cols_to_files[col] + str(rows_to_ranks[row])


