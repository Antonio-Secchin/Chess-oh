import random

class Deck(object):
    def __init__(self, player, size = 0):
        self.size = size
        self.actual_size = size
        self.cards = list()
        self.gy = list()
        self.player = player

    def AddToDeck(self, card = None, cards = None):
        if card:
            self.cards.append(card)  # Use append para adicionar um único card
            self.size += 1
            self.actual_size += 1
        if cards:
            self.cards.extend(cards)  # Use extend para adicionar uma lista de cards
            self.size += len(cards)
            self.actual_size += len(cards)

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
            if self.actual_size == 0:
                return None
            self.gy.append(self.cards.pop())  # Adiciona a carta como um item na tupla
            self.actual_size -= 1
            
    def Shuffle(self):
        random.shuffle(self.cards)
        