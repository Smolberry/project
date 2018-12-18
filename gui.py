import main as gamebot
import pickle
import tkinter

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

class thegui(tkinter.Tk):
    def __init__(self):
        
