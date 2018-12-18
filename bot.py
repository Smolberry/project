import telegram
import main as gamebot
import pickle
import os
import logging
from telegram.ext import Updater, CommandHandler, BaseFilter, MessageHandler
import threading
import time
import random

configpath = "gameconfig.tgbot"
def writeToFile(elements):
    if os.path.isfile(configpath):
        try:
            file = open(configpath, 'wb')
            pickle.dump(elements, file)
            file.close()
        except:
            file.close()
    else:
        file = open(configpath, 'wb+')
        pickle.dump(elements, file)
        file.close()

def getFromFile():
    if os.path.isfile(configpath):
        file = open(configpath, 'rb')
        stuff = pickle.load(file)
    else:
        stuff = {}
    return stuff

def createCity(thebot, update, args):
    if len(args) > 0:
        thing = bot.game.create_city(args[0], update.message.chat_id)
        print("Did it")
        print(thing)
        if thing:
            update.message.reply_text("Added city " + args[0])
        else:
            update.message.reply_text("Could not add city %s, either this chat is already a city or you should review the help docs." % args[0])

def checkIfReply(message):
    if message.from_user.id in bot.registrations.keys():
        if message.reply_to_message.message_id in bot.registrations[message.from_user.id].keys():
            if bot.registrations[message.from_user.id][message.reply_to_message.message_id] == "name":
                bot.registrations[message.from_user.id]["name"] = message.text
                message.reply_to_message.edit_text("Name: "+ message.text)
            elif bot.registrations[message.from_user.id][message.reply_to_message.message_id] == "gender":
                bot.registrations[message.from_user.id]["gender"] = message.text
                message.reply_to_message.edit_text("Gender: "+ message.text)
            elif bot.registrations[message.from_user.id][message.reply_to_message.message_id] == "species":
                bot.registrations[message.from_user.id]["species"] = message.text
                message.reply_to_message.edit_text("Species: "+ message.text)
            elif bot.registrations[message.from_user.id][message.reply_to_message.message_id] == "age":
                bot.registrations[message.from_user.id]["age"] = message.text
                message.reply_to_message.edit_text("Age: "+ message.text)
            elif bot.registrations[message.from_user.id][message.reply_to_message.message_id] == "height":
                bot.registrations[message.from_user.id]["height"] = message.text
                message.reply_to_message.edit_text("Height: "+ message.text)
            elif bot.registrations[message.from_user.id][message.reply_to_message.message_id] == "city":
                if message.text in bot.getCityNames():
                    bot.registrations[message.from_user.id]["city"] = message.text
                    message.reply_to_message.edit_text("City: "+ message.text)
        else:
            pass
        if "name" in bot.registrations[message.from_user.id] and "gender" in bot.registrations[message.from_user.id] and "species" in bot.registrations[message.from_user.id] and "age" in bot.registrations[message.from_user.id] and "height" in bot.registrations[message.from_user.id] and "city" in bot.registrations[message.from_user.id]:
            createRegistry(bot.registrations[message.from_user.id], message.chat_id, message.from_user.id)
            message.reply_text("Registered")
        else:
            pass


def getPlayerInfo(thebot, update, args=None):
    if update.message.chat_id in bot.game.cities.keys():
        if update.message.from_user.id in bot.game.cities[update.message.chat_id].players.keys():
            update.message.reply_text(str(bot.game.cities[update.message.chat_id].players[update.message.from_user.id]))
        else:
            update.message.reply_text("You are not a player in this city, please look into migration or creating a new player")
    else:
        update.message.reply_text("This chat is not yet a city")

def dummy(thebot, update):
    print("Dummy")
    print(update.message.text)
    print(update.message.text[0])
    if update.message.text[0] == "/":
        command, args = update.message.text[1:].split(" ")[0], update.message.text[1:].split(" ")[1:]
        print(command, args)
        if command in list(bot.commandlist.keys()):
            print("Executing", command)
            bot.commandlist[command](thebot, update, args)
    pass

def start(thebot, update, args=None):
    name = bot.sendMessage(update.message.chat_id, "Reply with your name")
    gender = bot.sendMessage(update.message.chat_id, "Reply with your gender")
    species = bot.sendMessage(update.message.chat_id, "Reply with your species")
    age = bot.sendMessage(update.message.chat_id, "Reply with your age")
    height = bot.sendMessage(update.message.chat_id, "Reply with your height in inches")
    city = bot.sendMessage(update.message.chat_id, "Reply with the city you'd like to go, your options are: %s" % (", ".join(bot.getCityNames())))
    bot.registrations[update.message.from_user.id] = {name.message_id:"name", gender.message_id:"gender", species.message_id:"species", age.message_id:"age", height.message_id:"height", city.message_id:"city"}
    print(str(bot.registrations))
    
def createRegistry(iden, id, otherid):
    thething = 0
    for i in bot.game.cities.keys():
        if bot.game.cities[i].current == bot.registrations[otherid]["city"]:
            thething = i
    bot.game.cities[thething].create_player(otherid, bot.registrations[otherid]["name"], bot.registrations[otherid]["height"], bot.registrations[otherid]["age"], bot.registrations[otherid]["gender"], bot.registrations[otherid]["species"])

