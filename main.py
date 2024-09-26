import copy
import random
import pygame
import classes
from additions import *
import constants as c

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
player_black = "black"

# Tenho que ver algum jeito melhor pra isso, mas por enquanto vai aqui
cost = None
pay_cost_card = 0
playing_card = False
card_playing = None
cost_type = None

deck = list(range(1,21))
handWhite = list()
whiteQtdPlay = 1
blackQtdPlay = 1
drawPhase = True
firstTurn = True
random.shuffle(deck)
print(deck)
print(deck.pop(0))
print(deck)

#Carregando as imagens
x_scale = 150
y_scale = 250
# Carregar as imagens das cartas (suponha que você tenha as imagens)
board = c.ler_imagem('xadrez/board.png',(700,700))
boardSquaHeight = board.get_height()/8
boardSquaWidth = board.get_width()/8


exp_duvi_img = c.ler_imagem('cards/exploracao_duvidosa.png', (x_scale,y_scale))

gan_duvi_img = c.ler_imagem('cards/ganancia_duvidosa.png', (x_scale,y_scale))

sac_plan_img = c.ler_imagem('cards/sacrificio_planejado.png', (x_scale,y_scale))

isso_meu_img = c.ler_imagem('cards/isso_e_meu.jpeg', (x_scale,y_scale))

est_alt_img = c.ler_imagem('cards/Estrategia_alt.jpeg', (x_scale,y_scale))

dir_iguais_img = c.ler_imagem('cards/direitos_iguais.png', (x_scale,y_scale))

cardBackBlack = c.ler_imagem('cards/cardback_black.jpg',(x_scale,y_scale))
cardBackWhite = c.ler_imagem('cards/cardback_white.jpg',(x_scale,y_scale))

#Criando os templates das cartas

sac_plan = classes.Sac_pla("Sacrifício Planejado", sac_plan_img, "Sacrifique uma torre, pule o seu próximo turno. No seu turno seguinte você terá dois turnos para jogar.", x_scale, y_scale)

iss_meu = classes.Isso_meu("Isso é Meu", isso_meu_img, "Compre a carta do topo do deck do oponente", x_scale, y_scale)

gan_duvi = classes.Gan_duv("Ganância Duvidosa", gan_duvi_img, "Uma vez por turno, sacrifique dois ou mais pontos. Compre duas Cartas", x_scale, y_scale)

est_alt = classes.Est_alt("Estratégia Alternativa", est_alt_img, "Envie para o cemitério 3 cartas do deck do oponente", x_scale, y_scale)

dir_iguais = classes.Est_alt("Estratégia Alternativa", est_alt_img, "Envie para o cemitério 3 cartas do deck do oponente", x_scale, y_scale)

deck_white = classes.Deck(player_white,20)

deck_black = classes.Deck(player_black,20)

for _ in range(20):
    deck_white.AddToDeck(card = sac_plan)
    deck_black.AddToDeck(card = est_alt)

