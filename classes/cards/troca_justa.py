from classes.cards.card import CardTemplate

class Troca_justa(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)
        self.cost_value = 0
        self.type = "pawn"

    def Effect_cost(self):
        return (self.cost_value,"Any")
    
    def Effect(self, ally_Deck = None, ally_Hand = None, enemy_Deck = None, enemy_Hand = None):
        ally_Hand.AddToHand(cards = ally_Deck.Draw(1))
        return (("Place", "Any"), ("Enemy","pawn"))