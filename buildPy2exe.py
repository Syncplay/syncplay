#!/usr/bin/env python
#coding:utf8

''' *** TROUBLESHOOTING ***

) If you get the error "ImportError: No module named zope.interface" then add an empty __init__.py file to the PYTHONDIR/Lib/site-packages/zope directory

2) It is expected that you will have NSIS 3  NSIS from http://nsis.sourceforge.net installed to: C:\Program Files (x86)\NSIS\

'''

import sys, codecs
try:
    if (sys.version_info.major != 2) or (sys.version_info.minor < 7):
        raise Exception("You must build Syncplay with Python 2.7!")
except AttributeError:
    import warnings
    warnings.warn("You must build Syncplay with Python 2.7!")

from distutils.core import setup
from py2exe.build_exe import py2exe
from string import Template

import syncplay
import os
import subprocess

from syncplay.messages import getMissingStrings
missingStrings = getMissingStrings()
if missingStrings is not None and missingStrings is not "":
    import warnings
    warnings.warn("MISSING/UNUSED STRINGS DETECTED:\n{}".format(missingStrings))

p = "C:\\Program Files (x86)\\NSIS\\makensis.exe" #TODO: how to move that into proper place, huh
NSIS_COMPILE = p if os.path.isfile(p) else "makensis.exe"
OUT_DIR = "syncplay v{}".format(syncplay.version)
SETUP_SCRIPT_PATH = "syncplay_setup.nsi"
NSIS_SCRIPT_TEMPLATE = r"""
  !include LogicLib.nsh
  !include nsDialogs.nsh
  !include FileFunc.nsh

  LoadLanguageFile "$${NSISDIR}\Contrib\Language files\English.nlf"
  LoadLanguageFile "$${NSISDIR}\Contrib\Language files\Polish.nlf"
  LoadLanguageFile "$${NSISDIR}\Contrib\Language files\Russian.nlf"
  LoadLanguageFile "$${NSISDIR}\Contrib\Language files\German.nlf"

  Unicode true

  Name "Syncplay $version"
  OutFile "Syncplay $version Setup.exe"
  InstallDir $$PROGRAMFILES\Syncplay
  RequestExecutionLevel admin
  XPStyle on
  Icon resources\icon.ico ;Change DIR
  SetCompressor /SOLID lzma

  VIProductVersion "$version.0"
  VIAddVersionKey /LANG=$${LANG_ENGLISH} "ProductName" "Syncplay"
  VIAddVersionKey /LANG=$${LANG_ENGLISH} "FileVersion" "$version.0"
  VIAddVersionKey /LANG=$${LANG_ENGLISH} "LegalCopyright" "Syncplay"
  VIAddVersionKey /LANG=$${LANG_ENGLISH} "FileDescription" "Syncplay"

  VIAddVersionKey /LANG=$${LANG_POLISH} "ProductName" "Syncplay"
  VIAddVersionKey /LANG=$${LANG_POLISH} "FileVersion" "$version.0"
  VIAddVersionKey /LANG=$${LANG_POLISH} "LegalCopyright" "Syncplay"
  VIAddVersionKey /LANG=$${LANG_POLISH} "FileDescription" "Syncplay"

  VIAddVersionKey /LANG=$${LANG_RUSSIAN} "ProductName" "Syncplay"
  VIAddVersionKey /LANG=$${LANG_RUSSIAN} "FileVersion" "$version.0"
  VIAddVersionKey /LANG=$${LANG_RUSSIAN} "LegalCopyright" "Syncplay"
  VIAddVersionKey /LANG=$${LANG_RUSSIAN} "FileDescription" "Syncplay"

  LangString ^SyncplayLanguage $${LANG_ENGLISH} "en"
  LangString ^Associate $${LANG_ENGLISH} "Associate Syncplay with multimedia files."
  LangString ^VLC $${LANG_ENGLISH} "Install Syncplay interface for VLC 2 and above"
  LangString ^BrowseVLCBtn $${LANG_ENGLISH} "Select VLC folder"
  LangString ^Shortcut $${LANG_ENGLISH} "Create Shortcuts in following locations:"
  LangString ^StartMenu $${LANG_ENGLISH} "Start Menu"
  LangString ^Desktop $${LANG_ENGLISH} "Desktop"
  LangString ^QuickLaunchBar $${LANG_ENGLISH} "Quick Launch Bar"
  LangString ^AutomaticUpdates $${LANG_ENGLISH} "Check for updates automatically"
  LangString ^UninstConfig $${LANG_ENGLISH} "Delete configuration file."

  LangString ^SyncplayLanguage $${LANG_POLISH} "pl"
  LangString ^Associate $${LANG_POLISH} "Skojarz Syncplaya z multimediami"
  LangString ^VLC $${LANG_POLISH} "Zainstaluj interface Syncplaya dla VLC 2+"
  LangString ^BrowseVLCBtn $${LANG_POLISH} "Określ folder VLC"
  LangString ^Shortcut $${LANG_POLISH} "Utworz skroty w nastepujacych miejscach:"
  LangString ^StartMenu $${LANG_POLISH} "Menu Start"
  LangString ^Desktop $${LANG_POLISH} "Pulpit"
  LangString ^QuickLaunchBar $${LANG_POLISH} "Pasek szybkiego uruchamiania"
  LangString ^UninstConfig $${LANG_POLISH} "Usun plik konfiguracyjny."

  LangString ^SyncplayLanguage $${LANG_RUSSIAN} "ru"
  LangString ^Associate $${LANG_RUSSIAN} "Ассоциировать Syncplay с видеофайлами"
  LangString ^VLC $${LANG_RUSSIAN} "Установить интерфейс Syncplay для VLC 2+"
  LangString ^BrowseVLCBtn $${LANG_RUSSIAN} "Укажите папку VLC"
  LangString ^Shortcut $${LANG_RUSSIAN} "Создать ярлыки:"
  LangString ^StartMenu $${LANG_RUSSIAN} "в меню Пуск"
  LangString ^Desktop $${LANG_RUSSIAN} "на рабочем столе"
  LangString ^QuickLaunchBar $${LANG_RUSSIAN} "в меню быстрого запуска"
  LangString ^AutomaticUpdates $${LANG_RUSSIAN} "Проверять обновления автоматически"; TODO: Confirm Russian translation ("Check for updates automatically")
  LangString ^UninstConfig $${LANG_RUSSIAN} "Удалить файл настроек."

  LangString ^SyncplayLanguage $${LANG_GERMAN} "de"
  LangString ^Associate $${LANG_GERMAN} "Syncplay als Standardprogramm für Multimedia-Dateien verwenden."
  LangString ^VLC $${LANG_GERMAN} "Syncplay-Interface für VLC installieren (ab VLC 2+)"
  LangString ^Shortcut $${LANG_GERMAN} "Erstelle Verknüpfungen an folgenden Orten:"
  LangString ^BrowseVLCBtn $${LANG_GERMAN} "VLC-Ordner wählen"
  LangString ^StartMenu $${LANG_GERMAN} "Startmenü"
  LangString ^Desktop $${LANG_GERMAN} "Desktop"
  LangString ^QuickLaunchBar $${LANG_GERMAN} "Schnellstartleiste"
  LangString ^AutomaticUpdates $${LANG_GERMAN} "Automatisch nach Updates suchen";
  LangString ^UninstConfig $${LANG_GERMAN} "Konfigurationsdatei löschen."

  ; Remove text to save space
  LangString ^ClickInstall $${LANG_GERMAN} " "

  PageEx license
    LicenseData resources\license.rtf
  PageExEnd
  Page custom DirectoryCustom DirectoryCustomLeave
  Page instFiles

  UninstPage custom un.installConfirm un.installConfirmLeave
  UninstPage instFiles

  Var Dialog
  Var Icon_Syncplay
  Var Icon_Syncplay_Handle
  ;Var CheckBox_Associate
  Var CheckBox_VLC
  Var CheckBox_AutomaticUpdates
  Var CheckBox_StartMenuShortcut
  Var CheckBox_DesktopShortcut
  Var CheckBox_QuickLaunchShortcut
  ;Var CheckBox_Associate_State
  Var CheckBox_VLC_State
  Var CheckBox_AutomaticUpdates_State
  Var CheckBox_StartMenuShortcut_State
  Var CheckBox_DesktopShortcut_State
  Var CheckBox_QuickLaunchShortcut_State
  Var Button_Browse
  Var Button_Browse_VLC
  Var Directory
  Var GroupBox_DirSub
  Var Label_Text
  Var Label_Shortcut
  Var Label_Size
  Var Label_Space
  Var Text_Directory

  Var Uninst_Dialog
  Var Uninst_Icon
  Var Uninst_Icon_Handle
  Var Uninst_Label_Directory
  Var Uninst_Label_Text
  Var Uninst_Text_Directory
  Var Uninst_CheckBox_Config
  Var Uninst_CheckBox_Config_State

  Var Size
  Var SizeHex
  Var AvailibleSpace
  Var AvailibleSpaceGiB
  Var Drive
  Var VLC_Directory

  ;!macro APP_ASSOCIATE EXT FileCLASS DESCRIPTION COMMANDTEXT COMMAND
  ;  WriteRegStr HKCR ".$${EXT}" "" "$${FileCLASS}"
  ;  WriteRegStr HKCR "$${FileCLASS}" "" `$${DESCRIPTION}`
  ;  WriteRegStr HKCR "$${FileCLASS}\shell" "" "open"
  ;  WriteRegStr HKCR "$${FileCLASS}\shell\open" "" `$${COMMANDTEXT}`
  ;  WriteRegStr HKCR "$${FileCLASS}\shell\open\command" "" `$${COMMAND}`
  ;!macroend

  !macro APP_UNASSOCIATE EXT FileCLASS
    ; Backup the previously associated File class
    ReadRegStr $$R0 HKCR ".$${EXT}" `$${FileCLASS}_backup`
    WriteRegStr HKCR ".$${EXT}" "" "$$R0"
    DeleteRegKey HKCR `$${FileCLASS}`
  !macroend

  ;!macro ASSOCIATE EXT
  ;  !insertmacro APP_ASSOCIATE "$${EXT}" "Syncplay.$${EXT}" "$$INSTDIR\Syncplay.exe,%1%" \
  ;  "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
  ;!macroend

  !macro UNASSOCIATE EXT
    !insertmacro APP_UNASSOCIATE "$${EXT}" "Syncplay.$${EXT}"
  !macroend

  ;Prevents from running more than one instance of installer and sets default state of checkboxes
  Function .onInit
    System::Call 'kernel32::CreateMutexA(i 0, i 0, t "SyncplayMutex") i .r1 ?e'
    Pop $$R0
    StrCmp $$R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
      Abort

    ;StrCpy $$CheckBox_Associate_State $${BST_CHECKED}
    StrCpy $$CheckBox_StartMenuShortcut_State $${BST_CHECKED}
    Call GetVLCDir
    Call UpdateVLCCheckbox

    Call GetSize
    Call DriveSpace
    Call Language
  FunctionEnd

  ;Language selection dialog
  Function Language
    Push ""
    Push $${LANG_ENGLISH}
    Push English
    Push $${LANG_POLISH}
    Push Polski
	Push $${LANG_RUSSIAN}
    Push Русский
    Push $${LANG_GERMAN}
    Push Deutsch
    Push A ; A means auto count languages
    LangDLL::LangDialog "Language Selection" "Please select the language of Syncplay and the installer"
    Pop $$LANGUAGE
    StrCmp $$LANGUAGE "cancel" 0 +2
      Abort
  FunctionEnd

  Function DirectoryCustom

    nsDialogs::Create 1018
    Pop $$Dialog

    GetFunctionAddress $$R8 DirectoryCustomLeave
    nsDialogs::OnBack $$R8

    $${NSD_CreateIcon} 0u 0u 22u 20u ""
    Pop $$Icon_Syncplay
    $${NSD_SetIconFromInstaller} $$Icon_Syncplay $$Icon_Syncplay_Handle

    $${NSD_CreateLabel} 25u 0u 241u 34u "$$(^DirText)"
    Pop $$Label_Text

    $${NSD_CreateText} 8u 38u 187u 12u "$$INSTDIR"
    Pop $$Text_Directory
    $${NSD_SetFocus} $$Text_Directory

    $${NSD_CreateBrowseButton} 202u 37u 55u 14u "$$(^BrowseBtn)"
    Pop $$Button_Browse
    $${NSD_OnClick} $$Button_Browse DirectoryBrowseDialog

    $${NSD_CreateGroupBox} 1u 27u 264u 30u "$$(^DirSubText)"
    Pop $$GroupBox_DirSub

    $${NSD_CreateLabel} 0u 122u 132 8u "$$(^SpaceRequired)$$SizeMB"
    Pop $$Label_Size

    $${NSD_CreateLabel} 321u 122u 132 8u "$$(^SpaceAvailable)$$AvailibleSpaceGiB.$$AvailibleSpaceGB"
    Pop $$Label_Space

    ;$${NSD_CreateCheckBox} 8u 59u 187u 10u "$$(^Associate)"
    ;Pop $$CheckBox_Associate

    $${NSD_CreateBrowseButton} 185u 70u 70u 14u "$$(^BrowseVLCBtn)"
    Pop $$Button_Browse_VLC
    $${NSD_OnClick} $$Button_Browse_VLC DirectoryBrowseDialogVLC

    $${NSD_CreateCheckBox} 8u 72u 250u 10u "$$(^VLC)"
    Pop $$CheckBox_VLC

    $${NSD_CreateCheckBox} 8u 85u 250u 10u "$$(^AutomaticUpdates)"
    Pop $$CheckBox_AutomaticUpdates
    $${NSD_Check} $$CheckBox_AutomaticUpdates

    $${NSD_CreateLabel} 8u 98u 187u 10u "$$(^Shortcut)"
    Pop $$Label_Shortcut

    $${NSD_CreateCheckbox} 8u 111u 60u 10u "$$(^StartMenu)"
    Pop $$CheckBox_StartMenuShortcut

    $${NSD_CreateCheckbox} 78u 111u 70u 10u "$$(^Desktop)"
    Pop $$CheckBox_DesktopShortcut

    $${NSD_CreateCheckbox} 158u 111u 130u 10u "$$(^QuickLaunchBar)"
    Pop $$CheckBox_QuickLaunchShortcut

    ;$${If} $$CheckBox_Associate_State == $${BST_CHECKED}
    ;  $${NSD_Check} $$CheckBox_Associate
    ;$${EndIf}

    $${If} $$CheckBox_VLC_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_VLC
    $${EndIf}

    Call UpdateVLCCheckbox

    $${If} $$CheckBox_StartMenuShortcut_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_StartMenuShortcut
    $${EndIf}

    $${If} $$CheckBox_DesktopShortcut_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_DesktopShortcut
    $${EndIf}

    $${If} $$CheckBox_QuickLaunchShortcut_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_QuickLaunchShortcut
    $${EndIf}

    $${If} $$CheckBox_AutomaticUpdates_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_AutomaticUpdates
    $${EndIf}

    nsDialogs::Show

    $${NSD_FreeIcon} $$Icon_Syncplay_Handle

  FunctionEnd

  Function DirectoryCustomLeave
    $${NSD_GetText} $$Text_Directory $$INSTDIR
    ;$${NSD_GetState} $$CheckBox_Associate $$CheckBox_Associate_State
    $${NSD_GetState} $$CheckBox_VLC $$CheckBox_VLC_State
    $${NSD_GetState} $$CheckBox_AutomaticUpdates $$CheckBox_AutomaticUpdates_State
    $${NSD_GetState} $$CheckBox_StartMenuShortcut $$CheckBox_StartMenuShortcut_State
    $${NSD_GetState} $$CheckBox_DesktopShortcut $$CheckBox_DesktopShortcut_State
    $${NSD_GetState} $$CheckBox_QuickLaunchShortcut $$CheckBox_QuickLaunchShortcut_State
  FunctionEnd

  Function DirectoryBrowseDialog
    nsDialogs::SelectFolderDialog $$(^DirBrowseText)
    Pop $$Directory
    $${If} $$Directory != error
    StrCpy $$INSTDIR $$Directory
    $${NSD_SetText} $$Text_Directory $$INSTDIR
    Call DriveSpace
    $${NSD_SetText} $$Label_Space "$$(^SpaceAvailable)$$AvailibleSpaceGiB.$$AvailibleSpaceGB"
    $${EndIf}
    Abort
  FunctionEnd

  Function GetVLCDir
    IfFileExists "$$VLC_Directory\vlc.exe" VLCFound 0
    ReadRegStr $$VLC_Directory HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "VLCInstallLocation"
    IfFileExists "$$VLC_Directory\vlc.exe" VLCFound 0
    ReadRegStr $$VLC_Directory HKLM "Software\VideoLAN\VLC" "InstallDir"
    IfFileExists "$$VLC_Directory\vlc.exe" VLCFound 0
    StrCpy $$VLC_Directory "c:\program files (x86)\videolan\vlc"
    IfFileExists "$$VLC_Directory\vlc.exe" VLCFound 0
    StrCpy $$VLC_Directory "c:\program files\videolan\vlc"
    IfFileExists "$$VLC_Directory\vlc.exe" VLCFound 0
    StrCpy $$VLC_Directory ""
    VLCFound:
  FunctionEnd

  Function UpdateVLCCheckbox
    IfFileExists "$$VLC_Directory\vlc.exe" VLC_Enabled VLC_Disabled

    VLC_Enabled:
    EnableWindow $$CheckBox_VLC 1
    StrCpy $$CheckBox_VLC_State $${BST_CHECKED}
    $${NSD_SetState} $$CheckBox_VLC $$CheckBox_VLC_State
    goto CheckboxUpdated

    VLC_Disabled:
    EnableWindow $$CheckBox_VLC 0
    StrCpy $$CheckBox_VLC_State $${BST_UNCHECKED}
    $${NSD_SetState} $$CheckBox_VLC $$CheckBox_VLC_State

    CheckboxUpdated:
  FunctionEnd

  Function DirectoryBrowseDialogVLC
    nsDialogs::SelectFolderDialog $$(^BrowseVLCBtn) $$VLC_Directory
    Pop $$Directory
    $${If} $$Directory != error
    StrCpy $$VLC_Directory $$Directory
    Call UpdateVLCCheckbox
    $${EndIf}
    Abort
  FunctionEnd

  Function GetSize
    StrCpy $$Size "$totalSize"
    IntOp $$Size $$Size / 1024
    IntFmt $$SizeHex "0x%08X" $$Size
    IntOp $$Size $$Size / 1024
  FunctionEnd

  ;Calculates Free Space on HDD
  Function DriveSpace
    StrCpy $$Drive $$INSTDIR 1
    $${DriveSpace} "$$Drive:\" "/D=F /S=M" $$AvailibleSpace
    IntOp $$AvailibleSpaceGiB $$AvailibleSpace / 1024
    IntOp $$AvailibleSpace $$AvailibleSpace % 1024
    IntOp $$AvailibleSpace $$AvailibleSpace / 102
  FunctionEnd

  Function InstallOptions
    ;$${If} $$CheckBox_Associate_State == $${BST_CHECKED}
    ;  Call Associate
    ;  DetailPrint "Associated Syncplay with multimedia files"
    ;$${EndIf}

    $${If} $$CheckBox_StartMenuShortcut_State == $${BST_CHECKED}
      CreateDirectory $$SMPROGRAMS\Syncplay
      CreateShortCut "$$SMPROGRAMS\Syncplay\Syncplay.lnk" "$$INSTDIR\Syncplay.exe" ""
      CreateShortCut "$$SMPROGRAMS\Syncplay\Syncplay Server.lnk" "$$INSTDIR\syncplayServer.exe" ""
      CreateShortCut "$$SMPROGRAMS\Syncplay\Uninstall.lnk" "$$INSTDIR\Uninstall.exe" ""
      WriteINIStr "$$SMPROGRAMS\Syncplay\SyncplayWebsite.url" "InternetShortcut" "URL" "http://syncplay.pl"
    $${EndIf}

    $${If} $$CheckBox_DesktopShortcut_State == $${BST_CHECKED}
      CreateShortCut "$$DESKTOP\Syncplay.lnk" "$$INSTDIR\Syncplay.exe" ""
    $${EndIf}

    $${If} $$CheckBox_QuickLaunchShortcut_State == $${BST_CHECKED}
      CreateShortCut "$$QUICKLAUNCH\Syncplay.lnk" "$$INSTDIR\Syncplay.exe" ""
    $${EndIf}

    $${If} $$CheckBox_VLC_State == $${BST_CHECKED}
    IfFileExists "$$VLC_Directory\vlc.exe" 0 EndOfVLC
      SetOutPath $$VLC_Directory\lua\intf
      File resources\lua\intf\syncplay.lua
      EndOfVLC:
    $${EndIf}
  FunctionEnd

  ;Associates extensions with Syncplay
  ;Function Associate
  ;  !insertmacro ASSOCIATE avi
  ;  !insertmacro ASSOCIATE mpg
  ;  !insertmacro ASSOCIATE mpeg
  ;  !insertmacro ASSOCIATE mpe
  ;  !insertmacro ASSOCIATE m1v
  ;  !insertmacro ASSOCIATE m2v
  ;  !insertmacro ASSOCIATE mpv2
  ;  !insertmacro ASSOCIATE mp2v
  ;  !insertmacro ASSOCIATE mkv
  ;  !insertmacro ASSOCIATE mp4
  ;  !insertmacro ASSOCIATE m4v
  ;  !insertmacro ASSOCIATE mp4v
  ;  !insertmacro ASSOCIATE 3gp
  ;  !insertmacro ASSOCIATE 3gpp
  ;  !insertmacro ASSOCIATE 3g2
  ;  !insertmacro ASSOCIATE 3pg2
  ;  !insertmacro ASSOCIATE flv
  ;  !insertmacro ASSOCIATE f4v
  ;  !insertmacro ASSOCIATE rm
  ;  !insertmacro ASSOCIATE wmv
  ;  !insertmacro ASSOCIATE swf
  ;  !insertmacro ASSOCIATE rmvb
  ;  !insertmacro ASSOCIATE divx
  ;  !insertmacro ASSOCIATE amv
  ;FunctionEnd

  Function WriteRegistry
    Call GetSize
    WriteRegStr HKLM SOFTWARE\Syncplay "Install_Dir" "$$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayName" "Syncplay"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "InstallLocation" "$$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "VLCInstallLocation" "$$VLC_Directory"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "UninstallString" '"$$INSTDIR\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayIcon" "$$INSTDIR\resources\icon.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "Publisher" "Syncplay"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayVersion" "$version"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "URLInfoAbout" "http://syncplay.pl/"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoRepair" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "EstimatedSize" "$$SizeHex"
    WriteINIStr $$APPDATA\syncplay.ini general language $$(^SyncplayLanguage)
    $${If} $$CheckBox_AutomaticUpdates_State == $${BST_CHECKED}
        WriteINIStr $$APPDATA\syncplay.ini general CheckForUpdatesAutomatically "True"
    $${Else}
        WriteINIStr $$APPDATA\syncplay.ini general CheckForUpdatesAutomatically "False"
    $${EndIf}
  FunctionEnd

  Function un.installConfirm
    nsDialogs::Create 1018
    Pop $$Uninst_Dialog

    $${NSD_CreateIcon} 0u 1u 22u 20u ""
    Pop $$Uninst_Icon
    $${NSD_SetIconFromInstaller} $$Uninst_Icon $$Uninst_Icon_Handle

    $${NSD_CreateLabel} 0u 45u 55u 8u "$$(^UninstallingSubText)"
    Pop $$Uninst_Label_Directory

    $${NSD_CreateLabel} 25u 0u 241u 34u "$$(^UninstallingText)"
    Pop $$Uninst_Label_Text

    ReadRegStr $$INSTDIR HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "InstallLocation"
    $${NSD_CreateText} 56u 43u 209u 12u "$$INSTDIR"
    Pop $$Uninst_Text_Directory
    EnableWindow $$Uninst_Text_Directory 0

    $${NSD_CreateCheckBox} 0u 60u 250u 10u "$$(^UninstConfig)"
    Pop $$Uninst_CheckBox_Config


    nsDialogs::Show
    $${NSD_FreeIcon} $$Uninst_Icon_Handle
  FunctionEnd

  Function un.installConfirmLeave
    $${NSD_GetState} $$Uninst_CheckBox_Config $$Uninst_CheckBox_Config_State
  FunctionEnd

  Function un.AssociateDel
    !insertmacro UNASSOCIATE avi
    !insertmacro UNASSOCIATE mpg
    !insertmacro UNASSOCIATE mpeg
    !insertmacro UNASSOCIATE mpe
    !insertmacro UNASSOCIATE m1v
    !insertmacro UNASSOCIATE m2v
    !insertmacro UNASSOCIATE mpv2
    !insertmacro UNASSOCIATE mp2v
    !insertmacro UNASSOCIATE mkv
    !insertmacro UNASSOCIATE mp4
    !insertmacro UNASSOCIATE m4v
    !insertmacro UNASSOCIATE mp4v
    !insertmacro UNASSOCIATE 3gp
    !insertmacro UNASSOCIATE 3gpp
    !insertmacro UNASSOCIATE 3g2
    !insertmacro UNASSOCIATE 3pg2
    !insertmacro UNASSOCIATE flv
    !insertmacro UNASSOCIATE f4v
    !insertmacro UNASSOCIATE rm
    !insertmacro UNASSOCIATE wmv
    !insertmacro UNASSOCIATE swf
    !insertmacro UNASSOCIATE rmvb
    !insertmacro UNASSOCIATE divx
    !insertmacro UNASSOCIATE amv
  FunctionEnd

  Function un.InstallOptions
    Delete $$SMPROGRAMS\Syncplay\Syncplay.lnk
    Delete "$$SMPROGRAMS\Syncplay\Syncplay Server.lnk"
    Delete $$SMPROGRAMS\Syncplay\Uninstall.lnk
    Delete $$SMPROGRAMS\Syncplay\SyncplayWebsite.url
    RMDir $$SMPROGRAMS\Syncplay
    Delete $$DESKTOP\Syncplay.lnk
    Delete $$QUICKLAUNCH\Syncplay.lnk
    ReadRegStr $$VLC_Directory HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "VLCInstallLocation"
    IfFileExists "$$VLC_Directory\lua\intf\syncplay.lua" 0 +2
    Delete $$VLC_Directory\lua\intf\syncplay.lua
  FunctionEnd

  Section "Install"
    SetOverwrite on
    SetOutPath $$INSTDIR
    WriteUninstaller uninstall.exe

    $installFiles

    Call InstallOptions
    Call WriteRegistry
  SectionEnd

  Section "Uninstall"
    Call un.AssociateDel
    Call un.InstallOptions
    $uninstallFiles
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay"
    DeleteRegKey HKLM SOFTWARE\Syncplay
    Delete $$INSTDIR\uninstall.exe
    RMDir $$INSTDIR\Syncplay\\resources\lua\intf
    RMDir $$INSTDIR\Syncplay\\resources\lua
    RMDir $$INSTDIR\Syncplay\\resources
    RMDir $$INSTDIR\resources
    RMDir $$INSTDIR\lib
    RMDir $$INSTDIR

    $${If} $$Uninst_CheckBox_Config_State == $${BST_CHECKED}
      IfFileExists "$$APPDATA\.syncplay" 0 +2
      Delete $$APPDATA\.syncplay
      IfFileExists "$$APPDATA\syncplay.ini" 0 +2
      Delete $$APPDATA\syncplay.ini
    $${EndIf}
  SectionEnd
"""

