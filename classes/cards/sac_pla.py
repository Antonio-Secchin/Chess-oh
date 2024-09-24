from classes.cards.card import CardTemplate

class Sac_pla(CardTemplate):
    def __init__(self, name, img, text, x_scale, y_scale):
        super().__init__(name, img, text, x_scale, y_scale)

    def Effect_cost(self):
        pass