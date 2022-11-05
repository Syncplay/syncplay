import os

if "QT_PREFERRED_BINDING" not in os.environ:
    os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(
        ["PySide6", "PySide2", "PySide", "PyQt5", "PyQt4"]
    )

try:
    from syncplay.ui.gui import MainWindow as GraphicalUI
except ImportError:
    pass
from syncplay.ui.consoleUI import ConsoleUI


def getUi(graphical=True, passedBar=None):
    if graphical:
        ui = GraphicalUI(passedBar=passedBar)
    else:
        ui = ConsoleUI()
        ui.setDaemon(True)
        ui.start()
    return ui
