from syncplay.ui.gui import MainDialog as GraphicalUI
from syncplay.ui.consoleUI import ConsoleUI

def getUi(graphical=True):
    if(graphical): #TODO: Add graphical ui
        ui = GraphicalUI()
    else:
        ui = ConsoleUI()
        ui.setDaemon(True)
        ui.start()
    return ui 
