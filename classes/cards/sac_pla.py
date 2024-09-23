from classes.cards.card import CardTemplate

class Sac_pla(CardTemplate):
    def __init__(self, name, img, text):
        super().__init__(name, img, text)

    def effect_cost(self):
        pass