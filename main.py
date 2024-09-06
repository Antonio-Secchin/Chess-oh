import copy
import random
import pygame

pygame.init()
width = 1200
height = 900
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("Chess-OH")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
turns = 0

# Carregar as imagens das cartas (suponha que você tenha as imagens)
card1 = pygame.image.load('cards/exploracao_duvidosa.png')  # substitua pelo caminho correto
card2 = pygame.image.load('cards/ganancia_duvidosa.png')
card3 = pygame.image.load('cards/sacrificio_planejado.png')
card4 = pygame.image.load('cards/cardback_black.jpg')
card5 = pygame.image.load('cards/cardback_white.jpg')


# Redimensionar as imagens se necessário
card1 = pygame.transform.scale(card1, (200, 300))  # Tamanho ajustado para as cartas
card2 = pygame.transform.scale(card2, (200, 300))
card3 = pygame.transform.scale(card3, (200, 300))
card4 = pygame.transform.scale(card4, (200, 300))
card5 = pygame.transform.scale(card5, (200, 300))

# Definir as posições das cartas
card1_pos = (100, 600)
card2_pos = (260, 600)
card3_pos = (420, 600)
card4_pos = (1000,600)
card5_pos = (1000,0)



run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')

    screen.blit(card1, card1_pos)
    screen.blit(card2, card2_pos)
    screen.blit(card3, card3_pos)
    screen.blit(card4, card4_pos)
    screen.blit(card5, card5_pos)

    pygame.display.flip()

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit