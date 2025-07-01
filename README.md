# Tic Tac Toe AI Web Application

A modern web-based Tic Tac Toe game featuring AI opponents using Minimax and Alpha-Beta Pruning algorithms.

**Repository:** [https://github.com/edgarvelr/tic-tac-toe-ai](https://github.com/edgarvelr/tic-tac-toe-ai)

## Features

- **Three Game Modes**: Human vs AI, AI vs AI, and Human vs Human
- **Two AI Algorithms**: Minimax and Alpha-Beta Pruning
- **Modern Web Interface**: Beautiful, responsive design
- **Game Statistics**: Track wins, losses, and ties
- **Real-time Gameplay**: Smooth, interactive experience

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5001
   ```

## How to Play

### Game Modes

1. **Human vs AI**: Play against an AI opponent
   - Choose your algorithm (Minimax or Alpha-Beta Pruning)
   - You play as 'O', AI plays as 'X'

2. **AI vs AI**: Watch two AI players compete
   - Both AIs use the same algorithm
   - Automatic gameplay with 1-second delays between moves

3. **Human vs Human**: Play with a friend
   - Take turns on the same device

### AI Algorithms

- **Minimax**: Classic algorithm that explores all possible game states
- **Alpha-Beta Pruning**: Optimized version that prunes unnecessary branches for faster performance

### Controls

- Click any empty cell to make a move
- Use "New Game" to start a new game with different settings
- Use "Reset" to clear all statistics and return to setup

## Technical Details

### Files Structure

```
HW2 AI/
├── tictactoe.py      # Core game logic and AI algorithms
├── app.py           # Flask web application
├── templates/
│   └── index.html   # Web interface
├── requirements.txt # Python dependencies
└── README.md       # This file
```

### Algorithm Performance

- **Minimax**: Explores all possible game states (optimal but slower)
- **Alpha-Beta Pruning**: Significantly faster by pruning unnecessary branches
- Both algorithms play optimally and are unbeatable

## Troubleshooting

### Common Issues

1. **"Import flask could not be resolved"**
   - Make sure you've installed the requirements: `pip install -r requirements.txt`

2. **Port already in use**
   - Change the port in `app.py` or kill the existing process

3. **AI moves are slow**
   - This is normal for Minimax algorithm
   - Try Alpha-Beta Pruning for faster gameplay

### Performance Tips

- Alpha-Beta Pruning is significantly faster than Minimax
- AI vs AI mode can be slow with Minimax algorithm
- The web interface provides visual feedback during AI thinking

## Development

The application is built with:
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI**: Custom Minimax and Alpha-Beta Pruning implementations

## License

This project is for educational purposes. Feel free to use and modify as needed. 