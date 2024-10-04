import pygame
import chess

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512
DIMENSION = 8  # 8x8 board
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
FONT_SIZE = 36
SEARCH_DEPTH = 3  # Depth for Minimax search

# Colors
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
LIGHT_SQUARE = pygame.Color('lightgray')
DARK_SQUARE = pygame.Color('darkgray')

# Font for displaying pieces
FONT = pygame.font.SysFont('Arial', FONT_SIZE)

# Chess piece symbols mapping
PIECE_SYMBOLS = {
    'p': 'p', 'r': 'r', 'n': 'n', 'b': 'b', 'q': 'q', 'k': 'k',  # Black pieces
    'P': 'P', 'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K'   # White pieces
}

# Function to draw the board and pieces
def draw_board(screen, board):
    colors = [LIGHT_SQUARE, DARK_SQUARE]
    
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
            # Flip board for white to be on bottom
            flipped_row = 7 - row if board.turn else row
            piece = board.piece_at(chess.square(col, flipped_row))
            
            if piece:
                piece_symbol = piece.symbol()
                piece_text = PIECE_SYMBOLS[piece_symbol]
                text_surface = FONT.render(piece_text, True, BLACK if piece_symbol.islower() else WHITE)
                text_rect = text_surface.get_rect(center=(col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2))
                screen.blit(text_surface, text_rect)

# Enhanced evaluation function for the bot
def evaluate_position(board):
    if board.is_checkmate():
        if board.turn:  # If it's the bot's turn and it's checkmate, the bot is losing
            return -10000
        else:  # If it's the player's turn and it's checkmate, the bot is winning
            return 10000
    elif board.is_stalemate():
        return 0  # Neutral score for stalemates
    
    # Simplified material count: positive score for bot advantage
    material_score = sum(piece_value(piece) for piece in board.piece_map().values())
    return material_score

def piece_value(piece):
    """Returns the value of a piece. Positive for white pieces, negative for black."""
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    value = values[piece.symbol().upper()]
    return value if piece.color == chess.WHITE else -value

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_position(board)
    
    legal_moves = list(board.legal_moves)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Bot that uses Minimax with Alpha-Beta pruning
def minimax_bot_move(board, depth=SEARCH_DEPTH):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_score = float('-inf')

    for move in legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

# Main game loop with drag-and-drop functionality
def play_chess_with_gui():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    
    board = chess.Board()
    dragging = False
    selected_square = None
    selected_piece = None

    while not board.is_game_over():
        draw_board(screen, board)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // SQ_SIZE, x // SQ_SIZE
                flipped_row = 7 - row if board.turn else row  # Adjust for board flipping
                square = chess.square(col, flipped_row)
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:  # Player's piece
                    dragging = True
                    selected_square = square
                    selected_piece = piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    x, y = event.pos
                    row, col = y // SQ_SIZE, x // SQ_SIZE
                    flipped_row = 7 - row if board.turn else row  # Adjust for board flipping
                    target_square = chess.square(col, flipped_row)
                    move = chess.Move(selected_square, target_square)
                    if move in board.legal_moves:
                        board.push(move)
                        draw_board(screen, board)
                        pygame.display.flip()
                        # Bot makes its move
                        bot_move = minimax_bot_move(board)
                        board.push(bot_move)
                    dragging = False
                    selected_square = None

        clock.tick(FPS)

    print("Game Over!")

if __name__ == "__main__":
    play_chess_with_gui()
