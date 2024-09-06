class Card(object):
    card_type = None

    
    def __init__(self, id, name, img, text, duelist):
        self.id = id
        self.name = name
        self.img = img
        self.text = text
        self.card_owner = duelist
        self.current_user = None
        self.is_set = False
        self.in_hand = True
        
        # self.fusion_types_string = "Fusion types: "
        # for x in range(len(fusion_types_array)):
        #     if fusion_types_array[x] == fusion_types_array[-1]:
        #         self.fusion_types_string += fusion_types_array[x]
        #     else:
        #         self.fusion_types_string += fusion_types_array[x] + ", "

    def getUser(self):
        return self.current_user
        
    def getName(self):
        return self.name
        
    def getType(self):
        return self.card_type

    def setUser(self, current_user):
        self.current_user = current_user

    def removeFromPlace(self, mode):
        if mode == "To hand":
            self.returnToHand(self.card_owner)
            return
        elif mode == "To graveyard":
            #print(self.current_zone)
            self.current_zone.zone_gui.card_img = None
            self.current_zone = None
            self.sendToGrave(self.card_owner)
            #print('q', self.current_zone)
            return

    def returnToHand(self, owner):
        owner.addToHand(self)
        self.current_zone = None

    def sendToGrave(self, owner):
        owner.duelist_zone.graveyard.placeCardToZone(self)
        
    def setZone(self, zone):
        self.current_zone = zone
        
    def activate(self):
        return None

    def selectGuardianStar(self):
        return None
        
    def set(self):
        self.is_set = True
        self.selectGuardianStar()

class SpellOrTrapCard(Card):
    will_animate = False
    single_card_animation = False

def __init__(self, id, name, img, text, duelist, spell_or_trap_type):
    super().__init__(id, name, img, text, duelist)
    self.spell_or_trap_type = spell_or_trap_type
    self.set_for_ai = True
    self.has_been_activated = False
    
def getSpellOrTrapType(self):
    return self.spell_or_trap_type
    
def effect(self):
    return None
    
def isActivationValid(self):
    return self.effect(testing=True)
    
def activate(self):
    self.has_been_activated = True
    self.is_set = False
    #self.effect()
    if self.spell_or_trap_type == "Normal":
        self.current_zone.removeCardFromZone(self, "To graveyard")

class SpellCard(SpellOrTrapCard):
    card_type = "Spell"

class FieldSpellCard(SpellCard):
    def effect(self, testing=False):
        return True
        
    def aiUseCondition(gi):
        return True

class TrapCard(SpellOrTrapCard):
    card_type = "Trap"
