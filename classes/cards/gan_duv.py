from classes.cards.card import CardTemplate

class Gan_duv(CardTemplate):
    def __init__(self, name, img, text):
        super().__init__(name, img, text)
        self.archtype = "duvidosa"
        self.cost_value = 2

    def effect_cost(self):
        return (self.cost_value,"Any")
    
    def effect(self, Ally_deck = None, Ally_hand = None, Enemy_deck = None, Enemy_Hand = None):
        Ally_hand.AddToHand(cards = Ally_deck.Draw(2))