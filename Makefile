BIN_PATH          = /usr/bin
LIB_PATH          = /usr/lib
APP_SHORTCUT_PATH = /usr/share/applications
ICON_PATH         = /usr/share/icons

install:
	touch $(BIN_PATH)/syncplay
	echo '#!/bin/sh\npython $(LIB_PATH)/syncplay/syncplayClient.py "$$@"' > $(BIN_PATH)/syncplay
	chmod a+x $(BIN_PATH)/syncplay
	touch $(BIN_PATH)/syncplay-server
	echo '#!/bin/sh\npython $(LIB_PATH)/syncplay/syncplayServer.py "$$@"' > $(BIN_PATH)/syncplay-server
	chmod a+x $(BIN_PATH)/syncplay-server
	mkdir $(LIB_PATH)/syncplay/
	cp syncplayClient.py $(LIB_PATH)/syncplay/
	cp syncplayServer.py $(LIB_PATH)/syncplay/
	cp -r syncplay $(LIB_PATH)/syncplay/
	cp syncplay.desktop $(APP_SHORTCUT_PATH)/
	cp syncplay-server.desktop $(APP_SHORTCUT_PATH)/
	cp icon.ico $(ICON_PATH)/

uninstall:
	rm $(BIN_PATH)/syncplay
	rm $(BIN_PATH)/syncplay-server
	rm -rf $(LIB_PATH)/syncplay
	rm $(APP_SHORTCUT_PATH)/syncplay.desktop
	rm $(APP_SHORTCUT_PATH)/syncplay-server.desktop
	rm $(ICON_PATH)/icon.ico
