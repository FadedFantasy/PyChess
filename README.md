# Chess Engine Project

A modular chess engine designed with a clean separation between the board representation, move generation, evaluation, and UI components. This project provides a solid foundation for both playing and teaching chess programming.

## Project Structure

```
chess_engine/
├── main.py                           # Entry point
├── config.py                         # Configuration settings
├── assets/
│   └── images/
│       └── pieces/                   # Place your piece images here
├── src/
│   ├── board/
│   │   ├── __init__.py
│   │   ├── base_board.py             # Abstract board interface
│   │   ├── array_board.py            # Array representation (8x8)
│   │   ├── bitboard.py               # Bitboard implementation
│   │   └── move.py                   # Move representation
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── base_engine.py            # Abstract engine interface
│   │   ├── alpha_beta.py             # Alpha-beta pruning implementation
│   │   └── neural_engine.py          # Neural network implementation
│   │   └── stockfish.py              # Stockfish implementation
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── base_evaluator.py         # Abstract evaluator interface
│   │   ├── material_evaluator.py     # Material-based evaluation
│   │   └── positional_evaluator.py   # Position-based evaluation
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── renderer.py               # Pygame rendering
│   │   └── animations.py             # Piece movement animations
│   └── utils/
│       ├── __init__.py
│       ├── fen.py                    # FEN notation handling
│       └── pgn.py                    # PGN notation handling
└── tests/                            # Unit tests
```

## Features

- **Modular Architecture**: Clear separation between board representation, move generation, evaluation, and UI.
- **Customizable UI**: Modern Pygame-based UI with smooth animations and highlighting.
- **Standard Chess Notation**: Uses FEN-style notation for pieces ('P', 'N', 'B', 'R', 'Q', 'K' for white, lowercase for black).
- **Multiple Board Representations**: Framework for both array-based and bitboard representations.
- **Animation System**: Smooth piece movement animations with easing functions.

## Setting Up

1. **Install Dependencies**:
   ```
   pip install pygame numpy
   ```

2. **Piece Images**:
   - Place your piece images in the `assets/images/pieces/` directory
   - Use the following naming convention:
     - `white_pawn.png`, `white_knight.png`, etc.
     - `black_pawn.png`, `black_knight.png`, etc.

3. **Run the Application**:
   ```
   python main.py
   ```

## Implementation Details

### Renderer

The UI renderer handles:

- Drawing the chess board with standard alternating colors
- Loading and rendering piece images
- Highlighting selected squares, legal moves, last move, and check
- Smooth animations for piece movement
- Information panel with move history and game status
- Engine evaluation display

### Board Interface

The `BaseBoard` class defines an interface for chess board implementations:

- Uses FEN-style notation for pieces ('P', 'N', 'B', 'R', 'Q', 'K' for white, lowercase for black)
- Abstract methods for move generation, position evaluation, etc.
- Allows for swapping between array and bitboard implementations

### Move Representation

The `Move` class stores all information about a chess move:

- Source and destination positions
- Piece that's moving
- Captured piece (if any)
- Special move flags (castling, en passant, promotion)
- String representation in algebraic notation

## Extending the Project

### Implementing the Chess Logic

Implement the following to complete the chess engine:

1. **Board Representation**: Complete the array_board.py implementation.
2. **Move Generation**: Implement legal move generation for each piece type.
3. **Game Rules**: Add checkmate, stalemate, and draw detection.
4. **Evaluation**: Create evaluation functions of increasing sophistication.
5. **Search Algorithm**: Implement the alpha-beta pruning algorithm.

### Advanced Extensions

Once the basics are working, consider these extensions:

1. **Bitboard Implementation**: Create a more efficient bitboard representation.
2. **Opening Book**: Add an opening book for standard chess openings.
3. **Neural Network Evaluation**: Train a neural network to evaluate positions.
4. **Time Management**: Add sophisticated time management for tournament play.

## License

This project is provided for educational purposes. Feel free to modify and extend it for your own or commercial use.