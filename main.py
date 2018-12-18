# A game
# Open world
#   Navigation system, keep track of players
# Players will have their own id's
# Main navigation class
#   subclass for each navigation class
# Different chats are different cities
import json
import os
import types
import pickle
import re
gamedata = "gamedata.tgbot"

class Game:
    """docstring for the game (mostly data)."""
    def __init__(self):
        pass
    def writeData(self, data):
        if os.path.isfile(gamedata):
            try:
                file = open(gamedata, 'wb+')
                picle.dump(data, file)
                file.close()
                return True
            except:
                return False
        else:
            try:
                file = open(gamedata, 'wb+')
                pickle.dump(data, file)
                file.close()
                return True
            except:
                return False
    def getData(self):
        if os.path.isfile(gamedata):
            file = open(gamedata, 'rb')
            tempvar = pickle.load(file)
            file.close()
            return tempvar
        else:
            return {}

class Navigation(Game):
    """Main navigation class"""
    def __init__(self):
        Game.__init__(self)
        self.players = {}
        self.data = self.getData()
        self.spawn = Room()
        self.rooms = []
    def get_players(self):
        return self.players
    def set_player(self, player):
        if isinstance(player, Player):
            self.players[player.get_ident()] = player
    def rem_player(self, player):
        if player in self.players.values():
            del self.players[player.get_ident()]
    def set_spawn(self, room):
        if isinstance(room, Room):
            self.spawn = room
            return True
        else:
            return False

#Goes inside navigation
class Room(Game):
    def __init__(self):
        Game.__init__(self)
        self.name = "Placeholder"
        self.exits = {}
        self.desc = ""
        self.objects = {}
        self.objdesc = ""
        self.ident = 0
        self.players = []
    def go(self, player):
        player.set_location(self)
    def get_exits(self):
        return self.exits
    def add_exit(go):
        if isinstance(go, Room, direction) and not direction in self.exits.keys():
            self.exits[direction] = go.go
    def get_name(self):
        return self.name
    def set_name(self, name):
        if isinstance(name, str):
            self.name = name
            return True
        else:
            return False
    def set_desc(self, desc):
        if isinstance(desc, str):
            self.desc = desc
            return True
        else:
            return False
    def get_obj(self):
        result = ""
        for i in self.objects.keys():
            if self.objects[i].viewable == True:
                result += "     " + self.objects[i].description + "\n"
class Player(Game):
    """Player class, will dictate inventory, status and location.
        Will have a location variable
    """
    def __init__(self):
        Game.__init__(self)
        self.age = 18
        self.name = "Foobar"
        self.gender = "Heck"
        self.species = "dragon"
        self.height = 108
        self.inventory = []
        self.active_chats = []
        self.data = self.getData()
        self.ident = 0
        self.location = 0
        self.stats = Attrib()
    def __str__(self):
        """Will return the name, age, gender, species and height of player."""
        return "The player '%s' is %s, a %s %s. Their age is %s" % (self.name, self.get_height_metric(), self.gender, self.species, str(self.age))
    def set_location(self, room):
        if isinstance(room, Room):
            self.location = room.ident
            return True
        else:
            return False
    def get_location(self):
        return self.location
    def get_height_metric(self):
        if self.height % 12 == 0:
            result = format(self.height / 12, ".0f") + "'"
        else:
            result = "%s'%s\"" % (format(self.height / 12, ".0f"), self.height % 12)
        return result
    def get_age(self):
        return self.age
    def set_age(self, age):
        self.age = age
    def get_gender(self):
        return self.gender
    def set_gender(self, gender):
        self.gender = gender
    def get_species(self):
        return self.species
    def set_species(self, species):
        self.species = species
    def set_height(self, height):
        self.height = height
    def get_height(self):
        return self.height
    def set_name(self, name):
        if isinstance(name, str):
            self.name = name
            return True
        else:
            return False
    def set_ident(self, ident):
        if isinstance(ident, int):
            self.ident = ident
            return True
        else:
            return False
    def get_ident(self):
        return self.ident
    def add_inventory(self, item):
        """Adds an item to the inventory, if there is already an item of the same type it just increases the amount"""
        if isinstance(item, InventoryObject):
            if not item in self.inventory:
                self.inventory.append(item)
                return True
            else:
                counter = 0
                for i in self.inventory:
                    if i.ident == item.ident:
                        self.inventory[counter].amount += item.amount
                    counter += 1
        else:
            return False
    def rem_inventory(self, item):
        """Removes an item from the inventory, if there is already an item of the same type
         it decreases the amount, or if the amount of the item in the inventory is
         lesser than the item being subtracted it removes it"""
        if isinstance(item, InventoryObject):
            if item in self.inventory:
                self.inventory.remove(item)
            else:
                counter = 0
                for i in self.inventory:
                    if i.ident == item.ident and i.amount > item.amount:
                        self.inventory[counter].amount -= item.amount
                    elif i.ident == item.ident and i.amount < item.amount:
                        del self.inventory[counter]
                    counter += 1
            return True
        else:
            return False
    # For use in game
    def add_chat(self, chat):
        if isinstance(chat, DialogueTree) and not chat in self.active_chats:
            self.active_chats.append(chat)
            return True
        else:
            return False
    #Won't work, it's not set up like that, look will have to be in the later mechanics