class NSISScript(object):
    def create(self):
        fileList, totalSize = self.getBuildDirContents(OUT_DIR)
        print "Total size eq: {}".format(totalSize)
        installFiles = self.prepareInstallListTemplate(fileList) 
        uninstallFiles = self.prepareDeleteListTemplate(fileList)
        
        if os.path.isfile(SETUP_SCRIPT_PATH):
            raise RuntimeError("Cannot create setup script, file exists at {}".format(SETUP_SCRIPT_PATH))
        contents =  Template(NSIS_SCRIPT_TEMPLATE).substitute(
                                                              version = syncplay.version,
                                                              uninstallFiles = uninstallFiles,
                                                              installFiles = installFiles,
                                                              totalSize = totalSize,
                                                              )
        with codecs.open(SETUP_SCRIPT_PATH, "w", "utf-8-sig") as outfile:
            outfile.write(contents.decode('utf-8'))
        
    def compile(self):
        if not os.path.isfile(NSIS_COMPILE):
            return "makensis.exe not found, won't create the installer"
        subproc = subprocess.Popen([NSIS_COMPILE, SETUP_SCRIPT_PATH], env=os.environ)
        subproc.communicate()
        retcode = subproc.returncode
        os.remove(SETUP_SCRIPT_PATH)
        if retcode:
            raise RuntimeError("NSIS compilation return code: %d" % retcode)
   
    def getBuildDirContents(self, path):
        fileList = {}
        totalSize = 0
        for root, _, files in os.walk(path):
            totalSize += sum(os.path.getsize(os.path.join(root, file_)) for file_ in files)
            for file_ in files:
                new_root = root.replace(OUT_DIR, "").strip("\\")
                if not fileList.has_key(new_root):
                    fileList[new_root] = []
                fileList[new_root].append(file_)
        return fileList, totalSize          
    
    def prepareInstallListTemplate(self, fileList):
        create = []
        for dir_ in fileList.iterkeys():
            create.append('SetOutPath "$INSTDIR\\{}"'.format(dir_))
            for file_ in fileList[dir_]:
                create.append('FILE "{}\\{}\\{}"'.format(OUT_DIR, dir_, file_))
        return "\n".join(create)
    
    def prepareDeleteListTemplate(self, fileList):
        delete = []
        for dir_ in fileList.iterkeys():
            for file_ in fileList[dir_]:
                delete.append('DELETE "$INSTDIR\\{}\\{}"'.format(dir_, file_))
            delete.append('RMdir "$INSTDIR\\{}"'.format(file_))    
        return "\n".join(delete)
    
