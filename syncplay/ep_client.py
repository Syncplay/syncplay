# coding:utf8
import sys

from syncplay.clientManager import SyncplayClientManager
from syncplay.utils import blackholeStdoutForFrozenWindow

def main():
    blackholeStdoutForFrozenWindow()
    SyncplayClientManager().run()

if __name__ == "__main__":
    main()