from classes.cards.card import CardTemplate

class Est_alt(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)
        self.cost_value = 0

    def Effect_cost(self):
        return (self.cost_value,"Any")
    
    def Effect(self, ally_Deck = None, ally_Hand = None, enemy_Deck = None, enemy_Hand = None):
        enemy_Deck.SendToGrave(3)