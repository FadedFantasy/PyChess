import time
import config


class Animation:
    """Handles animations for chess piece movements."""

    def __init__(self):
        self.active_animations = []

    def add_move_animation(self, piece, from_pos, to_pos, piece_images):
        """
        Add a new piece movement animation.

        Args:
            piece: The character representing the piece (FEN notation)
            from_pos: Starting (row, col) position
            to_pos: Ending (row, col) position
            piece_images: Dictionary of piece images used for rendering
        """
        if not config.ENABLE_ANIMATIONS:
            return

        # Convert board positions to screen coordinates
        board_x = 20  # Should match renderer board_x
        board_y = (config.WINDOW_HEIGHT - config.BOARD_SIZE) // 2  # Should match renderer board_y
        square_size = config.SQUARE_SIZE

        # Calculate start and end positions
        # Convert from chess coordinates (row=0 is top) to screen coordinates (row=0 is bottom)
        start_x = board_x + from_pos[1] * square_size + (square_size - piece_images[piece].get_width()) // 2
        start_y = board_y + (7 - from_pos[0]) * square_size + (square_size - piece_images[piece].get_height()) // 2

        end_x = board_x + to_pos[1] * square_size + (square_size - piece_images[piece].get_width()) // 2
        end_y = board_y + (7 - to_pos[0]) * square_size + (square_size - piece_images[piece].get_height()) // 2

        # Create animation
        self.active_animations.append({
            'piece': piece,
            'image': piece_images[piece],
            'start_pos': (start_x, start_y),
            'end_pos': (end_x, end_y),
            'start_time': time.time(),
            'duration': config.ANIMATION_DURATION
        })

    def update_and_draw(self, screen):
        """
        Update animation states and draw animated pieces.

        Args:
            screen: Pygame screen surface to draw on

        Returns:
            True if animations are still active, False if all animations are complete
        """
        current_time = time.time()

        # Remove completed animations
        self.active_animations = [anim for anim in self.active_animations
                                  if current_time < anim['start_time'] + anim['duration']]

        # Draw active animations
        for anim in self.active_animations:
            # Calculate progress (0.0 to 1.0)
            elapsed = current_time - anim['start_time']
            progress = min(elapsed / anim['duration'], 1.0)

            # Use easing function for smoother movement
            progress = self._ease_out_quad(progress)

            # Calculate current position
            start_x, start_y = anim['start_pos']
            end_x, end_y = anim['end_pos']

            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress

            # Draw piece at current position
            screen.blit(anim['image'], (current_x, current_y))

        return len(self.active_animations) > 0

    def clear_animations(self):
        """Clear all active animations."""
        self.active_animations = []

    @staticmethod
    def _ease_out_quad(t):
        """
        Quadratic easing function for smoother animation.

        Args:
            t: Progress value from 0.0 to 1.0

        Returns:
            Eased value from 0.0 to 1.0
        """
        return -t * (t - 2)  # Simple quadratic easing
