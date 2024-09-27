import random
import pygame
import classes
from chess import Game as ChessGame, BOARD_X, BOARD_Y, SQUARE_SIZE, BOARD_SIZE, WHITE, BLACK

def ler_imagem(caminho: str, tamanho: tuple[int, int]):
    image = pygame.image.load(caminho)
    image = pygame.transform.scale(image, tamanho)
    image = image.convert_alpha()
    return image

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
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Chess-OH")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
turns = 0
turn_step = 0
player_white = "white"
player_black = "black"

# Tenho que ver algum jeito melhor pra isso, mas por enquanto vai aqui
cost = None
pay_cost_card = 0
playing_card = False
card_playing = None
cost_type = None

whiteQtdPlay = 1
blackQtdPlay = 1
drawPhase = True
firstTurn = True

#Carregando as imagens
x_scale = 150
y_scale = 250
# Carregar as imagens das cartas (suponha que você tenha as imagens)
board = ler_imagem('xadrez/board.png',(700,700))
boardSquaHeight = board.get_height()/8
boardSquaWidth = board.get_width()/8


exp_duvi_img = ler_imagem('cards/exploracao_duvidosa.png', (x_scale,y_scale))

gan_duvi_img = ler_imagem('cards/ganancia_duvidosa.png', (x_scale,y_scale))

sac_plan_img = ler_imagem('cards/sacrificio_planejado.png', (x_scale,y_scale))

isso_meu_img = ler_imagem('cards/isso_e_meu.jpeg', (x_scale,y_scale))

est_alt_img = ler_imagem('cards/Estrategia_alt.jpeg', (x_scale,y_scale))

dir_iguais_img = ler_imagem('cards/direitos_iguais.png', (x_scale,y_scale))

cardBackBlack = ler_imagem('cards/cardback_black.jpg',(x_scale,y_scale))
cardBackWhite = ler_imagem('cards/cardback_white.jpg',(x_scale,y_scale))

#Criando os templates das cartas

sac_plan = classes.Sac_pla("Sacrifício Planejado", sac_plan_img, "Sacrifique uma torre, pule o seu próximo turno. No seu turno seguinte você terá dois turnos para jogar.", x_scale, y_scale)

iss_meu = classes.Isso_meu("Isso é Meu", isso_meu_img, "Compre a carta do topo do deck do oponente", x_scale, y_scale)

gan_duvi = classes.Gan_duv("Ganância Duvidosa", gan_duvi_img, "Uma vez por turno, sacrifique dois ou mais pontos. Compre duas Cartas", x_scale, y_scale)

est_alt = classes.Est_alt("Estratégia Alternativa", est_alt_img, "Envie para o cemitério 3 cartas do deck do oponente", x_scale, y_scale)

dir_iguais = classes.Dir_iguais("Direitos Iguais", dir_iguais_img, "Se for o primeiro turno do jogo e você estiver jogando com as peças pretas. Ative essa carta da sua mão. Pule o turno do oponente", x_scale, y_scale)

deck_white = classes.Deck(player_white,20)

deck_black = classes.Deck(player_black,20)

for _ in range(20):
    deck_white.AddToDeck(card = sac_plan)
    deck_black.AddToDeck(card = est_alt)

handWhite = classes.Hand(startHand=(50,height-y_scale),endHand=(1000,height - y_scale))
handBlack = classes.Hand(startHand=(50,height-y_scale),endHand=(1000,height - y_scale))

#handBlack.AddToHand(card= dir_iguais)

# Definir as posições das cartas
card1_pos = (100, height - y_scale)
card2_pos = (260, height - y_scale)
card3_pos = (420, height - y_scale)
card4_pos = (1000,height - y_scale)
card5_pos = (1000,0)

chess_game = ChessGame()

run = True
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    
    # Draw chess game
    chess_game.draw(screen)

    if handBlack.Contains(dir_iguais) and firstTurn:
        turn_step = 2
        firstTurn = False
        handBlack.RemoveFromHand(dir_iguais)
    last_turn_step = turn_step
    if drawPhase:
        if last_turn_step < 2:
            if not firstTurn:
                handWhite.AddToHand(cards = deck_white.Draw(1))
            firstTurn = False
        else:
            handBlack.AddToHand(cards = deck_white.Draw(1))
            #turn_step = 0
        drawPhase = False
  
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
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not chess_game.game_over:
            mouse_x, mouse_y = event.pos

            # Handle chess moves
            if BOARD_X <= mouse_x < BOARD_X + BOARD_SIZE * SQUARE_SIZE and BOARD_Y <= mouse_y < BOARD_Y + BOARD_SIZE * SQUARE_SIZE:
                chess_game.handle_click((mouse_x, mouse_y))
            
            auxCard = handWhite.Get_card_at_mouse(mouse_pos=(mouse_x, mouse_y))
            if(auxCard and card_playing == None):
                playing_card = True
                card_playing = auxCard
                cost = auxCard.Effect_cost()
                pay_cost_card = cost[0]
                #types: Any, peca especifica, place
                cost_type = cost[1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                handWhite.AddToHand(cards=deck_white.Draw(1))
                
            if event.key == pygame.K_f:
                iss_meu.Effect(ally_Deck = deck_white, ally_Hand = handWhite, enemy_Deck = deck_black)

    if playing_card and pay_cost_card == 0:
        cardEffect = card_playing.Effect(ally_Deck = deck_white, ally_Hand = handWhite, enemy_Deck = deck_black)
        turn_step_aux = turn_step
        if cardEffect:
            for effect,qtd in cardEffect:
                if effect == "Skip" and qtd == 1:
                    if turn_step_aux < 2:
                        turn_step = 2
                    else:
                        turn_step = 0
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

    if last_turn_step != turn_step and (turn_step == 0 or turn_step == 2):
        drawPhase = True

    pygame.display.flip()

    mouse_pos = pygame.mouse.get_pos()
    
    # Nao tive ainda a visao pra fazer mas tem algo feito la so falta aumentar
    #handWhite.is_mouse_on_card(mouse_pos)

pygame.quit