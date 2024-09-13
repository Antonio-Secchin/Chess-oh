import copy
import random
import pygame
import classes
import additions
from constants import *

# Definir os pontos das peças
points = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0
}

# Data structures for chess game
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False

# Função para calcular a posição de uma peça no tabuleiro
def calcular_posicao_tabuleiro(coluna, linha, board_x, board_y, square_width, square_height):
    pos_x = board_x + coluna * square_width
    pos_y = board_y + linha * square_height
    return pos_x, pos_y

# Função para desenhar as pontuações das peças
def desenhar_pontuacoes(screen, font, pieces_positions, points, board_x, board_y, square_width, square_height):
    for piece_data in pieces_positions:
        piece_type = piece_data['piece']
        coluna, linha = piece_data['position']
        
        # Calcular a posição onde o número será desenhado
        pos_x, pos_y = calcular_posicao_tabuleiro(coluna, linha, board_x, board_y, square_width, square_height)
        
        # Obter a pontuação da peça
        piece_points = points[piece_type]
        
        # Renderizar o texto da pontuação
        points_text = font.render(str(piece_points), True, (255, 255, 255))
        
        # Ajustar a posição do texto para centralizar dentro do quadrado
        text_rect = points_text.get_rect(center=(pos_x + square_width // 2, pos_y + square_height // 2))
        
        # Desenhar o número no tabuleiro
        screen.blit(points_text, text_rect)

#def isOnCard(mouse_pos, cards):
#    for card in cards:
#        if mouse_pos[0] > card[0] and mouse_pos[0] < card[0] + x_scale and mouse_pos[1] < card[1]:
#            card.scale()

def ler_imagem(caminho: str, tamanho: tuple[int, int]):
    image = pygame.image.load(caminho)
    image = pygame.transform.scale(image, tamanho)
    image = image.convert_alpha()
    return image

# draw main game board
def draw_board():
    colors = ['white', 'light gray']
    for row in range(8):
        for col in range(8):
            # Determine the color of the square
            color_index = (row + col) % 2
            color = colors[color_index]
            # Calculate the position and size of the square
            square_rect = pygame.Rect(
                board_x + col * square_size,
                board_y + row * square_size,
                square_size,
                square_size
            )
            # Draw the square
            pygame.draw.rect(screen, color, square_rect)
    # Draw board outline
    pygame.draw.rect(screen, 'black', (board_x, board_y, board_width, board_height), 2)

def draw_pieces():
    # Draw white pieces
    for i in range(len(white_pieces)):
        piece = white_pieces[i]
        position = white_locations[i]
        image = white_images[piece]
        col, row = position
        # Calculate the top-left pixel position of the square
        pos_x = board_x + col * square_size
        pos_y = board_y + row * square_size
        # Center the piece image within the square
        piece_rect = image.get_rect(center=(
            pos_x + square_size / 2,
            pos_y + square_size / 2
        ))
        screen.blit(image, piece_rect)
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', piece_rect, 2)

    # Draw black pieces
    for i in range(len(black_pieces)):
        piece = black_pieces[i]
        position = black_locations[i]
        image = black_images[piece]
        col, row = position
        pos_x = board_x + col * square_size
        pos_y = board_y + row * square_size
        piece_rect = image.get_rect(center=(
            pos_x + square_size / 2,
            pos_y + square_size / 2
        ))
        screen.blit(image, piece_rect)
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue', piece_rect, 2)

# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        position = (
            captured_white_start_x,
            captured_white_start_y + captured_piece_spacing * i
        )
        screen.blit(small_black_images[index], position)
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        position = (
            captured_black_start_x,
            captured_black_start_y + captured_piece_spacing * i
        )
        screen.blit(small_white_images[index], position)


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        col, row = king_location
                        pygame.draw.rect(screen, 'dark red', [
                            board_x + col * square_size,
                            board_y + row * square_size,
                            square_size,
                            square_size
                        ], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        col, row = king_location
                        pygame.draw.rect(screen, 'dark blue', [
                            board_x + col * square_size,
                            board_y + row * square_size,
                            square_size,
                            square_size
                        ], 5)


def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

def draw_valid(moves):
    color = 'red' if turn_step < 2 else 'blue'
    for move in moves:
        col, row = move
        center_x = board_x + col * square_size + square_size / 2
        center_y = board_y + row * square_size + square_size / 2
        pygame.draw.circle(screen, color, (center_x, center_y), 5)


pygame.init()
width = 1200
height = 1000
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("Chess-OH")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
turns = 0
player_white = "white"

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

# Load images of the pieces
white_images = {
    'pawn':   ler_imagem('xadrez/assets/images/white pawn.png',   (int(65 * piece_scale_factor), int(65 * piece_scale_factor))),
    'queen':  ler_imagem('xadrez/assets/images/white queen.png',  (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'king':   ler_imagem('xadrez/assets/images/white king.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'rook':   ler_imagem('xadrez/assets/images/white rook.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'bishop': ler_imagem('xadrez/assets/images/white bishop.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'knight': ler_imagem('xadrez/assets/images/white knight.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor)))
}

black_images = {
    'pawn':   ler_imagem('xadrez/assets/images/black pawn.png',   (int(65 * piece_scale_factor), int(65 * piece_scale_factor))),
    'queen':  ler_imagem('xadrez/assets/images/black queen.png',  (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'king':   ler_imagem('xadrez/assets/images/black king.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'rook':   ler_imagem('xadrez/assets/images/black rook.png',   (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'bishop': ler_imagem('xadrez/assets/images/black bishop.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor))),
    'knight': ler_imagem('xadrez/assets/images/black knight.png', (int(80 * piece_scale_factor), int(80 * piece_scale_factor)))
}

deck = list(range(1,21))
hand = list()
random.shuffle(deck)
print(deck)
print(deck.pop(0))
print(deck)

#Carregando as imagens
x_scale = 150
y_scale = 250
# Carregar as imagens das cartas (suponha que você tenha as imagens)
board = ler_imagem('xadrez/board.png',(700,700))
# to pensando em usar isso pra colocar onde as pecas estariam e suas pontuaçoes
boardSquaHeight = board.get_height()/8
boardSquaWidth = board.get_width()/8
exp_duvi_img = ler_imagem('cards/exploracao_duvidosa.png', (x_scale,y_scale))

gan_duvi_img = ler_imagem('cards/ganancia_duvidosa.png', (x_scale,y_scale))
#card1 = pygame.image.load('cards/exploracao_duvidosa.png')  # substitua pelo caminho correto

sac_plan_img = ler_imagem('cards/sacrificio_planejado.png', (x_scale,y_scale))

cardBackBlack = ler_imagem('cards/cardback_black.jpg',(x_scale,y_scale))
cardBackWhite = ler_imagem('cards/cardback_white.jpg',(x_scale,y_scale))

#Criando os templates das cartas

sac_plan = classes.CardTemplate("Sacrifício Planejado", exp_duvi_img, "Sacrifique uma torre, pule o seu próximo turno. No seu turno seguinte você terá dois turnos para jogar.")

deck_white = classes.Deck(player_white,20)

for _ in range(20):
    deck_white.AddToDeck(card = sac_plan)

# Adjust card positions based on new board dimensions (not used yet, but might be useful)
# hand_start_x = board_x + board_width + 20  # Place the hand to the right of the board
# hand_start_y = height - y_scale - 20

hand = classes.Hand(startHand=(50,height-y_scale),endHand=(1000,height - y_scale))

#card_drawn = deck_white.Draw(1)

# for card in card_drawn:
#     print(card.name)

# Definir as posições das cartas
card1_pos = (100, height - y_scale)
card2_pos = (260, height - y_scale)
card3_pos = (420, height - y_scale)
card4_pos = (1000,height - y_scale)
card5_pos = (1000,0)

# Initialize options
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    # Desenha os movimentos da peça
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    hand.DrawHand(screen=screen)

    # Draw the deck indicators (adjust positions if necessary)
    x = 0
    for i in range(round(deck_white.actual_size / 4)):
        screen.blit(cardBackWhite, (width - x_scale - 25 + x, 25 - x))
        screen.blit(cardBackBlack, (width - x_scale - 25 + x, height - y_scale - x))
        x += 5

    pygame.display.flip()

    # event handling, if quit pressed, then exit game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            # Check if the click is within the board area
            if board_x <= mouse_x < board_x + board_width and board_y <= mouse_y < board_y + board_height:
                col = int((mouse_x - board_x) / square_size)
                row = int((mouse_y - board_y) / square_size)
                click_coords = (col, row)
                # Handle selection and movement logic
                if turn_step <= 1:
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        if turn_step == 0:
                            turn_step = 1
                    elif click_coords in valid_moves and selection != 100:
                        white_locations[selection] = click_coords
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                        # Update options
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2
                        selection = 100
                        valid_moves = []
                else:
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        if turn_step == 2:
                            turn_step = 3
                    elif click_coords in valid_moves and selection != 100:
                        black_locations[selection] = click_coords
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                        # Update options
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 0
                        selection = 100
                        valid_moves = []

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                hand.AddToHand(cards=deck_white.Draw(1))
    mouse_pos = pygame.mouse.get_pos()
    
    # Nao tive ainda a visao pra fazer mas tem algo feito la so falta aumentar
    #hand.is_mouse_on_card(mouse_pos)

pygame.quit