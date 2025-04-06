class Move:
    """
    Represents a chess move with all necessary information.
    """

    def __init__(self, from_pos, to_pos, piece, captured=None, promotion=None,
                 is_castling=False, is_en_passant=False, castling_rook_move=None):
        self.from_pos = from_pos  # (row, col) tuple
        self.to_pos = to_pos  # (row, col) tuple
        self.piece = piece  # Character representation of the piece (FEN style)
        self.captured = captured  # Captured piece, if any
        self.promotion = promotion  # Piece to promote to, if any
        self.is_castling = is_castling  # Flag for castling moves
        self.is_en_passant = is_en_passant  # Flag for en passant captures
        self.castling_rook_move = castling_rook_move  # Additional rook move for castling

    def __str__(self):
        """Convert move to algebraic notation."""
        files = 'abcdefgh'
        ranks = '87654321'  # Reversed because chess board row 0 is rank 8

        from_file = files[self.from_pos[1]]
        from_rank = ranks[self.from_pos[0]]
        to_file = files[self.to_pos[1]]
        to_rank = ranks[self.to_pos[0]]

        # Special notations
        if self.is_castling:
            if self.to_pos[1] > self.from_pos[1]:
                return "O-O"  # Kingside castling
            else:
                return "O-O-O"  # Queenside castling

        # Standard notation
        move_str = f"{from_file}{from_rank}{to_file}{to_rank}"

        # Add promotion if applicable
        if self.promotion:
            move_str += f"={self.promotion.upper()}"

        return move_str
