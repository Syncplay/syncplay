SINGLE_USER	= false

ifndef VLC_SUPPORT
	VLC_SUPPORT = true
endif

ifeq ($(shell uname)),FreeBSD)
	BSD          = true
endif
ifeq ($(shell uname)),NetBSD)
	BSD          = true
endif
ifeq ($(shell uname)),OpenBSD)
	BSD          = true
endif
ifeq ($(shell uname)),DragonFly)
	BSD          = true
endif

ifeq ($(SINGLE_USER),false)
ifneq ($(BSD),true)
	PREFIX      ?= /usr
	VLC_LIB_PATH = ${PREFIX}/lib
else
	PREFIX 	    ?= /usr/local
	VLC_LIB_PATH = ${PREFIX}/lib
endif
else
	PREFIX       = ${HOME}/.local
	VLC_LIB_PATH = ${HOME}/.local/share
endif

	BIN_PATH          = ${DESTDIR}${PREFIX}/bin
	LIB_PATH          = ${DESTDIR}${PREFIX}/lib
	APP_SHORTCUT_PATH = ${DESTDIR}${PREFIX}/share/applications
	SHARE_PATH        = ${DESTDIR}${PREFIX}/share

common:
	-mkdir -p $(LIB_PATH)/syncplay/resources/lua/intf
	-mkdir -p $(APP_SHORTCUT_PATH)
	-mkdir -p $(SHARE_PATH)/app-install/icons
	-mkdir -p $(SHARE_PATH)/pixmaps/
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
	cp syncplayClient.py $(BIN_PATH)/syncplay
	sed -i -e 's%# libpath%site.addsitedir\("${PREFIX}/lib/syncplay"\)%' $(BIN_PATH)/syncplay
	chmod 755 $(BIN_PATH)/syncplay
	cp syncplayClient.py $(LIB_PATH)/syncplay/
	cp resources/syncplay.desktop $(APP_SHORTCUT_PATH)/

ifeq ($(SINGLE_USER),false)
	chmod 755 $(APP_SHORTCUT_PATH)/syncplay.desktop
endif
	
ifeq ($(VLC_SUPPORT),true)
	-mkdir -p ${DESTDIR}$(VLC_LIB_PATH)/vlc/lua/intf/
	cp resources/lua/intf/syncplay.lua ${DESTDIR}$(VLC_LIB_PATH)/vlc/lua/intf/
endif

u-client:
	-rm $(BIN_PATH)/syncplay
	-rm $(LIB_PATH)/syncplay/syncplayClient.py
	-rm ${DESTDIR}$(VLC_LIB_PATH)/vlc/lua/intf/syncplay.lua
	-rm $(APP_SHORTCUT_PATH)/syncplay.desktop

server:
	-mkdir -p $(BIN_PATH)
	cp syncplayServer.py $(BIN_PATH)/syncplay-server
	sed -i -e 's%# libpath%site.addsitedir\("${PREFIX}/lib/syncplay"\)%' $(BIN_PATH)/syncplay-server
	chmod 755 $(BIN_PATH)/syncplay-server
	cp syncplayServer.py $(LIB_PATH)/syncplay/
	cp resources/syncplay-server.desktop $(APP_SHORTCUT_PATH)/

ifeq ($(SINGLE_USER),false)
	chmod 755 $(APP_SHORTCUT_PATH)/syncplay-server.desktop
endif

u-server:
	-rm $(BIN_PATH)/syncplay-server
	-rm $(LIB_PATH)/syncplay/syncplayServer.py
	-rm $(APP_SHORTCUT_PATH)/syncplay-server.desktop
	
warnings:
ifeq ($(SINGLE_USER),true)
	@echo -e "\n**********\n**********\n \nRemeber to add ${HOME}/.local/bin to your \$$PATH with 'echo \"export PATH=\$$PATH:${HOME}/.local/bin\" >> ${HOME}/.profile' \nThis will take effect after you logoff.\n \n**********\n**********\n"
endif

install-client: common client warnings

uninstall-client: u-client u-common 

install-server: common server warnings

uninstall-server: u-server u-common

install: common client server warnings 

uninstall: u-client u-server u-common
