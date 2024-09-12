import copy
import random
import pygame
import classes

# Definir os pontos das peças
points = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0
}

# Posições iniciais das peças no tabuleiro (usando (coluna, linha) 0-index)
pieces_positions = [
    {'piece': 'rook', 'position': (0, 0)},  # Torre na posição (0, 0)
    {'piece': 'knight', 'position': (1, 0)},  # Cavalo na posição (1, 0)
    {'piece': 'bishop', 'position': (2, 0)},  # Bispo na posição (2, 0)
    {'piece': 'queen', 'position': (3, 0)},  # Rainha na posição (3, 0)
    {'piece': 'king', 'position': (4, 0)},   # Rei na posição (4, 0)
    {'piece': 'bishop', 'position': (5, 0)}, # Bispo na posição (5, 0)
    {'piece': 'knight', 'position': (6, 0)}, # Cavalo na posição (6, 0)
    {'piece': 'rook', 'position': (7, 0)},   # Torre na posição (7, 0)
    {'piece': 'pawn', 'position': (0, 1)},   # Peão na posição (0, 1)
    {'piece': 'pawn', 'position': (1, 1)},
    {'piece': 'pawn', 'position': (2, 1)},
    {'piece': 'pawn', 'position': (3, 1)},
    {'piece': 'pawn', 'position': (4, 1)},
    {'piece': 'pawn', 'position': (5, 1)},
    {'piece': 'pawn', 'position': (6, 1)},
    {'piece': 'pawn', 'position': (7, 1)}
    # Adicione todas as outras peças conforme necessário
]

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

board_x = 100
board_y = 50

run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')

    screen.blit(board, (100,50))

    desenhar_pontuacoes(screen, smaller_font, pieces_positions, points, board_x, board_y, boardSquaWidth, boardSquaHeight)


    hand.DrawHand(screen=screen)

    x = 0
    for i in range(round(deck_white.actual_size/4)):
        screen.blit(cardBackWhite, (width - x_scale - 25 + x, 25 - x))
        screen.blit(cardBackBlack, (width - x_scale - 25 + x, height - y_scale -x))
        x += 5

    pygame.display.flip()

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                hand.AddToHand(cards=deck_white.Draw(1))
    mouse_pos = pygame.mouse.get_pos()
    
    # Nao tive ainda a visao pra fazer mas tem algo feito la so falta aumentar
    #hand.is_mouse_on_card(mouse_pos)

pygame.quit