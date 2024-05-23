import pygame
import os

from utils import *
from pieces import *
import UI
import logic

# Initialize pygame
pygame.init()
screenInfo = pygame.display.Info()

# Constants
WIDTH, HEIGHT = screenInfo.current_w - 200, screenInfo.current_h - 100

# Window customizations
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Chess Game")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "chess-icon.png")))

# Initialize instances
ui = UI.UI()

chess_board, square_rects = ui.chess_board()
all_pieces = ui.initialize_pieces()

# Variable initialization
selected_piece: UI.Sprite = None
selected_piece_name: str = None
allowed_moves = {}
played_moves = []

def show_allowed_moves() -> None: # Highlights allowed moves (by piece)
    if not allowed_moves:
        return
    
    moves = allowed_moves.get("moves", [])
    captures = allowed_moves.get("capture", [])
    
    if moves:
        for square in moves:
            square_rect = square_rects_dict.get(square)
            pygame.draw.circle(WINDOW, DARK_GRAY, square_rect.center, 10) # Highlight available moves
    
    if captures:
        for capture_square in captures:
            capture_square_rect = square_rects_dict.get(capture_square)
            capture_highlight = capture_square_rect.inflate(2, 2)
            pygame.draw.rect(WINDOW, RED, capture_highlight, 3) # Highlight available captures

def piece_highlight() -> None: # Highlight selection of piece
    if selected_piece is not None:
        piece_rect: pygame.Rect = selected_piece.get_rect()
        square_rect = get_square(piece_rect.center)[1]

        overlay_color = (255, 255, 0)
        overlay_surface = pygame.Surface((square_rect.width, square_rect.height), pygame.SRCALPHA)
        overlay_surface.fill(overlay_color)
        overlay_surface.set_alpha(70)

        show_allowed_moves()
        WINDOW.blit(overlay_surface, square_rect.topleft)

def display_moves(): # TODO: Fix design
    background_rect = pygame.Rect(WIDTH - 500, 50, 300, 300)
    pygame.draw.rect(WINDOW, (30, 30, 30), background_rect, border_radius = 20)
    text_y = background_rect.top + 10
    for move in played_moves:
        text_surface = FONT32.render(move, True, (255, 255, 255))
        WINDOW.blit(text_surface, (background_rect.left + 10, text_y))
        text_y += 30

def add_graphics() -> None: # Graphics section (board and more...)
    WINDOW.fill(GRAY)
    WINDOW.blit(chess_board, (BOARD_OFFSET_X, BOARD_OFFSET_Y)) # Loading chess board

    piece_highlight() # Piece selection
    display_moves() # Highlight moves and captures

    all_pieces.update() # Update pieces on board
    all_pieces.draw(WINDOW)
    pygame.display.update() # Display update

def main(): # Main function/loop
    global selected_piece, selected_piece_name, allowed_moves
    clicked = False
    selected = False

    clock = pygame.time.Clock()
    running = True
    while running: # Main loop
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
                clicked_square = get_square(mouse_pos)[0]
                if selected and clicked_square is not None: # Piece selected and clicked in valid square
                    piece_rect: pygame.Rect = chess_pieces_dict.get(piece_name).get_rect()
                    if friendly_piece(piece_rect.center, mouse_pos):
                        selected, piece_name = select_piece(mouse_pos) # Switch selection if clicked on friendly piece
                        selected_piece, selected_piece_name = chess_pieces_dict.get(piece_name), piece_name # Record selection
                        if piece_name is not None:
                            allowed_moves = logic.get_allowed_moves(piece_name, mouse_pos)
                    else:
                        move = logic.move_piece(piece_name, mouse_pos) # Move piece
                        if move is not None:
                            played_moves.append(move) # Record move
                        selected = False
                        selected_piece = None # Reset selection
                else:
                    selected, piece_name = select_piece(mouse_pos) # Select piece
                    selected_piece, selected_piece_name = chess_pieces_dict.get(piece_name), piece_name # Record selection
                    if piece_name is not None:
                        allowed_moves = logic.get_allowed_moves(piece_name, mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                print("Clicked square: ", get_square(mouse_pos)[0]) # DEBUG

        add_graphics()

    pygame.quit()

if __name__ == "__main__":
    main()