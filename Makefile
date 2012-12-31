SINGLE_USER	= false

BASE_PATH	= /usr
LOCAL_PATH	= ~/.local

ifeq ($(SINGLE_USER),false)
	BIN_PATH          = $(BASE_PATH)/bin
	LIB_PATH          = $(BASE_PATH)/lib
	APP_SHORTCUT_PATH = $(BASE_PATH)/share/applications
	ICON_PATH         = $(BASE_PATH)/share
else
	BIN_PATH          = $(LOCAL_PATH)/syncplay
	LIB_PATH          = $(LOCAL_PATH)/syncplay
	APP_SHORTCUT_PATH = $(LOCAL_PATH)/share/applications
	ICON_PATH         = $(LOCAL_PATH)/share
endif

common:
	-mkdir -p $(LIB_PATH)/syncplay/
	cp -r syncplay $(LIB_PATH)/syncplay/
	cp -r resources/hicolor $(ICON_PATH)/icons/
	cp resources/hicolor/48x48/apps/syncplay.png $(ICON_PATH)/app-install/icons/
	cp resources/hicolor/48x48/apps/syncplay.png $(ICON_PATH)/pixmaps/

u-common:
	-rm -rf $(LIB_PATH)/syncplay
	-rm $(ICON_PATH)/icons/hicolor/*/apps/syncplay.png
	-rm $(ICON_PATH)/app-install/icons/syncplay.png
	-rm $(ICON_PATH)/pixmaps/syncplay.png

client:
	-mkdir -p $(BIN_PATH)
	touch $(BIN_PATH)/syncplay
	echo '#!/bin/sh\npython $(LIB_PATH)/syncplay/syncplayClient.py "$$@"' > $(BIN_PATH)/syncplay
	chmod a+x $(BIN_PATH)/syncplay
	cp syncplayClient.py $(LIB_PATH)/syncplay/
	cp resources/syncplay.desktop $(APP_SHORTCUT_PATH)/

u-client:
	-rm $(BIN_PATH)/syncplay
	-rm $(LIB_PATH)/syncplay/syncplayClient.py
	-rm $(APP_SHORTCUT_PATH)/syncplay.desktop

server:
	-mkdir -p $(BIN_PATH)
	touch $(BIN_PATH)/syncplay-server
	echo '#!/bin/sh\npython $(LIB_PATH)/syncplay/syncplayServer.py "$$@"' > $(BIN_PATH)/syncplay-server
	chmod a+x $(BIN_PATH)/syncplay-server
	cp syncplayServer.py $(LIB_PATH)/syncplay/
	cp resources/syncplay-server.desktop $(APP_SHORTCUT_PATH)/

u-server:
	-rm $(BIN_PATH)/syncplay-server
	-rm $(LIB_PATH)/syncplay/syncplayServer.py
	-rm $(APP_SHORTCUT_PATH)/syncplay-server.desktop

install-client: common client

uninstall-client: u-client u-common

install-server: common server

uninstall-server: u-server u-common

install-all: common client server

uninstall-all: u-client u-server u-common
