from classes.cards.card import CardTemplate

class Gan_duv(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)
        self.archtype = "duvidosa"
        self.cost_value = 2

    def Effect_cost(self):
        return (self.cost_value,"Any")
    
    def Effect(self, ally_Deck = None, ally_Hand = None, enemy_Deck = None, enemy_Hand = None):
        ally_Hand.AddToHand(cards = ally_Deck.Draw(2))