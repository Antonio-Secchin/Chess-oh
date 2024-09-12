class Deck(object):
    def __init__(self, player, size = 20):
        self.size = size
        self.actual_size = size
        self.cards = list()
        self.gy = list()
        self.player = player

    def AddToDeck(self, card = None, cards = None):
        if card:
            self.cards.append(card)  # Use append para adicionar um único card
        if cards:
            self.cards.extend(cards)  # Use extend para adicionar uma lista de cards

    def Draw(self, qtd):
        if self.actual_size == 0:
            return None
        aux = ()
        self.actual_size -= qtd
        for _ in range(qtd):
            aux += (self.cards.pop(),)  # Adiciona a carta como um item na tupla
        return aux
    
    def SendToGrave(self, qtd):
        for _ in range(qtd):
            self.gy.append(self.cards.pop())  # Adiciona a carta como um item na tupla
        