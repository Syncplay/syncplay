'''
Created on 05-07-2012

@author: Uriziel
'''
from __future__ import print_function
import threading


class ConsoleUI(threading.Thread):
    def __init__(self):
        self.promptMode = threading.Event()
        self.PromptResult = ""
        self.promptMode.set()
        self._syncplayClient = None
        threading.Thread.__init__(self, name="ConsoleUI")
        
    def addClient(self, client):
        self._syncplayClient = client
        
    def run(self):
        try:
            while True:
                data = raw_input()
                if not data:
                    break
                data = data.rstrip('\n\r')
                if(not self.promptMode.isSet()):
                    self.PromptResult = data
                    self.promptMode.set()
                elif(self._syncplayClient):
                    self._syncplayClient.execute_command(data)
        except:
            raise
        
    def promptFor(self, promptName = ">", message = ""):
        print(message)
        self.promptMode.clear()
        print(promptName+": ", end='')
        self.promptMode.wait()
        return self.PromptResult

    def showMessage(self, message):
        print(message)

    def showDebugMessage(self, message):
        print(message)
        
    def showErrorMessage(self, message):
        print(message)
