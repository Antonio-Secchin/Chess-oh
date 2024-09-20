import pygame
pygame.init()

WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

def ler_imagem(caminho: str, tamanho: tuple[int, int]):
    image = pygame.image.load(caminho)
    image = pygame.transform.scale(image, tamanho)
    image = image.convert_alpha()
    return image

# game variables and images

# Define board position and size
board_x = 300  # X-coordinate of the top-left corner of the board
board_y = 250   # Y-coordinate of the top-left corner of the board
square_size = 60  # Size of each square on the board (adjust as needed)

# Calculate board dimensions based on square size
board_width = square_size * 8
board_height = square_size * 8

# Load images of the pieces with adjusted sizes
piece_scale_factor = square_size / 80  # Assuming original piece images were 80x80

# Adjusted positions for captured pieces
captured_white_start_x = board_x + board_width + 20  # To the right of the board
captured_white_start_y = board_y
captured_black_start_x = board_x - 70  # To the left of the board
captured_black_start_y = board_y
captured_piece_spacing = 50  # Space between captured pieces

# Define forfeit button area
forfeit_width = square_size * 2
forfeit_height = square_size
forfeit_x = board_x + board_width + 20
forfeit_y = board_y + board_height - forfeit_height
forfeit_button_rect = pygame.Rect(forfeit_x, forfeit_y, forfeit_width, forfeit_height)

# Data structures for chess game
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = None
valid_moves = []

# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2

# region pieces images
black_queen =        pygame.image.load('xadrez/assets/images/black queen.png')
black_queen =        pygame.transform.scale(black_queen, (80, 80))
black_queen_small =  pygame.transform.scale(black_queen, (45, 45))
black_king =         pygame.image.load('xadrez/assets/images/black king.png')
black_king =         pygame.transform.scale(black_king, (80, 80))
black_king_small =   pygame.transform.scale(black_king, (45, 45))
black_rook =         pygame.image.load('xadrez/assets/images/black rook.png')
black_rook =         pygame.transform.scale(black_rook, (80, 80))
black_rook_small =   pygame.transform.scale(black_rook, (45, 45))
black_bishop =       pygame.image.load('xadrez/assets/images/black bishop.png')
black_bishop =       pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight =       pygame.image.load('xadrez/assets/images/black knight.png')
black_knight =       pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn =         pygame.image.load('xadrez/assets/images/black pawn.png')
black_pawn =         pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small =   pygame.transform.scale(black_pawn, (45, 45))
white_queen =        pygame.image.load('xadrez/assets/images/white queen.png')
white_queen =        pygame.transform.scale(white_queen, (80, 80))
white_queen_small =  pygame.transform.scale(white_queen, (45, 45))
white_king =         pygame.image.load('xadrez/assets/images/white king.png')
white_king =         pygame.transform.scale(white_king, (80, 80))
white_king_small =   pygame.transform.scale(white_king, (45, 45))
white_rook =         pygame.image.load('xadrez/assets/images/white rook.png')
white_rook =         pygame.transform.scale(white_rook, (80, 80))
white_rook_small =   pygame.transform.scale(white_rook, (45, 45))
white_bishop =       pygame.image.load('xadrez/assets/images/white bishop.png')
white_bishop =       pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight =       pygame.image.load('xadrez/assets/images/white knight.png')
white_knight =       pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn =         pygame.image.load('xadrez/assets/images/white pawn.png')
white_pawn =         pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small =   pygame.transform.scale(white_pawn, (45, 45))
# endregion

white_images = {
    'pawn':   ler_imagem('xadrez/assets/images/white pawn.png',   (int(65 * piece_scale_factor), int(65 * piece_scale_factor))),
    'queen':  ler_imagem('xadrez/assets/images/white queen.png',  (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'king':   ler_imagem('xadrez/assets/images/white king.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'rook':   ler_imagem('xadrez/assets/images/white rook.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'bishop': ler_imagem('xadrez/assets/images/white bishop.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'knight': ler_imagem('xadrez/assets/images/white knight.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor)))
}
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = {
    'pawn':   ler_imagem('xadrez/assets/images/black pawn.png',   (int(65 * piece_scale_factor), int(65 * piece_scale_factor))),
    'queen':  ler_imagem('xadrez/assets/images/black queen.png',  (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'king':   ler_imagem('xadrez/assets/images/black king.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'rook':   ler_imagem('xadrez/assets/images/black rook.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'bishop': ler_imagem('xadrez/assets/images/black bishop.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'knight': ler_imagem('xadrez/assets/images/black knight.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor)))
}
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
white_ep = None
black_ep = None
white_promote = False
black_promote = False
promo_index = None
check = False
castling_moves = []