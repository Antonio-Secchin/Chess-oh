from classes.cards.card import CardTemplate

class Isso_meu(CardTemplate):
    def __init__(self, name, img, text):
        super().__init__(name, img, text)
        self.archtype = "duvidosa"
        self.cost_value = 2

    def effect_cost(self):
        return None
    
    def effect(self, Ally_deck = None, Ally_hand = None, Enemy_deck = None, Enemy_Hand = None):
        Ally_hand.AddToHand(cards = Enemy_deck.Draw(1))