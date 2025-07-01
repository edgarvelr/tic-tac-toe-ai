from flask import Flask, render_template, request, jsonify, session
import json
import sys
import os

# Add the current directory to Python path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tictactoe import TicTacToe, AIPlayer, HumanPlayer
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    try:
        data = request.get_json()
        game_mode = data.get('game_mode')
        ai_algorithm = data.get('ai_algorithm', 'alpha-beta')
        
        # Initialize game
        game = TicTacToe()
        
        # Set up players based on game mode
        if game_mode == 'human_vs_ai':
            x_player = AIPlayer('X', algorithm=ai_algorithm)
            o_player = HumanPlayer('O')
            current_player = 'O'  # Human goes first
        elif game_mode == 'ai_vs_ai':
            x_player = AIPlayer('X', algorithm=ai_algorithm)
            o_player = AIPlayer('O', algorithm=ai_algorithm)
            current_player = 'X'  # AI X goes first
        else:  # human_vs_human
            x_player = HumanPlayer('X')
            o_player = HumanPlayer('O')
            current_player = 'X'
        
        # Store game state in session
        session['game_board'] = game.board
        session['current_player'] = current_player
        session['game_mode'] = game_mode
        session['ai_algorithm'] = ai_algorithm
        session['winner'] = None
        session['game_over'] = False
        
        return jsonify({
            'board': [cell if cell != ' ' else '' for cell in game.board],
            'current_player': current_player,
            'game_mode': game_mode
        })
    except Exception as e:
        print(f"Error in new_game: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/make_move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        position = data.get('position')
        
        # Get current game state
        game = TicTacToe()
        game.board = session.get('game_board', [' ' for _ in range(9)])
        game.winner = session.get('winner')
        current_player = session.get('current_player', 'X')
        game_mode = session.get('game_mode', 'human_vs_ai')
        ai_algorithm = session.get('ai_algorithm', 'alpha-beta')
        
        # Make the move
        if game.make_move(position, current_player):
            # Update session
            session['game_board'] = game.board
            session['winner'] = game.winner
            
            # Check if game is over
            if game.winner or not game.has_empty_squares():
                session['game_over'] = True
                return jsonify({
                    'board': [cell if cell != ' ' else '' for cell in game.board],
                    'winner': game.winner,
                    'game_over': True,
                    'message': f"{game.winner} wins!" if game.winner else "It's a tie!"
                })
            
            # Switch players
            next_player = 'O' if current_player == 'X' else 'X'
            session['current_player'] = next_player
            
            # If next player is AI, make AI move
            ai_move = None
            if game_mode in ['human_vs_ai', 'ai_vs_ai'] and next_player == 'X':
                x_player = AIPlayer('X', algorithm=ai_algorithm)
                ai_move = x_player.get_move(game)
                
                if game.make_move(ai_move, next_player):
                    session['game_board'] = game.board
                    session['winner'] = game.winner
                    
                    if game.winner or not game.has_empty_squares():
                        session['game_over'] = True
                        return jsonify({
                            'board': [cell if cell != ' ' else '' for cell in game.board],
                            'winner': game.winner,
                            'game_over': True,
                            'ai_move': ai_move,
                            'message': f"{game.winner} wins!" if game.winner else "It's a tie!"
                        })
                    
                    next_player = 'O' if next_player == 'X' else 'X'
                    session['current_player'] = next_player
            
            return jsonify({
                'board': [cell if cell != ' ' else '' for cell in game.board],
                'current_player': next_player,
                'ai_move': ai_move
            })
        
        return jsonify({'error': 'Invalid move'}), 400
    except Exception as e:
        print(f"Error in make_move: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/ai_move', methods=['POST'])
def ai_move():
    try:
        # Get current game state
        game = TicTacToe()
        game.board = session.get('game_board', [' ' for _ in range(9)])
        game.winner = session.get('winner')
        current_player = session.get('current_player', 'X')
        ai_algorithm = session.get('ai_algorithm', 'alpha-beta')
        
        # Make AI move
        ai_player = AIPlayer(current_player, algorithm=ai_algorithm)
        ai_move = ai_player.get_move(game)
        
        if game.make_move(ai_move, current_player):
            session['game_board'] = game.board
            session['winner'] = game.winner
            
            if game.winner or not game.has_empty_squares():
                session['game_over'] = True
                return jsonify({
                    'board': [cell if cell != ' ' else '' for cell in game.board],
                    'winner': game.winner,
                    'game_over': True,
                    'ai_move': ai_move,
                    'message': f"{game.winner} wins!" if game.winner else "It's a tie!"
                })
            
            next_player = 'O' if current_player == 'X' else 'X'
            session['current_player'] = next_player
            
            return jsonify({
                'board': [cell if cell != ' ' else '' for cell in game.board],
                'current_player': next_player,
                'ai_move': ai_move
            })
        
        return jsonify({'error': 'AI move failed'}), 400
    except Exception as e:
        print(f"Error in ai_move: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Tic Tac Toe AI Web Application...")
    print("Open your browser and go to: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001) 