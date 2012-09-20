from syncplay.ui.gui import GraphicalUI
from syncplay.ui.consoleUI import ConsoleUI

def getUi(graphical = True):
    if(False): #graphical): #TODO: Add graphical ui
        ui = GraphicalUI()
    else:
        ui = ConsoleUI()
    ui.setDaemon(True)
    ui.start()
    return ui 