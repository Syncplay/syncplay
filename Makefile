SINGLE_USER	= false

ifndef VLC_SUPPORT
	VLC_SUPPORT = false
endif

BASE_PATH	= /usr
LOCAL_PATH	= ~/.local

ifeq ($(SINGLE_USER),false)
	BIN_PATH          = $(BASE_PATH)/bin
	LIB_PATH          = $(BASE_PATH)/lib
	APP_SHORTCUT_PATH = $(BASE_PATH)/share/applications
	SHARE_PATH        = $(BASE_PATH)/share
else
	BIN_PATH          = $(LOCAL_PATH)/syncplay
	LIB_PATH          = $(LOCAL_PATH)/syncplay
	APP_SHORTCUT_PATH = $(LOCAL_PATH)/share/applications
	SHARE_PATH        = $(LOCAL_PATH)/share
endif

common:
	-mkdir -p $(LIB_PATH)/syncplay/resources/
	-mkdir -p $(LIB_PATH)/syncplay/resources/lua
	-mkdir -p $(LIB_PATH)/syncplay/resources/lua/intf
	cp -r syncplay $(LIB_PATH)/syncplay/
	chmod 755 $(LIB_PATH)/syncplay/
	cp -r resources/hicolor $(SHARE_PATH)/icons/
	cp -r resources/*.png $(LIB_PATH)/syncplay/resources/
	cp -r resources/lua/intf/*.lua $(LIB_PATH)/syncplay/resources/lua/intf/
	cp resources/hicolor/48x48/apps/syncplay.png $(SHARE_PATH)/app-install/icons/
	cp resources/hicolor/48x48/apps/syncplay.png $(SHARE_PATH)/pixmaps/

u-common:
	-rm -rf $(LIB_PATH)/syncplay
	-rm $(SHARE_PATH)/icons/hicolor/*/apps/syncplay.png
	-rm $(SHARE_PATH)/app-install/icons/syncplay.png
	-rm $(SHARE_PATH)/pixmaps/syncplay.png

client:
	-mkdir -p $(BIN_PATH)
	touch $(BIN_PATH)/syncplay
	chmod 755 $(BIN_PATH)/syncplay
	cp syncplayClient.py $(LIB_PATH)/syncplay/
	cp resources/syncplay.desktop $(APP_SHORTCUT_PATH)/
	
ifeq ($(VLC_SUPPORT),true)
	-mkdir -p $(LIB_PATH)/vlc/lua/intf/
	cp resources/lua/intf/syncplay.lua $(LIB_PATH)/vlc/lua/intf/
endif

u-client:
	-rm $(BIN_PATH)/syncplay
	-rm $(LIB_PATH)/syncplay/syncplayClient.py
	-rm $(LIB_PATH)/vlc/lua/intf/syncplay.lua
	-rm $(APP_SHORTCUT_PATH)/syncplay.desktop

server:
	-mkdir -p $(BIN_PATH)
	touch $(BIN_PATH)/syncplay-server
	chmod 755 $(BIN_PATH)/syncplay-server
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

install: common client server

uninstall: u-client u-server u-common
