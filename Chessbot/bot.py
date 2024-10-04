import chess
import chess.engine

# Create a chess board
board = chess.Board()

# Function to display the board
def display_board(board):
    print(board)

# Evaluation function to score the position for a draw
def evaluate_for_draw(board):
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        return 0  # Perfect draw
    if board.is_checkmate():
        return 1000 if board.turn else -1000  # Losing is bad, but winning is worse for the bot
    return len(list(board.legal_moves))  # Prefer positions with fewer legal moves (closer to draw)

# Bot that tries to draw
def draw_bot_move(board):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_score = float('inf')

    for move in legal_moves:
        board.push(move)
        score = evaluate_for_draw(board)
        if score < best_score:
            best_score = score
            best_move = move
        board.pop()  # Undo the move

    return best_move

# Main game loop
def play_chess():
    display_board(board)

    # Loop for the game
    while not board.is_game_over():
        # Player 1 (White) makes a move
        if board.turn:  # White's turn
            move = input("Enter your move (e.g., e2e4): ")
            if chess.Move.from_uci(move) in board.legal_moves:
                board.push(chess.Move.from_uci(move))
                display_board(board)
            else:
                print("Illegal move, try again.")
                continue

        # Player 2 (Black, Bot) makes a move
        else:
            print("Bot (Black) is thinking...")
            bot_move = draw_bot_move(board)
            board.push(bot_move)
            display_board(board)

    # Check game result
    if board.is_checkmate():
        print("Checkmate!")
    elif board.is_stalemate():
        print("Stalemate!")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material!")
    elif board.is_seventyfive_moves():
        print("Draw due to 75-move rule!")
    elif board.is_fivefold_repetition():
        print("Draw due to fivefold repetition!")
    elif board.is_variant_draw():
        print("Draw!")
    else:
        print("Game over!")

if __name__ == "__main__":
    play_chess()
