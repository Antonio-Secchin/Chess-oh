import copy
import random
import pygame
import classes

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



run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')

    hand.DrawHand(screen=screen)
    # screen.blit(card1, card1_pos)
    # screen.blit(card2, card2_pos)
    # screen.blit(card3, card3_pos)
    # #screen.blit(card4, card4_pos)
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