handWhite = classes.Hand(startHand=(50,height-y_scale),endHand=(1000,height - y_scale))
handBlack = classes.Hand(startHand=(50,height-y_scale),endHand=(1000,height - y_scale))


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
    if c.counter < 30:
        c.counter += 1
    else:
        c.counter = 0
    screen.fill('dark gray')
    
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    last_turn_step = c.turn_step
    if drawPhase:
        if last_turn_step < 2:
            if not firstTurn:
                handWhite.AddToHand(cards = deck_white.Draw(1))
            firstTurn = False
        else:
            handBlack.AddToHand(cards = deck_white.Draw(1))
            #c.turn_step = 0
        drawPhase = False

    # Desenha os movimentos da peça
    if c.selection is not None:
        c.valid_moves = check_valid_moves()
        draw_valid(c.valid_moves)
    else:
        c.valid_moves = []
    
    mouse_pos = pygame.mouse.get_pos()
    handWhite.DrawHand(screen=screen,mouse_pos=mouse_pos)

    # Draw the deck indicators (adjust positions if necessary)
    x = 0
    for i in range(round(deck_white.actual_size / 4)):
        screen.blit(cardBackWhite, (width - x_scale - 25 + x, 25 - x))
        screen.blit(cardBackBlack, (width - x_scale - 25 + x, height - y_scale - x))
        x += 5

    # event handWhiteling, if quit pressed, then exit game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not c.game_over:
            mouse_x, mouse_y = event.pos
            auxCard = handWhite.Get_card_at_mouse(mouse_pos=(mouse_x, mouse_y))
            if(auxCard and card_playing == None):
                playing_card = True
                card_playing = auxCard
                cost = auxCard.Effect_cost()
                pay_cost_card = cost[0]
                #types: Any, peca especifica, place
                cost_type = cost[1]
        
            if c.board_x <= mouse_x < c.board_x + c.board_width and c.board_y <= mouse_y < c.board_y + c.board_height:
                x_coord = int((mouse_x - c.board_x) // c.square_size)
                y_coord = int((mouse_y - c.board_y) // c.square_size)
                click_coords = (x_coord, y_coord)
                if c.turn_step <= 1:

                    if pay_cost_card != 0:
                        if click_coords in c.white_locations:
                            c.selection = c.white_locations.index(click_coords)
                            selected_piece = c.white_pieces[c.selection]
                            if cost_type == "Any" or cost_type == selected_piece:
                                c.white_pieces.pop(c.selection)
                                c.white_locations.pop(c.selection)
                                c.white_moved.pop(c.selection)
                                pay_cost_card = max(0,pay_cost_card -c.points[selected_piece])
                                c.selection = None

                    if c.forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                        c.winner = 'black'

                    if click_coords in c.white_locations:
                        c.selection = c.white_locations.index(click_coords)
                        selected_piece = c.white_pieces[c.selection]
                        if c.turn_step == 0:
                            c.turn_step = 1

                    if click_coords in c.valid_moves and c.selection is not None:
                        c.white_ep = check_ep(c.white_locations[c.selection], click_coords)
                        c.white_locations[c.selection] = click_coords
                        c.white_moved[c.selection] = True

                        # Handle capturing black pieces
                        if click_coords in c.black_locations:
                            black_piece = c.black_locations.index(click_coords)
                            c.captured_pieces_white.append(c.black_pieces[black_piece])
                            if c.black_pieces[black_piece] == 'king':
                                c.winner = 'white'
                            c.black_pieces.pop(black_piece)
                            c.black_locations.pop(black_piece)
                            c.black_moved.pop(black_piece)
                        
                        # Handle en passant
                        if c.black_ep is not None and click_coords == c.black_ep:
                            black_piece = c.black_locations.index((c.black_ep[0], c.black_ep[1] - 1))
                            c.captured_pieces_white.append(c.black_pieces[black_piece])
                            c.black_pieces.pop(black_piece)
                            c.black_locations.pop(black_piece)
                            c.black_moved.pop(black_piece)
                        
                        # Reset c.selection BEFORE updating options
                        c.selection = None
                        c.valid_moves = []
                        
                        # Update options
                        c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                        c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                        if whiteQtdPlay == 1:
                                    c.turn_step = 2
                                    whiteQtdPlay = 1
                        else:
                            whiteQtdPlay-=1
                    # add option to castle
                    elif c.selection is not None and selected_piece == 'king':
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                c.white_locations[c.selection] = click_coords
                                c.white_moved[c.selection] = True
                                if click_coords == (1, 0):
                                    rook_coords = (0, 0)
                                else:
                                    rook_coords = (7, 0)
                                rook_index = c.white_locations.index(rook_coords)
                                c.white_locations[rook_index] = castling_moves[q][1]
                                c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                                c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                                if whiteQtdPlay == 0:
                                    c.turn_step = 2
                                    whiteQtdPlay = 1
                                else:
                                    whiteQtdPlay-=1
                                c.selection = None
                                c.valid_moves = []
                if c.turn_step > 1:
                    if c.forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                        c.winner = 'white'

                    if click_coords in c.black_locations:
                        c.selection = c.black_locations.index(click_coords)
                        selected_piece = c.black_pieces[c.selection]
                        if c.turn_step == 2:
                            c.turn_step = 3

                    if click_coords in c.valid_moves and c.selection is not None:
                        c.black_ep = check_ep(c.black_locations[c.selection], click_coords)
                        c.black_locations[c.selection] = click_coords
                        c.black_moved[c.selection] = True

                        # Handle capturing white pieces
                        if click_coords in c.white_locations:
                            white_piece = c.white_locations.index(click_coords)
                            c.captured_pieces_black.append(c.white_pieces[white_piece])
                            if c.white_pieces[white_piece] == 'king':
                                c.winner = 'black'
                            c.white_pieces.pop(white_piece)
                            c.white_locations.pop(white_piece)
                            c.white_moved.pop(white_piece)
                        
                        # Handle en passant
                        if c.white_ep is not None and click_coords == c.white_ep:
                            white_piece = c.white_locations.index((c.white_ep[0], c.white_ep[1] + 1))
                            c.captured_pieces_black.append(c.white_pieces[white_piece])
                            c.white_pieces.pop(white_piece)
                            c.white_locations.pop(white_piece)
                            c.white_moved.pop(white_piece)
                        
                        # Reset c.selection BEFORE updating options
                        c.selection = None
                        c.valid_moves = []
                        
                        # Update options
                        c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                        c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                        c.turn_step = 0
                    # add option to castle
                    elif c.selection is not None and selected_piece == 'king':
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                c.black_locations[c.selection] = click_coords
                                c.black_moved[c.selection] = True
                                if click_coords == (1, 7):
                                    rook_coords = (0, 7)
                                else:
                                    rook_coords = (7, 7)
                                rook_index = c.black_locations.index(rook_coords)
                                c.black_locations[rook_index] = castling_moves[q][1]
                                c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                                c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                                c.turn_step = 0
                                c.selection = None
                                c.valid_moves = []
            else:
                # Handle clicks outside the board (e.g., promotion c.selection)
                check_promo_select()

        if event.type == pygame.KEYDOWN and c.game_over:
            if event.key == pygame.K_RETURN:
                c.game_over = False
                c.winner = ''
                c.white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                c.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                c.white_moved = [False, False, False, False, False, False, False, False,
                            False, False, False, False, False, False, False, False]
                c.black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                c.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                c.black_moved = [False, False, False, False, False, False, False, False,
                            False, False, False, False, False, False, False, False]
                c.captured_pieces_white = []
                c.captured_pieces_black = []
                c.turn_step = 0
                c.selection = None
                c.valid_moves = []
                c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                c.white_options = check_options(c.white_pieces, c.white_locations, 'white')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                handWhite.AddToHand(cards=deck_white.Draw(1))
                
            if event.key == pygame.K_f:
                iss_meu.Effect(ally_Deck = deck_white, ally_Hand = handWhite, enemy_Deck = deck_black)

    if playing_card and pay_cost_card == 0:
        cardEffect = card_playing.Effect(ally_Deck = deck_white, ally_Hand = handWhite, enemy_Deck = deck_black)
        turn_step_aux = c.turn_step
        if cardEffect:
            for effect,qtd in cardEffect:
                if effect == "Skip" and qtd == 1:
                    if turn_step_aux < 2:
                        c.turn_step = 2
                    else:
                        c.turn_step = 0
                if effect == "QtdPlay":
                    if turn_step_aux < 2:
                        whiteQtdPlay = 2
                    else:
                        blackQtdPlay = 2
        handWhite.RemoveFromHand(card_playing)
        playing_card = False
        card_playing = None
        cost_type = None
        cost = None
        cardEffect = None

    if last_turn_step != c.turn_step and (c.turn_step == 0 or c.turn_step == 2):
        drawPhase = True

    if c.winner != '':
        c.game_over = True
        draw_game_over()

    pygame.display.flip()

    mouse_pos = pygame.mouse.get_pos()
    
    # Nao tive ainda a visao pra fazer mas tem algo feito la so falta aumentar
    #handWhite.is_mouse_on_card(mouse_pos)

pygame.quit