##    def look(self):
##        total = ""
##        total += self.location.description + "\n"
##        total += self.location.objdesc
        
class Attrib:
    def __init__(self):
        self.strength = 5
        self.libido = 0
        self.speed = 5
        self.health = 5
        self.luck = 5
        self.charisma = 5
        self.athleticism = 5
        self.armor = 0
        self.regen = 5
        self.attacks = {}
        self.pvpenabled = True
        self.damageTaken = 0
        self.defeat = False
        self.gold = 0
    def getHP(self):
        return self.health * 100 - self.damageTaken
    def defeated(winner):
        if self.gold > 0:
            winner.receiveGold(int(self.gold*0.02))
            self.gold -= int(self.gold * 0.02)
            self.defeat = True
            
    def receiveGold(amount):
        self.gold += amount
class InventoryObject(Game):
    """docstring for InventoryObject."""
    def __init__(self):
        Game.__init__(self)
        self.name = "Placeholder"
        self.ident = 0
        self.value = 0
        self.amount = 1
        self.foundin = []
        self.findable = False
        self.buyable = False
        self.tradeable = False

class WorldObject(Game):
    """docstring for WorldObject.
        Objects within the world, may be npcs, general objects or doors.
    """
    def __init__(self):
        Game.__init__(self)
        self.name = "Placeholder"
        self.interactable = False
        self.NPC = False
        self.desc = ""
        self.interactions = {}
        self.door = False
        self.isopen = False
        self.ident = 0
        self.spawnchance = 0
        self.viewable = True
        self.inventory = {}
    def open(self):
        if self.door and "open" in self.interactions.keys() and self.interactable:
            return self.__interactions["open"]
        else:
            return "You can't open this"
    def look(self):
        if self.interactable and "look" in self.interactions.keys():
            return self.interactions["look"]
        else:
            return "You don't see anything of interest."
    def enter(self):
        if self.door and self.isopen and self.interactable and "enter" in self.interactions:
            return self.interactions["enter"]
        else:
            return "You can't enter this"
    def initiateDia(self, player):
        """Called when a player tries to talk to an object (mainly for npc)"""
        if isinstance(player, Player):
            if self.interactable and "initiate" in self.interactions.keys():
                tempvar = self.interactions["initiate"]()
                player.add_chat(tempvar)
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def set_interactable(self, tf):
        if isinstance(tf, bool):
            self.interactable = tf
            return True
        else:
            return False
    def set_door(self, tf):
        if isinstance(tf, bool):
            self.door = tf
            return True
        else:
            return False
    def get_open(self):
        return self.isopen
    def get_ident(self):
        return self.ident
    def set_ident(self, ident):
        if isinstance(ident, int):
            self.ident = ident
    def set_description(self, desc):
        if isinstance(desc, str):
            self.desc = desc
    def set_interactions(self, interactions):
        if isinstance(interactions, dict):
            self.interactions = dict
    def add_contents(self, item):
        if isinstance(item, InventoryObject):
            if item.ident not in self.inventory.keys():
                self.inventory[item.ident] = item
            else:
                self.inventory[item.ident].amount += item.amount

class Enemy(WorldObject):
    def __init__(self):
        WorldObject.__init__(self)
        self.type = ""
        self.HP = 10
        self.attack = 1

class NPC(WorldObject):
    """docstring for NPC."""
    def __init__(self):
        WorldObject.__init__(self)
        self.dialogue = {}
        self.age = 0
        self.gender = "Heck"
        self.species = "Dragon"
        self.height = 108
        self.interactions["initiate"] = self.get_tree
    def get_height_metric(self):
        if self.height % 12 == 0:
            result = format(self.height / 12, ".0f") + "'"
        else:
            result = "%s'%s\"" % (format(self.height / 12, ".0f"), self.height % 12)
        return result
    def get_age(self):
        return self.age
    def set_age(self, age):
        self.age = age
    def get_gender(self):
        return self.gender
    def set_gender(self, gender):
        self.gender = gender
    def get_species(self):
        return self.species
    def set_species(self, species):
        self.species = species
    def set_height(self, height):
        self.height = height
    def get_height(self):
        return self.height
    def get_tree(self):
        tempvar = DialogueTree(self.dialogue)
        return tempvar
    def set_dialogue(self, dialogue):
        if isinstance(dialogue, dict):
            self.dialogue = dict

