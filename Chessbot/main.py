import chess
import chess.engine

# Create a chess board
board = chess.Board()

# Function to display the board
def display_board(board):
    print(board)

# Main game loop
def play_chess():
    display_board(board)

    # Loop for the game
    while not board.is_game_over():
        # Player 1 (White) makes a move
        move = input("Enter your move (e.g., e2e4): ")
        if chess.Move.from_uci(move) in board.legal_moves:
            board.push(chess.Move.from_uci(move))
            display_board(board)
        else:
            print("Illegal move, try again.")
            continue

        # Check if the game is over
        if board.is_game_over():
            break

        # Player 2 (Black) makes a move
        move = input("Enter your move (e.g., e7e5): ")
        if chess.Move.from_uci(move) in board.legal_moves:
            board.push(chess.Move.from_uci(move))
            display_board(board)
        else:
            print("Illegal move, try again.")
            continue

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
