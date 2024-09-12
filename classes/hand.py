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


    def DrawHand(self, screen):
        if len(self.cards) == 0:
            return
        size = self.endHand[0] - self.startHand[0]
        sizePerCard = size / len(self.cards)
        
        for i, card in enumerate(self.cards):
            # Assume-se que 'card' seja uma superfície que pode ser desenhada com o blit
            screen.blit(card.get_img(), (sizePerCard * i + self.startHand[0], self.startHand[1]))

    def is_mouse_on_card(self,mouse_pos):
        if len(self.cards) == 0 or mouse_pos[1] < self.startHand[1]:
            return - 1
        size = self.endHand[0] - self.startHand[0]
        sizePerCard = size / len(self.cards)
        posx = round((mouse_pos[0] - self.startHand)/sizePerCard)
        card = self.cards[posx]
        
    