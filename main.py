import copy
import random
import pygame
import classes
from additions import *
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

turn_step = 0
selection = None
valid_moves = []

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
    if selection is not None:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    else:
        valid_moves = []

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
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            mouse_x, mouse_y = event.pos
            if board_x <= mouse_x < board_x + board_width and board_y <= mouse_y < board_y + board_height:
                x_coord = int((mouse_x - board_x) // square_size)
                y_coord = int((mouse_y - board_y) // square_size)
                click_coords = (x_coord, y_coord)
                if turn_step <= 1:

                    if forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                        winner = 'black'

                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        selected_piece = white_pieces[selection]
                        if turn_step == 0:
                            turn_step = 1
                    else:
                        selection = None  # Deselect if click is not on a piece

                    if click_coords in valid_moves and selection is not None:
                        white_ep = check_ep(white_locations[selection], click_coords)
                        white_locations[selection] = click_coords
                        white_moved[selection] = True

                        # Handle capturing black pieces
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = 'white'
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        
                        # Handle en passant
                        if black_ep is not None and click_coords == black_ep:
                            black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        
                        # Reset selection BEFORE updating options
                        selection = None
                        valid_moves = []
                        
                        # Update options
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2
                    # add option to castle
                    elif selection is not None and selected_piece == 'king':
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                white_locations[selection] = click_coords
                                white_moved[selection] = True
                                if click_coords == (1, 0):
                                    rook_coords = (0, 0)
                                else:
                                    rook_coords = (7, 0)
                                rook_index = white_locations.index(rook_coords)
                                white_locations[rook_index] = castling_moves[q][1]
                                black_options = check_options(black_pieces, black_locations, 'black')
                                white_options = check_options(white_pieces, white_locations, 'white')
                                turn_step = 2
                                selection = None
                                valid_moves = []
                if turn_step > 1:
                    if forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                        winner = 'white'

                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        selected_piece = black_pieces[selection]
                        if turn_step == 2:
                            turn_step = 3
                    else:
                        selection = None  # Deselect if click is not on a piece

                    if click_coords in valid_moves and selection is not None:
                        black_ep = check_ep(black_locations[selection], click_coords)
                        black_locations[selection] = click_coords
                        black_moved[selection] = True

                        # Handle capturing white pieces
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = 'black'
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        
                        # Handle en passant
                        if white_ep is not None and click_coords == white_ep:
                            white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        
                        # Reset selection BEFORE updating options
                        selection = None
                        valid_moves = []
                        
                        # Update options
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 0
                    # add option to castle
                    elif selection is not None and selected_piece == 'king':
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                black_locations[selection] = click_coords
                                black_moved[selection] = True
                                if click_coords == (1, 7):
                                    rook_coords = (0, 7)
                                else:
                                    rook_coords = (7, 7)
                                rook_index = black_locations.index(rook_coords)
                                black_locations[rook_index] = castling_moves[q][1]
                                black_options = check_options(black_pieces, black_locations, 'black')
                                white_options = check_options(white_pieces, white_locations, 'white')
                                turn_step = 0
                                selection = None
                                valid_moves = []
            else:
                # Handle clicks outside the board (e.g., promotion selection)
                check_promo_select()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                white_moved = [False, False, False, False, False, False, False, False,
                            False, False, False, False, False, False, False, False]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                black_moved = [False, False, False, False, False, False, False, False,
                            False, False, False, False, False, False, False, False]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = None
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                hand.AddToHand(cards=deck_white.Draw(1))

    if winner != '':
        game_over = True
        draw_game_over()

    mouse_pos = pygame.mouse.get_pos()
    
    # Nao tive ainda a visao pra fazer mas tem algo feito la so falta aumentar
    #hand.is_mouse_on_card(mouse_pos)

pygame.quit