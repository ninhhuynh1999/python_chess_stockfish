# Chess Game with Stockfish AI

This project is an object-oriented implementation of a chess game using Python, Pygame, and the Stockfish chess engine. It provides a user-friendly interface to play chess against the AI opponent (Stockfish) with a visually appealing board representation.

## Features

- **Play against Stockfish:** Challenge the Stockfish engine at its default skill level. 
- **Visual Board:** Enjoy the game on a graphical board with classic piece representation.
- **Game Over Detection:** The game detects checkmate and stalemate conditions, declaring the winner or a draw.
- **Restart Functionality:** Easily restart the game after checkmate or stalemate.

## Requirements

- **Python 3.x:** Make sure you have Python 3 installed.
- **Pygame:** Install the Pygame library using `pip install pygame`.
- **Chess:** Install the Python Chess library using `pip install chess`.
- **Stockfish Engine:** 
    - Download the Stockfish engine binary for your operating system from the official website: [https://stockfishchess.org/download/](https://stockfishchess.org/download/)
    - Place the executable (`stockfish.exe` or similar) in your project directory or provide the correct path in the code (see `engine_path` in `main.py`).

## How to Run

1. **Install Dependencies:** Use `pip install -r requirements.txt` to install the necessary libraries.
2. **Update Engine Path:** Open the `main.py` file and update the `engine_path` variable to the correct location of your Stockfish engine executable. 
3. **Run the Game:** Execute the `main.py` file from your terminal: `python main.py`

## Project Structure

- `main.py`: Contains the main game loop, Pygame initialization, and the main logic for the chess game.
- `assets/`: Folder to store image files for the chess pieces.
- `README.md`: This file.

## Future Roadmap

This project can be further enhanced with the following features:

- **Configurable Difficulty:** Allow the user to set the difficulty level of the Stockfish engine (e.g., by adjusting Elo rating or search depth).
- **Player vs. Player Mode:** Implement a mode where two human players can play against each other.
- **Move History:** Display a list of moves made during the game.
- **Move Hints:** Use Stockfish to generate and display a list of the top 'K' best moves as hints for the player.
- **Improved UI:** Create a more sophisticated graphical user interface (GUI) with menus, options, and visual enhancements.
- **Sound Effects:** Add sound effects for piece movements and other game events.

## Contributing

Contributions to this project are welcome. If you have any ideas for new features, improvements, or bug fixes, feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License.
