# Gobblet Jr.

Gobblet Jr. is a Python-based implementation of the board game Gobblet Jr. using Pygame. The objective of the game is to get three pieces of the same color in a row, either horizontally, vertically, or diagonally. Players can place pieces on an empty square or cover smaller pieces with larger ones, adding a strategic layer to the game.

## Game Rules
- The game is played on a 3x3 grid.
- Each player has 6 pieces (2 of each size: small, medium, large).
- Players take turns to place or move pieces on the board.
- A piece can be placed on an empty cell or on top of a smaller piece of either color.
- The goal is to align 3 pieces of your color in a row, column, or diagonal.
- The game ends when a player achieves this or if the board is completely filled, resulting in a draw.

## Assumptions
- The game is implemented as a local two-player game (no AI or network play).
- The design uses circles of different sizes and colors to represent game pieces.
- There is no undo button, and all moves are final.

## Installation
1. Make sure you have Python installed (>=3.7).
2. Install Pygame using pip:
```bash
pip install pygame
```
3. Clone the repository and run the game:
```bash
git clone https://github.com/yourusername/gobblet-jr.git
cd gobblet-jr
python Gobble.py
```

## How to Play
- Start the game and the first player ('P1', dark blue) will play first.
- Click on a piece from the reserve at the top (for P1) or bottom (for P2, light blue).
- Click on a cell in the grid to place the piece.
- You can also move pieces on the board if they are on top of a stack.
- The game indicates the current player's turn and announces the winner or a draw.

## Controls
- **Left Mouse Button:** Select and place/move pieces.
- **Window Close Button:** Quit the game.

## Dependencies
- Python 3.7+
- Pygame

## Known Issues
- No support for resizing the window or handling edge cases beyond standard gameplay.
- Limited visual feedback for invalid moves.

