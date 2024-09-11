class Deck(object):
    def __init__(self, player, size = 20, cards = None):
        self.size = size
        self.actual_size = size
        self.cards = list(cards)
        self.gy = list(None)
        self.player = player

    def AddToDeck(self, card = None, cards = None):
        if card:
            self.cards.__add__(card)
        if cards:
            for c in cards:
                self.cards.__add__(c)

    def Draw(self, qtd):
        aux = ()
        for _ in range(qtd):
            aux += (self.cards.pop(),)  # Adiciona a carta como um item na tupla
        return aux
    
    def SendToGrave(self, qtd):
        for _ in range(qtd):
            self.gy.__add__(self.cards.pop())  # Adiciona a carta como um item na tupla
        