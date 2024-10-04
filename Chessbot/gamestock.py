import pygame
import chess
import chess.engine

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512
DIMENSION = 8  # 8x8 board
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
FONT_SIZE = 36
STOCKFISH_PATH = "path_to_your_stockfish_executable"  # Replace with your Stockfish path

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

# Function to select a move using Stockfish aiming for a draw
def stockfish_draw_move(board):
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        # Get Stockfish's best move for the current position
        info = engine.analyse(board, chess.engine.Limit(time=0.1))
        best_move = info['pv'][0]
        
        # Now we try to find moves that Stockfish evaluates close to 0.0 (drawish moves)
        legal_moves = list(board.legal_moves)
        draw_moves = []
        for move in legal_moves:
            board.push(move)
            info = engine.analyse(board, chess.engine.Limit(time=0.1))
            score = info['score'].relative.score(mate_score=10000) / 100.0
            board.pop()
            
            if -0.1 <= score <= 0.1:
                draw_moves.append(move)
        
        # If no drawish move is found, use the best move from Stockfish
        if draw_moves:
            return draw_moves[0]
        else:
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
                        # Bot makes its move aiming for a draw
                        bot_move = stockfish_draw_move(board)
                        board.push(bot_move)
                    dragging = False
                    selected_square = None

        clock.tick(FPS)

    print("Game Over!")

if __name__ == "__main__":
    play_chess_with_gui()