class build_installer(py2exe):
    def run(self):
        py2exe.run(self)
        script = NSISScript()
        script.create()
        print "*** compiling the NSIS setup script***"
        script.compile()
        print "*** DONE ***"

guiIcons = ['resources/accept.png', 'resources/arrow_undo.png', 'resources/clock_go.png',
     'resources/control_pause_blue.png', 'resources/cross.png', 'resources/door_in.png',
     'resources/folder_explore.png', 'resources/help.png', 'resources/table_refresh.png',
     'resources/timeline_marker.png','resources/control_play_blue.png',
     'resources/mpc-hc.png','resources/mpc-hc64.png','resources/mplayer.png',
     'resources/mpv.png','resources/vlc.png', 'resources/house.png', 'resources/film_link.png',
     'resources/eye.png', 'resources/comments.png', 'resources/cog_delete.png', 'resources/chevrons_right.png',
     'resources/user_key.png', 'resources/lock.png', 'resources/key_go.png', 'resources/page_white_key.png',
     'resources/tick.png', 'resources/lock_open.png', 'resources/empty_checkbox.png', 'resources/tick_checkbox.png',
     'resources/world_explore.png', 'resources/application_get.png', 'resources/cog.png', 'resources/arrow_switch.png',
     'resources/film_go.png', 'resources/world_go.png', 'resources/arrow_refresh.png', 'resources/bullet_right_grey.png',
     'resources/film_folder_edit.png',
     'resources/film_edit.png',
     'resources/folder_film.png',
     'resources/shield_edit.png',
     'resources/shield_add.png',
     'resources/email_go.png',
     'resources/world_add.png', 'resources/film_add.png', 'resources/delete.png', 'resources/spinner.mng'
    ]
