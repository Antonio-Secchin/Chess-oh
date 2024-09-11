import copy
import random
import pygame
import classes

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

deck = list(range(1,21))
hand = list()
random.shuffle(deck)
print(deck)
print(deck.pop(0))
print(deck)
# Carregar as imagens das cartas (suponha que você tenha as imagens)
card1 = pygame.image.load('cards/exploracao_duvidosa.png')  # substitua pelo caminho correto
card2 = pygame.image.load('cards/ganancia_duvidosa.png')
card3 = pygame.image.load('cards/sacrificio_planejado.png')
card4 = pygame.image.load('cards/cardback_black.jpg')
card5 = pygame.image.load('cards/cardback_white.jpg')

x_scale = 150
y_scale = 250
# Redimensionar as imagens se necessário
card1 = pygame.transform.scale(card1, (x_scale,y_scale))  # Tamanho ajustado para as cartas
card2 = pygame.transform.scale(card2, (x_scale,y_scale))
card3 = pygame.transform.scale(card3, (x_scale,y_scale))
card4 = pygame.transform.scale(card4, (x_scale,y_scale))
card5 = pygame.transform.scale(card5, (x_scale,y_scale))

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
    screen.fill('black')

    screen.blit(card1, card1_pos)
    screen.blit(card2, card2_pos)
    screen.blit(card3, card3_pos)
    #screen.blit(card4, card4_pos)
    x = 0
    for i in range(0,5):
        screen.blit(card5, (width - x_scale - 25 + x, 25 - x))
        screen.blit(card4, (width - x_scale - 25 + x, height - y_scale -x))
        x += 5

    pygame.display.flip()

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    mouse_pos = pygame.mouse.get_pos()

pygame.quit