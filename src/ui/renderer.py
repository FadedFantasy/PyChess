import pygame
import os
import time
import config
from src.ui.animations import Animation
from src.board.move import Move


class Renderer:
    """
    Main rendering controller for the chess UI.

    This class coordinates all visual aspects of the chess game, including the board,
    pieces, move highlights, annotations, and UI controls.
    """

    def __init__(self, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT):
        """
        Initialize the renderer.

        Args:
            width: Window width in pixels.
            height: Window height in pixels.
        """
        # Initialize pygame
        pygame.init()

        # Set up the display
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Chess Engine')
        self.clock = pygame.time.Clock()

        # Board dimensions and position
        self.board_size = config.BOARD_SIZE
        self.square_size = config.SQUARE_SIZE
        self.board_x = 20
        self.board_y = (height - self.board_size) // 2

        # Annotation panel
        self.annotation_x = self.board_x + self.board_size + 20
        self.annotation_y = self.board_y
        self.annotation_width = width - self.annotation_x - 20
        self.annotation_height = self.board_size

        # Load fonts
        self.fonts = {
            'small': pygame.font.Font(None, 24),
            'medium': pygame.font.Font(None, 28),
            'large': pygame.font.Font(None, 36)
        }

        # Load piece images
        self.piece_images = self._load_piece_images()

        # Create animation manager
        self.animation = Animation()

        # State variables
        self.selected_square = None
        self.move_hints = []
        self.last_move = None
        self.check_square = None
        self.game_state = "playing"  # "playing", "checkmate", "stalemate"

        # Performance tracking
        self.fps = 0
        self.last_time = time.time()
        self.frame_count = 0

    def draw(self, board, annotations=None, eval_info=None):
        """
        Draw everything to the screen.

        Args:
            board: The chess board to draw.
            annotations: Optional text annotations to display.
            eval_info: Optional evaluation information to display.
        """
        # Clear the screen
        self.screen.fill(config.BACKGROUND_COLOR)

        # Draw the board and pieces
        self._draw_board(board)
        self._draw_highlights()
        self._draw_pieces(board)

        # Draw active animations on top
        animations_active = self.animation.update_and_draw(self.screen)

        # Draw annotations panel
        if annotations:
            self._draw_annotations_panel(annotations)

        # Draw evaluation info if available
        if eval_info:
            self._draw_evaluation_info(eval_info)

        # Draw game state message if game is over
        if self.game_state != "playing":
            self._draw_game_over_message(board)

        # Update FPS counter
        self._update_fps()

        # Update the display
        pygame.display.flip()

        # Return whether animations are still running
        return animations_active

    def handle_events(self, board, game_controller):
        """
        Handle pygame events.

        Args:
            board: The chess board to interact with.
            game_controller: Controller for game logic.

        Returns:
            False if the program should exit, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if click was on the board
                x, y = event.pos
                if (self.board_x <= x < self.board_x + self.board_size and
                        self.board_y <= y < self.board_y + self.board_size):
                    # Convert pixel coordinates to board coordinates
                    col = (x - self.board_x) // self.square_size
                    row = 7 - (y - self.board_y) // self.square_size  # Flip row for chess convention

                    # Handle square selection
                    if self.game_state == "playing":
                        self._handle_square_selection(board, game_controller, (row, col))

                # Check if click was on buttons/controls
                else:
                    self._handle_control_click(event.pos, game_controller)

            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selected_square = None
                    self.move_hints = []
                elif event.key == pygame.K_u:
                    # Undo move functionality would go here
                    if hasattr(game_controller, 'undo_move'):
                        game_controller.undo_move()
                        self.animation.clear_animations()

        return True

    def set_selected_square(self, square):
        """
        Set the currently selected square.

        Args:
            square: Tuple (row, col) or None to deselect.
        """
        self.selected_square = square

    def set_move_hints(self, moves):
        """
        Set squares to highlight as move hints.

        Args:
            moves: List of Move objects representing legal moves.
        """
        self.move_hints = moves

    def set_last_move(self, move):
        """
        Set the last move made for highlighting.

        Args:
            move: Move object or None.
        """
        self.last_move = move

        # Add animation for this move
        if move and self.piece_images:
            self.animation.add_move_animation(
                move.piece,
                move.from_pos,
                move.to_pos,
                self.piece_images
            )

    def set_check_square(self, square):
        """
        Set the square in check for highlighting.

        Args:
            square: Tuple (row, col) or None.
        """
        self.check_square = square

    def set_game_state(self, state):
        """
        Set the current game state.

        Args:
            state: "playing", "checkmate", or "stalemate".
        """
        self.game_state = state

    def _load_piece_images(self):
        """
        Load piece images from files.

        Returns:
            Dictionary mapping piece notations to loaded images.
        """
        piece_images = {}
        piece_codes = {
            'P': 'white_pawn',
            'N': 'white_knight',
            'B': 'white_bishop',
            'R': 'white_rook',
            'Q': 'white_queen',
            'K': 'white_king',
            'p': 'black_pawn',
            'n': 'black_knight',
            'b': 'black_bishop',
            'r': 'black_rook',
            'q': 'black_queen',
            'k': 'black_king'
        }

        for code, name in piece_codes.items():
            # Load piece image from file
            image_path = os.path.join(config.PIECE_IMAGES_DIR, f"{name}.png")

            try:
                # Load the image
                image = pygame.image.load(image_path).convert_alpha()

                # Scale image to fit square - Use config value
                new_size = int(self.square_size * config.PIECE_SCALE)
                image = pygame.transform.smoothscale(image, (new_size, new_size))

                # Store in the dictionary
                piece_images[code] = image
            except Exception as e:
                print(f"Error loading piece image {name} from {image_path}: {e}")

        return piece_images

    def _draw_board(self, board):
        """
        Draw the chess board grid.

        Args:
            board: The chess board to draw.
        """
        for row in range(8):
            for col in range(8):
                # Determine square color
                if (row + col) % 2 == 0:
                    color = config.LIGHT_SQUARE
                else:
                    color = config.DARK_SQUARE

                # Calculate square position
                x = self.board_x + col * self.square_size
                y = self.board_y + (7 - row) * self.square_size  # Flip row for chess convention

                # Draw square
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))

                # Draw rank and file labels on the board edges
                if col == 0:  # Left edge - draw rank numbers
                    label = self.fonts['small'].render(str(row + 1), True,
                                                       config.DARK_SQUARE if (row + col) % 2 == 0
                                                       else config.LIGHT_SQUARE)
                    self.screen.blit(label, (x + 2, y + self.square_size - label.get_height() - 2))

                if row == 7:  # Bottom edge - draw file letters
                    label = self.fonts['small'].render(chr(97 + col), True,  # 'a' through 'h'
                                                       config.DARK_SQUARE if (row + col) % 2 == 0
                                                       else config.LIGHT_SQUARE)
                    self.screen.blit(label, (x + self.square_size - label.get_width() - 2,
                                             y + self.square_size - label.get_height() - 2))

    def _draw_pieces(self, board):
        """
        Draw pieces on the board.

        Args:
            board: The chess board containing piece positions.
        """
        # Skip drawing pieces that are currently being animated
        animated_pieces = set()
        for anim in self.animation.active_animations:
            # We don't know the exact board position from the animation
            # This is a simplification - a real implementation would track this better
            animated_pieces.add(anim['piece'])

        # Get the board state
        board_state = board.get_board_state()

        for row in range(8):
            for col in range(8):
                piece = board_state[row][col] if isinstance(board_state[0], list) else board_state[row, col]

                # Skip empty squares or animated pieces
                if piece == ' ' or piece == '':
                    continue

                # Skip pieces that are actively being animated
                skip = False
                if self.last_move:
                    if (row, col) == self.last_move.to_pos and piece == self.last_move.piece:
                        if any(a['piece'] == piece for a in self.animation.active_animations):
                            skip = True

                if skip:
                    continue

                # Calculate position
                x = self.board_x + col * self.square_size
                y = self.board_y + (7 - row) * self.square_size  # Flip row

                # Draw the piece if we have its image
                if piece in self.piece_images:
                    # Center the piece in the square
                    image = self.piece_images[piece]
                    x += (self.square_size - image.get_width()) // 2
                    y += (self.square_size - image.get_height()) // 2

                    # Draw the piece
                    self.screen.blit(image, (x, y))

    def _draw_highlights(self):
        """Draw all board highlights (selected square, move hints, last move, check)."""
        # Draw selected square highlight
        if self.selected_square is not None:
            row, col = self.selected_square
            x = self.board_x + col * self.square_size
            y = self.board_y + (7 - row) * self.square_size  # Flip row
            self._draw_highlight(x, y, config.HIGHLIGHT_COLOR)

        # Draw move hints
        for move in self.move_hints:
            to_row, to_col = move.to_pos
            x = self.board_x + to_col * self.square_size
            y = self.board_y + (7 - to_row) * self.square_size  # Flip row

            # For move hints, draw a circle if empty square, otherwise draw a highlight
            if move.captured is None and not getattr(move, 'is_en_passant', False):
                # Draw circle for empty square move
                center_x = x + self.square_size // 2
                center_y = y + self.square_size // 2
                radius = self.square_size // 6
                # Use alpha circle
                surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, config.MOVE_HINT_COLOR, (radius, radius), radius)
                self.screen.blit(surface, (center_x - radius, center_y - radius))
            else:
                # Draw transparent overlay for captures
                self._draw_highlight(x, y, config.MOVE_HINT_COLOR)

        # Draw last move highlight
        if self.last_move:
            from_row, from_col = self.last_move.from_pos
            to_row, to_col = self.last_move.to_pos

            # From square
            x = self.board_x + from_col * self.square_size
            y = self.board_y + (7 - from_row) * self.square_size  # Flip row
            self._draw_highlight(x, y, config.LAST_MOVE_COLOR)

            # To square
            x = self.board_x + to_col * self.square_size
            y = self.board_y + (7 - to_row) * self.square_size  # Flip row
            self._draw_highlight(x, y, config.LAST_MOVE_COLOR)

        # Draw check highlight
        if self.check_square:
            row, col = self.check_square
            x = self.board_x + col * self.square_size
            y = self.board_y + (7 - row) * self.square_size  # Flip row
            self._draw_highlight(x, y, config.CHECK_COLOR)

    def _draw_highlight(self, x, y, color):
        """
        Draw a highlight overlay on a square.

        Args:
            x: X-coordinate of the square.
            y: Y-coordinate of the square.
            color: Color to use for the highlight.
        """
        # Create transparent surface
        surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (0, 0, self.square_size, self.square_size))
        self.screen.blit(surface, (x, y))

    def _draw_annotations_panel(self, annotations):
        """
        Draw the annotations panel with move history and game info.

        Args:
            annotations: Dictionary with annotation data.
        """
        # Draw panel background
        panel_rect = (self.annotation_x, self.annotation_y,
                      self.annotation_width, self.annotation_height)
        pygame.draw.rect(self.screen, (56, 56, 56), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), panel_rect, 1)

        # Draw title
        title = self.fonts['medium'].render("Game Information", True, config.TEXT_COLOR)
        self.screen.blit(title, (self.annotation_x + 10, self.annotation_y + 10))

        # Draw move history
        history_y = self.annotation_y + 50
        move_history = annotations.get('move_history', [])

        if move_history:
            # Display move history in pairs (white and black)
            for i in range(0, len(move_history), 2):
                move_num = i // 2 + 1
                white_move = move_history[i]
                black_move = move_history[i + 1] if i + 1 < len(move_history) else ""

                text = f"{move_num}. {white_move}  {black_move}"
                move_text = self.fonts['small'].render(text, True, config.TEXT_COLOR)
                self.screen.blit(move_text, (self.annotation_x + 10, history_y))
                history_y += 24

                # If panel is full, show ellipsis and stop
                if history_y > self.annotation_y + self.annotation_height - 30:
                    ellipsis = self.fonts['small'].render("...", True, config.TEXT_COLOR)
                    self.screen.blit(ellipsis, (self.annotation_x + 10, history_y))
                    break
        else:
            # No moves yet
            no_moves = self.fonts['small'].render("No moves yet", True, config.TEXT_COLOR)
            self.screen.blit(no_moves, (self.annotation_x + 10, history_y))

        # Draw status at the bottom of the panel
        status_y = self.annotation_y + self.annotation_height - 30
        status_text = annotations.get('status', "White to move")
        status = self.fonts['small'].render(status_text, True, config.TEXT_COLOR)
        self.screen.blit(status, (self.annotation_x + 10, status_y))

    def _draw_evaluation_info(self, eval_info):
        """
        Draw evaluation information from the engine.

        Args:
            eval_info: Dictionary with evaluation data.
        """
        # Draw at the bottom of the annotation panel
        eval_y = self.annotation_y + self.annotation_height - 60

        # Display evaluation score
        score = eval_info.get('score', 0)
        score_text = f"Evaluation: {score / 100:.2f}" if abs(score) < 10000 else "Mate"
        eval_text = self.fonts['small'].render(score_text, True, config.TEXT_COLOR)
        self.screen.blit(eval_text, (self.annotation_x + 10, eval_y))

        # Display engine depth
        depth = eval_info.get('depth', 0)
        depth_text = self.fonts['small'].render(f"Depth: {depth}", True, config.TEXT_COLOR)
        self.screen.blit(depth_text, (self.annotation_x + 150, eval_y))

        # Display best line if available
        best_line = eval_info.get('best_line', [])
        if best_line:
            line_text = " ".join([str(move) for move in best_line[:3]])
            if line_text:
                line_render = self.fonts['small'].render(f"Best: {line_text}...",
                                                         True, config.TEXT_COLOR)
                self.screen.blit(line_render, (self.annotation_x + 10, eval_y - 20))

    def _draw_game_over_message(self, board):
        """Draw a message indicating the game result when the game is over."""
        if self.game_state == "checkmate":
            winner = "Black" if board.get_current_player() == 'w' else "White"
            message = f"{winner} wins by checkmate!"
        else:  # stalemate
            message = "Game drawn by stalemate"

        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.board_size, 40), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (self.board_x, self.board_y + self.board_size // 2 - 20))

        # Draw message
        text = self.fonts['large'].render(message, True, pygame.Color('white'))
        text_x = self.board_x + (self.board_size - text.get_width()) // 2
        text_y = self.board_y + self.board_size // 2 - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

    def _handle_square_selection(self, board, game_controller, square):
        """
        Handle selection of a square on the board.

        Args:
            board: The chess board.
            game_controller: Controller for game logic.
            square: Tuple (row, col) of the selected square.
        """
        row, col = square
        piece = board.get_piece(square)
        current_player = board.get_current_player()

        # If no square is currently selected
        if self.selected_square is None:
            # Only allow selecting squares with pieces of the current player
            if piece and ((piece.isupper() and current_player == 'w') or
                          (piece.islower() and current_player == 'b')):
                self.selected_square = square
                self.move_hints = board.get_legal_moves(square)

        # If a square is already selected
        else:
            selected_row, selected_col = self.selected_square

            # Check if the new square is a valid move target
            valid_move = None
            for move in self.move_hints:
                if move.to_pos == square:
                    valid_move = move
                    break

            if valid_move:
                # Make the move
                if hasattr(game_controller, 'make_move'):
                    game_controller.make_move(valid_move)
                self.selected_square = None
                self.move_hints = []

            # If clicking on another piece of the same color, select that instead
            elif piece and ((piece.isupper() and current_player == 'w') or
                            (piece.islower() and current_player == 'b')):
                self.selected_square = square
                self.move_hints = board.get_legal_moves(square)

            # Clicking elsewhere clears the selection
            else:
                self.selected_square = None
                self.move_hints = []

    def _handle_control_click(self, pos, game_controller):
        """
        Handle clicks on UI controls.

        Args:
            pos: Mouse position (x, y).
            game_controller: Controller for game logic.
        """
        # This will be implemented based on what UI controls you want
        pass

    def _update_fps(self):
        """Update and display the FPS counter."""
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time > 1.0:
            self.fps = self.frame_count / (current_time - self.last_time)
            self.last_time = current_time
            self.frame_count = 0

        # Draw FPS in bottom-right corner
        fps_text = self.fonts['small'].render(f"FPS: {int(self.fps)}", True, config.TEXT_COLOR)
        self.screen.blit(fps_text, (self.width - fps_text.get_width() - 10,
                                    self.height - fps_text.get_height() - 10))