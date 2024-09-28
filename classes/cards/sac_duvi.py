from classes.cards.card import CardTemplate

class Sac_duvi(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)
        self.archtype = "duvidosa"
        self.cost_value = 9
        self.type = "queen"
        self.type_res = 'pawn'
        self.res_qtd = 9

    def Effect_cost(self):
        return (self.cost_value,"queen")
    
    def Effect(self, ally_Deck = None, ally_Hand = None, enemy_Deck = None, enemy_Hand = None):
        return (("Place", "Near"), ("Ally","pawn"), ("Qtd",self.res_qtd))