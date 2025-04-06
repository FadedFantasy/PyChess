import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
PIECE_IMAGES_DIR = os.path.join(ASSETS_DIR, "images", "pieces")

# UI settings
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
BOARD_SIZE = 560  # Size of the chess board in pixels
SQUARE_SIZE = BOARD_SIZE // 8  # Size of each square
PIECE_SCALE = 0.95  # Size of pieces relative to square size (0.95 = 95% of square size)

# Board colors
LIGHT_SQUARE = (240, 217, 181)  # Light beige
DARK_SQUARE = (181, 136, 99)  # Dark brown
HIGHLIGHT_COLOR = (124, 192, 214, 170)  # Blue highlight with alpha
MOVE_HINT_COLOR = (106, 168, 79, 150)  # Green move hint with alpha
LAST_MOVE_COLOR = (247, 247, 105, 140)  # Yellow last move with alpha
CHECK_COLOR = (231, 76, 60, 170)  # Red check highlight with alpha

# Background color
BACKGROUND_COLOR = (46, 46, 46)  # Dark gray

# Text colors
TEXT_COLOR = (238, 238, 238)  # Light gray

# Animation settings
ANIMATION_DURATION = 0.3  # Animation duration in seconds (lower = faster)
ENABLE_ANIMATIONS = True

# Game settings
DEFAULT_FPS = 60
