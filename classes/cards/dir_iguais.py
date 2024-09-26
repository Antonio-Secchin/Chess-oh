from classes.cards.card import CardTemplate

class Dir_iguais(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)
        self.cost_value = 0
        self.type = "Imp"

    def Effect_cost(self):
        return (self.cost_value,self.type)
    
    def Effect(self, ally_Deck = None, ally_Hand = None, enemy_Deck = None, enemy_Hand = None):
        return ("Skip", 1)