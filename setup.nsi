  !include LogicLib.nsh
  !include nsDialogs.nsh
  !define VERSION "1.2.5.0"
  !define SYNCPLAY "syncplay v1.2.5"
  
  LoadLanguageFile "${NSISDIR}\Contrib\Language files\English.nlf"
  LoadLanguageFile "${NSISDIR}\Contrib\Language files\Polish.nlf"
  
  Name "Syncplay"
  OutFile "Syncplay.exe"
  InstallDir $PROGRAMFILES\Syncplay
  RequestExecutionLevel admin
  XPStyle on
  Icon resources\icon.ico ;Change DIR
  SetCompressor /SOLID lzma
     
  VIProductVersion "${VERSION}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "Syncplay"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${VERSION}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "Syncplay"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "Syncplay"
  
  VIAddVersionKey /LANG=${LANG_POLISH} "ProductName" "Syncplay"
  VIAddVersionKey /LANG=${LANG_POLISH} "FileVersion" "${VERSION}"
  VIAddVersionKey /LANG=${LANG_POLISH} "LegalCopyright" "Syncplay"
  VIAddVersionKey /LANG=${LANG_POLISH} "FileDescription" "Syncplay"  
  
  PageEx license
    LicenseData resources\license.txt
  PageExEnd
  Page directory
  Page instFiles
     
  UninstPage uninstConfirm
  UninstPage instFiles
    
  !macro APP_ASSOCIATE EXT FileCLASS DESCRIPTION COMMANDTEXT COMMAND
    WriteRegStr HKCR ".${EXT}" "" "${FileCLASS}"
    WriteRegStr HKCR "${FileCLASS}" "" `${DESCRIPTION}`
    WriteRegStr HKCR "${FileCLASS}\shell" "" "open"
    WriteRegStr HKCR "${FileCLASS}\shell\open" "" `${COMMANDTEXT}`
    WriteRegStr HKCR "${FileCLASS}\shell\open\command" "" `${COMMAND}`
  !macroend
  
  !macro APP_UNASSOCIATE EXT FileCLASS
    ; Backup the previously associated File class
    ReadRegStr $R0 HKCR ".${EXT}" `${FileCLASS}_backup`
    WriteRegStr HKCR ".${EXT}" "" "$R0"
 
    DeleteRegKey HKCR `${FileCLASS}`
  !macroend
  
  ;Associates extensions with Syncplay
  Function Associate
    !insertmacro APP_ASSOCIATE "mkv" "Syncplay.mkv" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "mp4" "Syncplay.mp4" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "avi" "Syncplay.avi" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "flv" "Syncplay.flv" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "mpg" "Syncplay.mpg" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "rmvb" "Syncplay.rmvb" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "vob" "Syncplay.vob" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "swf" "Syncplay.swf" "$INSTDIR\Syncplay.exe,%1%" \
     "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
    !insertmacro APP_ASSOCIATE "wmv" "Syncplay.wmv" "$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
  FunctionEnd
  
  Function WriteRegistry
    WriteRegStr HKLM SOFTWARE\Syncplay "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayName" "Syncplay"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoRepair" 1
  FunctionEnd
     
   Function WriteFiles
    File "${SYNCPLAY}\Syncplay.exe"
    File "${SYNCPLAY}\syncplayClientForceConfiguration.bat"
    File "${SYNCPLAY}\syncplayServer.exe"
    File "${SYNCPLAY}\w9xpopen.exe"
    File "${SYNCPLAY}\python27.dll"
   FunctionEnd
   
   Function WriteFilesLib
    File "${SYNCPLAY}\lib\API-MS-Win-Core-Debug-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-DelayLoad-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-ErrorHandling-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-File-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-Handle-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-Heap-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-IO-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-Interlocked-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-LibraryLoader-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-LocalRegistry-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-Localization-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-Misc-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-ProcessEnvironment-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-ProcessThreads-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-ProFile-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-String-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-Synch-L1-1-0.dll"
    File "${SYNCPLAY}\lib\API-MS-Win-Core-SysInfo-L1-1-0.dll"
    File "${SYNCPLAY}\lib\DNSAPI.DLL"
    File "${SYNCPLAY}\lib\MSIMG32.DLL"
    File "${SYNCPLAY}\lib\NSI.dll"
    File "${SYNCPLAY}\lib\USP10.DLL"
    File "${SYNCPLAY}\lib\_ctypes.pyd"
    File "${SYNCPLAY}\lib\_hashlib.pyd"
    File "${SYNCPLAY}\lib\_socket.pyd"
    File "${SYNCPLAY}\lib\_win32sysloader.pyd"
    File "${SYNCPLAY}\lib\atk.pyd"
    File "${SYNCPLAY}\lib\bz2.pyd"
    File "${SYNCPLAY}\lib\cairo._cairo.pyd"
    File "${SYNCPLAY}\lib\freetype6.dll"
    File "${SYNCPLAY}\lib\gio._gio.pyd"
    File "${SYNCPLAY}\lib\glib._glib.pyd"
    File "${SYNCPLAY}\lib\gobject._gobject.pyd"
    File "${SYNCPLAY}\lib\gtk._gtk.pyd"
    File "${SYNCPLAY}\lib\intl.dll"
    File "${SYNCPLAY}\lib\libatk-1.0-0.dll"
    File "${SYNCPLAY}\lib\libcairo-2.dll"
    File "${SYNCPLAY}\lib\libexpat-1.dll"
    File "${SYNCPLAY}\lib\libfontconfig-1.dll"
    File "${SYNCPLAY}\lib\libgdk-win32-2.0-0.dll"
    File "${SYNCPLAY}\lib\libgdk_pixbuf-2.0-0.dll"
    File "${SYNCPLAY}\lib\libgio-2.0-0.dll"
    File "${SYNCPLAY}\lib\libglib-2.0-0.dll"
    File "${SYNCPLAY}\lib\libgmodule-2.0-0.dll"
    File "${SYNCPLAY}\lib\libgobject-2.0-0.dll"
    File "${SYNCPLAY}\lib\libgthread-2.0-0.dll"
    File "${SYNCPLAY}\lib\libgtk-win32-2.0-0.dll"
    File "${SYNCPLAY}\lib\libpango-1.0-0.dll"
    File "${SYNCPLAY}\lib\libpangocairo-1.0-0.dll"
    File "${SYNCPLAY}\lib\libpangoft2-1.0-0.dll"
    File "${SYNCPLAY}\lib\libpangowin32-1.0-0.dll"
    File "${SYNCPLAY}\lib\libpng14-14.dll"
    File "${SYNCPLAY}\lib\libsync"
    File "${SYNCPLAY}\lib\pango.pyd"
    File "${SYNCPLAY}\lib\pangocairo.pyd"
    File "${SYNCPLAY}\lib\pyexpat.pyd"
    File "${SYNCPLAY}\lib\pythoncom27.dll"
    File "${SYNCPLAY}\lib\pywintypes27.dll"
    File "${SYNCPLAY}\lib\select.pyd"
    File "${SYNCPLAY}\lib\twisted.python._initgroups.pyd"
    File "${SYNCPLAY}\lib\unicodedata.pyd"
    File "${SYNCPLAY}\lib\win32api.pyd"
    File "${SYNCPLAY}\lib\win32gui.pyd"
    File "${SYNCPLAY}\lib\zlib1.dll"
    File "${SYNCPLAY}\lib\zope.interface._zope_interface_coptimizations.pyd"
   FunctionEnd
    
  Function un.AssociateDel
    !insertmacro APP_UNASSOCIATE "mkv" "Syncplay.mkv"
    !insertmacro APP_UNASSOCIATE "mp4" "Syncplay.mp4"
    !insertmacro APP_UNASSOCIATE "avi" "Syncplay.avi"
    !insertmacro APP_UNASSOCIATE "flv" "Syncplay.flv"
    !insertmacro APP_UNASSOCIATE "mpg" "Syncplay.mpg"
    !insertmacro APP_UNASSOCIATE "rmvb" "Syncplay.rmvb"
    !insertmacro APP_UNASSOCIATE "vob" "Syncplay.vob"
    !insertmacro APP_UNASSOCIATE "swf" "Syncplay.swf"
    !insertmacro APP_UNASSOCIATE "wmv" "Syncplay.wmv"      
  FunctionEnd
  
  Function un.DeleteFiles
    Delete "$INSTDIR\Syncplay.exe"
    Delete "$INSTDIR\syncplayClientForceConfiguration.bat"
    Delete "$INSTDIR\syncplayServer.exe "
    Delete "$INSTDIR\w9xpopen.exe"
    Delete "$INSTDIR\python27.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Debug-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-DelayLoad-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-ErrorHandling-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Delete-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Handle-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Heap-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-IO-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Interlocked-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-LibraryLoader-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-LocalRegistry-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Localization-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Misc-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-ProcessEnvironment-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-ProcessThreads-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-ProDelete-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-String-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Synch-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-SysInfo-L1-1-0.dll"
    Delete "$INSTDIR\lib\DNSAPI.DLL"
    Delete "$INSTDIR\lib\MSIMG32.DLL"
    Delete "$INSTDIR\lib\NSI.dll"
    Delete "$INSTDIR\lib\USP10.DLL"
    Delete "$INSTDIR\lib\_ctypes.pyd"
    Delete "$INSTDIR\lib\_hashlib.pyd"
    Delete "$INSTDIR\lib\_socket.pyd"
    Delete "$INSTDIR\lib\_win32sysloader.pyd"
    Delete "$INSTDIR\lib\atk.pyd"
    Delete "$INSTDIR\lib\bz2.pyd"
    Delete "$INSTDIR\lib\cairo._cairo.pyd"
    Delete "$INSTDIR\lib\freetype6.dll"
    Delete "$INSTDIR\lib\gio._gio.pyd"
    Delete "$INSTDIR\lib\glib._glib.pyd"
    Delete "$INSTDIR\lib\gobject._gobject.pyd"
    Delete "$INSTDIR\lib\gtk._gtk.pyd"
    Delete "$INSTDIR\lib\intl.dll"
    Delete "$INSTDIR\lib\libatk-1.0-0.dll"
    Delete "$INSTDIR\lib\libcairo-2.dll"
    Delete "$INSTDIR\lib\libexpat-1.dll"
    Delete "$INSTDIR\lib\libfontconfig-1.dll"
    Delete "$INSTDIR\lib\libgdk-win32-2.0-0.dll"
    Delete "$INSTDIR\lib\libgdk_pixbuf-2.0-0.dll"
    Delete "$INSTDIR\lib\libgio-2.0-0.dll"
    Delete "$INSTDIR\lib\libglib-2.0-0.dll"
    Delete "$INSTDIR\lib\libgmodule-2.0-0.dll"
    Delete "$INSTDIR\lib\libgobject-2.0-0.dll"
    Delete "$INSTDIR\lib\libgthread-2.0-0.dll"
    Delete "$INSTDIR\lib\libgtk-win32-2.0-0.dll"
    Delete "$INSTDIR\lib\libpango-1.0-0.dll"
    Delete "$INSTDIR\lib\libpangocairo-1.0-0.dll"
    Delete "$INSTDIR\lib\libpangoft2-1.0-0.dll"
    Delete "$INSTDIR\lib\libpangowin32-1.0-0.dll"
    Delete "$INSTDIR\lib\libpng14-14.dll"
    Delete "$INSTDIR\lib\libsync"
    Delete "$INSTDIR\lib\pango.pyd"
    Delete "$INSTDIR\lib\pangocairo.pyd"
    Delete "$INSTDIR\lib\pyexpat.pyd"
    Delete "$INSTDIR\lib\pythoncom27.dll"
    Delete "$INSTDIR\lib\pywintypes27.dll"
    Delete "$INSTDIR\lib\select.pyd"
    Delete "$INSTDIR\lib\twisted.python._initgroups.pyd"
    Delete "$INSTDIR\lib\unicodedata.pyd"
    Delete "$INSTDIR\lib\win32api.pyd"
    Delete "$INSTDIR\lib\win32gui.pyd"
    Delete "$INSTDIR\lib\zlib1.dll"
    Delete "$INSTDIR\lib\zope.interface._zope_interface_coptimizations.pyd"
    Delete "$INSTDIR\lib\API-MS-Win-Core-File-L1-1-0.dll"
    Delete "$INSTDIR\lib\API-MS-Win-Core-Profile-L1-1-0.dll"
    RMDir "$INSTDIR\lib"
    RMDir "$INSTDIR\pyt"
  FunctionEnd
  
  ;Prevents from running more than one instance of installer
  Function .onInit
    System::Call 'kernel32::CreateMutexA(i 0, i 0, t "myMutex") i .r1 ?e'
    Pop $R0
    StrCmp $R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
      Abort
        Call Language
  FunctionEnd
     
    ;Language selection dialog
  Function Language
    Push ""
    Push ${LANG_ENGLISH}
    Push English
    Push ${LANG_POLISH}
    Push Polski
    Push A ; A means auto count languages
    LangDLL::LangDialog "Installer Language" "Please select the language of the installer"
    Pop $LANGUAGE
    StrCmp $LANGUAGE "cancel" 0 +2
      Abort
    FunctionEnd
     
  Section "Install"
    SetOverwrite on
    SetOutPath $INSTDIR
    WriteUninstaller uninstall.exe
    Call Associate
    Call WriteRegistry
    Call WriteFiles
    SetOutPath $INSTDIR\lib
    Call WriteFilesLib
  SectionEnd
     
  Section "Uninstall"
    Call un.AssociateDel
    Call un.DeleteFiles
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay"
    DeleteRegKey HKLM SOFTWARE\Syncplay
    Delete $INSTDIR\uninstall.exe
    RMDir $INSTDIR\lib
    RMDir $INSTDIR\pyt
    RMDir $INSTDIR
  SectionEnd