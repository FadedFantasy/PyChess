from abc import ABC, abstractmethod


class BaseBoard(ABC):
    """
    Abstract base class defining the interface for chess board representations.
    Uses FEN-style piece notation:
    - 'P', 'p' = white/black pawn
    - 'N', 'n' = white/black knight
    - 'B', 'b' = white/black bishop
    - 'R', 'r' = white/black rook
    - 'Q', 'q' = white/black queen
    - 'K', 'k' = white/black king
    """

    @abstractmethod
    def initialize(self):
        """Set up the initial position of pieces on the board."""
        pass

    @abstractmethod
    def get_piece(self, position):
        """
        Get the piece at the specified position.

        Args:
            position: A tuple (row, col) specifying the position.

        Returns:
            A character representing the piece (uppercase for white, lowercase for black).
        """
        pass

    @abstractmethod
    def place_piece(self, piece, position):
        """
        Place a piece at the specified position.

        Args:
            piece: A character representing the piece.
            position: A tuple (row, col) specifying the position.
        """
        pass

    @abstractmethod
    def make_move(self, move):
        """
        Execute a move on the board.

        Args:
            move: A Move object representing the move to make.
        """
        pass

    @abstractmethod
    def get_legal_moves(self, position=None):
        """
        Get all legal moves for the specified position or for all pieces of the current player.

        Args:
            position: Optional tuple (row, col) specifying the position.
                     If None, return all legal moves for the current player.

        Returns:
            A list of Move objects representing legal moves.
        """
        pass

    @abstractmethod
    def get_board_state(self):
        """
        Get the current state of the board for display or evaluation.

        Returns:
            A representation of the board state.
        """
        pass

    @abstractmethod
    def is_check(self, color):
        """
        Check if the king of the specified color is in check.

        Args:
            color: 'w' for white, 'b' for black.

        Returns:
            True if the king is in check, False otherwise.
        """
        pass

    @abstractmethod
    def get_current_player(self):
        """
        Get the current player.

        Returns:
            'w' for white, 'b' for black.
        """
        pass