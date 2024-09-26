import pygame

class Hand(object):
    def __init__(self, startHand, endHand):
        self.cards = list()
        self.startHand = startHand
        self.endHand = endHand

    def AddToHand(self, card = None, cards = None):
        if card:
            self.cards.append(card)  # Use append para adicionar um único card
        if cards:
            self.cards.extend(cards)
    
    def RemoveFromHand(self,card):
        self.cards.remove(card)


    # def DrawHand(self, screen):
    #     if len(self.cards) == 0:
    #         return
    #     size = self.endHand[0] - self.startHand[0]
    #     sizePerCard = size / len(self.cards)
        
    #     for i, card in enumerate(self.cards):
    #         # Assume-se que 'card' seja uma superfície que pode ser desenhada com o blit
    #         screen.blit(card.get_img(), (sizePerCard * i + self.startHand[0], self.startHand[1]))

    def DrawHand(self, screen, mouse_pos):
        if len(self.cards) == 0:
            return
        size = self.endHand[0] - self.startHand[0]
        sizePerCard = size / len(self.cards)

        # Pega o índice da carta que o mouse está em cima, se houver
        card_index_under_mouse = self.Get_card_index_at_mouse(mouse_pos)

        for i, card in enumerate(self.cards):
            # Calcula a posição da carta
            card_x = sizePerCard * i + self.startHand[0]
            card_y = self.startHand[1]

            if i == card_index_under_mouse:
                # Aumenta o tamanho da carta em 20%
                card_img = card.get_img()
                enlarged_img = pygame.transform.smoothscale(card_img, 
                                 (int(card_img.get_width() * 1.8), int(card_img.get_height() * 1.8)))
                # Desenha a carta maior
                screen.blit(enlarged_img, (card_x, card_y - 500))  # Eleva um pouco para dar efeito de destaque
            else:
                # Desenha a carta no tamanho normal
                screen.blit(card.get_img(), (card_x, card_y))

        
    def Get_card_index_at_mouse(self, mouse_pos):
        """Retorna o índice da carta sob o mouse ou None se não houver carta."""
        if len(self.cards) == 0:
            return None
        
        mouse_x, mouse_y = mouse_pos

        # Verifica se o mouse está dentro da área vertical da mão
        card_height = self.cards[0].get_height()  # Assume que todas as cartas têm a mesma altura
        if not (self.startHand[1] <= mouse_y <= self.startHand[1] + card_height):
            return None

        # Tamanho total da área ocupada pelas cartas
        size = self.endHand[0] - self.startHand[0]
        sizePerCard = size / len(self.cards)

        # Verifica se o mouse está na área horizontal onde as cartas estão
        if self.startHand[0] <= mouse_x <= self.endHand[0]:
            card_index = int((mouse_x - self.startHand[0]) / sizePerCard)

            if 0 <= card_index < len(self.cards):
                return card_index

        return None
    

    def Get_card_at_mouse(self, mouse_pos):
        if len(self.cards) == 0:
            return None
        
        # Posição do mouse
        mouse_x, mouse_y = mouse_pos

        card_height = self.cards[0].get_height()
        # Verifica se o mouse está na área vertical onde as cartas estão
        if not (self.startHand[1] <= mouse_y <= self.startHand[1] + card_height):
            return None

        # Tamanho total da área ocupada pelas cartas
        size = self.endHand[0] - self.startHand[0]
        sizePerCard = size / len(self.cards)

        # Verifica se o mouse está na área horizontal onde as cartas estão
        if self.startHand[0] <= mouse_x <= self.endHand[0]:
            # Calcula o índice da carta com base na posição horizontal do mouse
            card_index = int((mouse_x - self.startHand[0]) / sizePerCard)

            # Retorna a carta correspondente
            if 0 <= card_index < len(self.cards):
                return self.cards[card_index]

        return None