from classes.cards.card import CardTemplate

class Sac_pla(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)
        self.cost_value = 5
        self.type = "rook"

    def Effect_cost(self):
        return (self.cost_value,self.type)
    
    def Effect(self, ally_Deck = None, ally_Hand = None, enemy_Deck = None, enemy_Hand = None):
        return (("Skip", 1), ("QtdPlay", 2))