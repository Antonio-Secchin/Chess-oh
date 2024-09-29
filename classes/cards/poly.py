from classes.cards.card import CardTemplate

class Poly(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)
        self.cost_qtd = 2
        self.res_qtd = 1
        self.type_res = "custom"

    def Effect_cost(self):
        return (self.cost_qtd,"Fusion")
    
    def Effect(self, ally_Deck = None, ally_Hand = None, enemy_Deck = None, enemy_Hand = None):
        return (("Place", "Near"), ("Ally", self.type_res), ("Qtd",self.res_qtd))