class DialogueTree(NPC):
    """docstring for DialogueTree.
        Basically holds the position for dialogue
    """
    def __init__(self, arg):
        NPC.__init__(self)
        self.position = arg
    def talk(self, inter):
        if inter in self.position.keys():
            self.position = self.position[inter]
            return self.position[inter]["response"]
        else:
            return "That is not a dialogue option"
    def get_options(self):
        return list(self.position.keys())
    def set_position(self, pos):
        self.position = pos

class City(Game):
    """City object, essentially represents a chat."""
    def __init__(self):
        Game.__init__(self)
        self.players = {}
        self.current = ""
        self.cities = {}
        self.data = self.getData()
        self.ident = 0
        self.objects = []
        self.objIdents = []
        self.nav = Navigation()
        if "cities" in self.data.keys():
            self.cities = self.data["cities"]
    def set_name(self, name):
        self.current = name
    def get_name(self):
        return self.current
    def set_ident(self, ident):
        self.ident = ident
    def get_ident(self):
        return self.ident
    def get_players(self):
        return self.players
    def set_spawn(self, room):
        if isinstance(room, Room):
            self.nav.set_spawn(room)
            return True
        else:
            return False
    def create_room(self, name, desc):
        tempvar = Room()
        tempvar.set_name(name)
        tempvar.set_desc(desc)
        self.nav.rooms.append(tempvar)
    def create_worldobj(self, ident, name="Placeholder", interactions={}, interactable=False, description=""):
        if not ident in self.objIdents:
            tempvar = WorldObject()
            tempvar.set_name(name)
            tempvar.set_interactable(interactable)
            tempvar.set_description(description)
            tempvar.set_interactions(interactions)
            tempvar.set_ident(ident)
            self.objIdents.append(ident)
            self.objects.append(tempvar)
            return True
        else:
            return False
    def create_npc(self, ident, name="Placeholder", interactions={}, interactable=False, description="", height=64, age=18, gender="foobar", species="Dragon", dialogue={}):
        if not ident in self.objIdents:
            tempvar = NPC()
            tempvar.set_age(age)
            tempvar.set_name(name)
            tempvar.set_interactions(interactions)
            tempvar.set_gender(gender)
            tempvar.set_description(description)
            tempvar.set_interactable(interactable)
            tempvar.set_height(height)
            tempvar.set_dialogue(dialogue)
            tempvar.set_ident(ident)
            self.objIdents.append(ident)
            self.objects.append(tempvar)
            return True
        else:
            return False
    def create_player(self, ident, name="Placeholder", height=69, age=18, gender="foobar", species="dragon"):
        if not ident in self.players.keys():
            tempvar = Player()
            tempvar.set_age(age)
            tempvar.set_name(name)
            tempvar.set_gender(gender)
            tempvar.set_height(height)
            tempvar.set_species(species)
            tempvar.set_ident(ident)
            self.players[ident] = tempvar
            self.nav.set_player(tempvar)
            return True
        else:
            return False
    def edit_player(player):
        if isinstance(player, Player):
            self.players[player.get_ident()] = player
    def get_nav(self):
        return self.nav
    def edit_nav(self, nav):
        if isinstance(nav, Navigation):
            self.nav = nav
class Director(Game):
    """docstring for Director."""
    def __init__(self):
        Game.__init__(self)
        self.data = self.getData()
        self.cities = {}
        self.items = {}
        if "cities" in self.data.keys():
            self.get()
    def store(self):
        """Actually stores the game data"""
        self.data["cities"] = self.cities
        self.writeData(self.data)
    def get(self):
        """Actually gets the game data"""
        self.data = self.getData()
        self.cities = self.data["cities"]
        if "items" in self.data.keys():
            self.items = self.data["items"]
    def create_city(self, name, ident):
        if len(re.compile("[^abcdefghijklmnopqrstuvwxyz]").findall(name.lower())) == 0 and isinstance(ident, int):
            tempvar = City()
            tempvar.set_name(name)
            tempvar.set_ident(ident)
            self.cities[ident] = tempvar
            return True
        else:
            return False
    def get_cities(self):
        return self.cities
    def edit_city(self, city):
        if isinstance(city, City):
            self.cities[city.get_ident()] = city
        else:
            return False
