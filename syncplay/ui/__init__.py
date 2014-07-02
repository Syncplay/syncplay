try:
    from syncplay.ui.gui import MainWindow as GraphicalUI
except ImportError:
    pass
from syncplay.ui.consoleUI import ConsoleUI

def getUi(graphical=True):
    if graphical: #TODO: Add graphical ui
        ui = GraphicalUI()
    else:
        ui = ConsoleUI()
        ui.setDaemon(True)
        ui.start()
    return ui 