resources = ["resources/icon.ico", "resources/syncplay.png", "resources/license.rtf", "resources/third-party-notices.rtf"]
resources.extend(guiIcons)
intf_resources = ["resources/lua/intf/syncplay.lua"]

common_info = dict(
    name='Syncplay',
    version=syncplay.version,
    author='Uriziel',
    author_email='dev@syncplay.pl',
    description='Syncplay',
)
    
info = dict(
    common_info,
    windows=[{"script":"syncplayClient.py", "icon_resources":[(1, "resources\\icon.ico")], 'dest_base': "Syncplay"},],
    console=['syncplayServer.py'],
    # *** If you wish to make the Syncplay client use console mode (for --no-gui to work) then comment out the above two lines and uncomment the following line:
    # console=['syncplayServer.py', {"script":"syncplayClient.py", "icon_resources":[(1, "resources\\icon.ico")], 'dest_base': "Syncplay"}],
    options={'py2exe': {
                         'dist_dir': OUT_DIR,
                         'packages': 'PySide2.QtUiTools',
                         'includes': 'twisted, sys, encodings, datetime, os, time, math, PySide2, liburl, ast, unicodedata',
                         'excludes': 'venv, _ssl, doctest, pdb, unittest, win32clipboard, win32file, win32pdh, win32security, win32trace, win32ui, winxpgui, win32pipe, win32process, Tkinter',
                         'dll_excludes': 'msvcr71.dll, MSVCP90.dll, POWRPROF.dll',
                         'optimize': 2,
                         'compressed': 1
                         }
             },
    data_files = [("resources", resources),("resources/lua/intf", intf_resources)],
    zipfile = "lib/libsync",
    cmdclass = {"py2exe": build_installer},               
)

sys.argv.extend(['py2exe', '-p win32com ', '-i twisted.web.resource'])
setup(**info)
