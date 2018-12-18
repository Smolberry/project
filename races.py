# Races
from main import Attrib
import pickle

dragon = "\
A fiersome beast capable of destroying entire armies with little care for the burdens they encounter.\
"

class Dragon(Attrib):
    def __init__(self):
        Attrib.__init__(self):
        self.strength += 5
        self.libido += 5
        self.speed += 1
        self.health += 10
        self.luck -= 4
        self.charisma -= 2
        self.athleticism -= 2
        self.description = dragon
    def claw(enemy=None, player=None):
        if enemy != None:
            pass
        if player != None and player.stats.pvpenabled:
            if player.stats.armor == self.strength * 0.8:
                player.stats.armor = 0
            elif player.stats.armor < self.strength * 0.8:
                player.stats.armor = 0
                if player.stats.getHP() < self.strength * 0.8:
                    player.stats.defeated(self)
                elif player.stats.getHP() > self.strength * 0.8:
                    player.stats.damageTaken += self.strength * 0.8