def look(thebot, update, args=None):
    update.message.reply_text(bot.mech.look(update.message.from_user.id, update.message.chat_id))

class Detect(BaseFilter):
    def filter(self, message):
        if message.text != None:
            print("Received message")
            if message.chat.type == "private":
                checkIfReply(message)
            return True

class Mechanics(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game
        self.items = self.getItems()
        self.running = False
    def run(self):
        self.running = True
        while self.running:
            self.turn()
            time.sleep(900)
        pass
    def turn(self):
        for i in self.game.cities.keys():
            #Player regeneration
            # Health = player.stats.health * 100 - player.stats.damageTaken
            # Can essentially regain health by just negating the damage taken
            for u in self.game.cities[i].players.keys():
                regen = 0
                if self.game.cities[i].players[u].stats.damageTaken > 0:
                    if self.game.cities[i].players[u].stats.regen*self.game.cities[i].players[u].stats.health >= self.game.cities[i].players[u].stats.damageTaken:
                        regen = self.game.cities[i].players[u].stats.damageTaken
                    else:
                        regen = int(self.game.cities[i].players[u].stats.regen*self.game.cities[i].players[u].stats.health)
                self.game.cities[i].players[u].stats.damageTaken -= regen
            for item in self.items.keys():
                for t in self.game.cities[i].nav.rooms:
                    if not item.ident in t.objects.keys():
                        if random.randrange(1, 200) == item.ident:
                            newamount = item
                            newamount.amount = random.randrange(1, 3)
                            t.objects[item.ident] = newamount
                    t.get_obj()
    def addItem(self, bot=None, update=None, args=None):
        tempItem = gamebot.InventoryObject()
        tempItem.name = "Stick"
        tempItem.ident = 1
        tempItem.value = 20
        tempItem.findable = True
        tempItem.tradeable = True
        tempObj = gamebot.WorldObject()
        tempObj.name = "Corpse"
        tempObj.ident = 1
        tempObj.viewable = True
        tempObj.interactions["look"] = "A rotting corpse, may have something inside it"
        tempObj.interactable = True
        tempObj.inventory[tempItem.ident] = tempItem
        for i in self.game.cities.keys():
            for t in self.game.cities[i].nav.rooms:
                if tempObj.ident not in t.objects.keys():
                    t.objects[tempObj.ident] = tempObj
        if "items" in self.game.data.keys():
            self.game.data["items"][tempItem.ident] = tempItem
            self.game.store()
        else:
            self.game.data["items"] = {}
            self.game.data["items"][tempItem.ident] = tempItem
            self.game.store()
    def createDefaultRoom(self, thebot=None, update=None, args=None):
        tempvar = gamebot.Room()
        tempvar.name = "Spawn"
        tempvar.desc = "A large open area with no viewable horizon"
        for i in bot.getCities():
            self.game.cities[i].nav.rooms.append(tempvar)
    def getItems(self):
        try:
            self.items = self.game.data["items"]
            return self.items
        except:
            return False
    def look(self, playerid, cityid):
        if cityid in self.game.cities.keys():
            if playerid in self.game.cities[cityid].players.keys():
                for i in self.game.cities[cityid].nav.rooms:
                    if i.ident == self.game.cities[cityid].players[playerid].location:
                        return i.desc + "\n  " + i.objdesc
class cityBot(telegram.Bot):
    def __init__(self):
        self.__variables = getFromFile()
        self.game = gamebot.Director()
        self.registrations = {}
        self.cities = []
        self.mech = Mechanics(self.game)
        for i in list(self.game.cities.keys()):
            self.cities.append(i)
        if "token" in self.__variables.keys():
            self.__token1 = self.__variables["token"]
        else:
            print("No token, please enter the token")
            self.__token1 = ""
            while self.__token1 == "" or self.__token1 == " ":
                self.__token1 = input("Enter the token")
            self.__variables["token"] = self.__token1
            writeToFile(self.__variables)
        try:
            print("Starting bot...")
            self.mech.start()
            self.commandlist = {}
            telegram.Bot.__init__(self, token=self.__token1)
            self.__updater = Updater(token=self.__token1)
            self.__dispatcher = self.__updater.dispatcher
            self.commandlist["createcity"] = createCity
            self.commandlist["start"] = start
            self.commandlist["stop"] = self.shutdown
            self.commandlist["debugitem"] = self.mech.addItem
            self.commandlist["look"] = look
            self.commandlist["debugroom"] = self.mech.createDefaultRoom
            self.reghandler=Detect()
            self.regi = MessageHandler(self.reghandler, dummy)
            self.__dispatcher.add_handler(self.regi)
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
            print("Finished registering commands...")
            self.__updater.start_polling()
        except Exception as err:
            print(err)
    def shutdown(self, bot=None, update=None, args=None):
        print("Saving...")
        self.game.store()
        if update != None:
            update.message.reply_text("Shutting down...")
        print("Shutting down...")
        self.__updater.stop()
    def getCities(self):
        self.cities = []
        for i in list(self.game.cities.keys()):
            self.cities.append(i)
        return self.cities
    def getCityNames(self):
        thing = []
        for i in self.game.cities.keys():
            thing.append(self.game.cities[i].current)
        return thing

bot = cityBot()
