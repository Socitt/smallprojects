import pygame
import chess
import chess.engine
import os

# Initialize Pygame
pygame.init()

# Load images for chess pieces
def load_images():
    pieces = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']
    images = {}
    for piece in pieces:
        images[piece] = pygame.image.load(os.path.join("images", piece + ".png"))
    return images

# Function to display the board and pieces
def draw_board(screen, board, images):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board.piece_at(chess.square(col, row))
            if piece:
                screen.blit(images[piece.symbol()], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

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

# Constants
WIDTH, HEIGHT = 512, 512
DIMENSION = 8  # 8x8 board
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15

# Main game loop with drag and drop functionality
def play_chess_with_gui():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    
    images = load_images()
    
    board = chess.Board()
    dragging = False
    selected_square = None
    selected_piece = None

    while not board.is_game_over():
        draw_board(screen, board, images)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // SQ_SIZE, x // SQ_SIZE
                square = chess.square(col, row)
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:  # Player's piece
                    dragging = True
                    selected_square = square
                    selected_piece = piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    x, y = event.pos
                    row, col = y // SQ_SIZE, x // SQ_SIZE
                    target_square = chess.square(col, row)
                    move = chess.Move(selected_square, target_square)
                    if move in board.legal_moves:
                        board.push(move)
                        draw_board(screen, board, images)
                        pygame.display.flip()
                        # Bot makes its move
                        bot_move = draw_bot_move(board)
                        board.push(bot_move)
                    dragging = False
                    selected_square = None

        clock.tick(FPS)

    print("Game Over!")

if __name__ == "__main__":
    play_chess_with_gui()
