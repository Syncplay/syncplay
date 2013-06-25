#!/usr/bin/env python
#coding:utf8
from distutils.core import setup
from py2exe.build_exe import py2exe
from string import Template

import syncplay
import sys
import os
import subprocess

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
  
  LangString ^Associate $${LANG_ENGLISH} "Associate Syncplay with multimedia files."
  LangString ^VLC $${LANG_ENGLISH} "Install Syncplay interface for VLC (requires VLC 2.0.6 or above)"
  LangString ^Shortcut $${LANG_ENGLISH} "Create Shortcuts in following locations:"
  LangString ^StartMenu $${LANG_ENGLISH} "Start Menu"
  LangString ^Desktop $${LANG_ENGLISH} "Desktop"
  LangString ^QuickLaunchBar $${LANG_ENGLISH} "Quick Launch Bar"
  LangString ^UninstConfig $${LANG_ENGLISH} "Delete configuration file."
    
  LangString ^Associate $${LANG_POLISH} "Skojarz Syncplaya z multimediami"
  LangString ^VLC $${LANG_POLISH} "Zainstaluj interface Syncplaya dla VLC(wymaga VLC 2.X.X)"
  LangString ^Shortcut $${LANG_POLISH} "Utworz skroty w nastepujacych miejscach:"
  LangString ^StartMenu $${LANG_POLISH} "Menu Start"
  LangString ^Desktop $${LANG_POLISH} "Pulpit"
  LangString ^QuickLaunchBar $${LANG_POLISH} "Pasek szybkiego uruchamiania"
  LangString ^UninstConfig $${LANG_POLISH} "Usun plik konfiguracyjny."
  
  PageEx license
    LicenseData resources\license.txt
  PageExEnd
  Page custom DirectoryCustom DirectoryCustomLeave
  Page instFiles
  
  UninstPage custom un.installConfirm un.installConfirmLeave
  UninstPage instFiles
  
  Var Dialog
  Var Icon_Syncplay
  Var Icon_Syncplay_Handle
  Var CheckBox_Associate
  Var CheckBox_VLC
  Var CheckBox_StartMenuShortcut
  Var CheckBox_DesktopShortcut
  Var CheckBox_QuickLaunchShortcut
  Var CheckBox_Associate_State
  Var CheckBox_VLC_State
  Var CheckBox_StartMenuShortcut_State
  Var CheckBox_DesktopShortcut_State
  Var CheckBox_QuickLaunchShortcut_State
  Var Button_Browse
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
  Var VLC_Version
    
  !macro APP_ASSOCIATE EXT FileCLASS DESCRIPTION COMMANDTEXT COMMAND
    WriteRegStr HKCR ".$${EXT}" "" "$${FileCLASS}"
    WriteRegStr HKCR "$${FileCLASS}" "" `$${DESCRIPTION}`
    WriteRegStr HKCR "$${FileCLASS}\shell" "" "open"
    WriteRegStr HKCR "$${FileCLASS}\shell\open" "" `$${COMMANDTEXT}`
    WriteRegStr HKCR "$${FileCLASS}\shell\open\command" "" `$${COMMAND}`
  !macroend
  
  !macro APP_UNASSOCIATE EXT FileCLASS
    ; Backup the previously associated File class
    ReadRegStr $$R0 HKCR ".$${EXT}" `$${FileCLASS}_backup`
    WriteRegStr HKCR ".$${EXT}" "" "$$R0"
    DeleteRegKey HKCR `$${FileCLASS}`
  !macroend
  
  !macro ASSOCIATE EXT
    !insertmacro APP_ASSOCIATE "$${EXT}" "Syncplay.$${EXT}" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
  !macroend
  
  !macro UNASSOCIATE EXT
    !insertmacro APP_UNASSOCIATE "$${EXT}" "Syncplay.$${EXT}"
  !macroend
  
  ;Prevents from running more than one instance of installer and sets default state of checkboxes
  Function .onInit
    System::Call 'kernel32::CreateMutexA(i 0, i 0, t "myMutex") i .r1 ?e'
    Pop $$R0
    StrCmp $$R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
      Abort
        
    StrCpy $$CheckBox_Associate_State $${BST_CHECKED}
    StrCpy $$CheckBox_StartMenuShortcut_State $${BST_CHECKED}
    
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
    Push A ; A means auto count languages
    LangDLL::LangDialog "Installer Language" "Please select the language of the installer"
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

    $${NSD_CreateLabel} 0u 111u 265u 8u "$$(^SpaceRequired)$$SizeMB"
    Pop $$Label_Size
    
    $${NSD_CreateLabel} 0u 122u 265u 8u "$$(^SpaceAvailable)$$AvailibleSpaceGiB.$$AvailibleSpaceGB"
    Pop $$Label_Space
    
    $${NSD_CreateCheckBox} 8u 59u 187u 10u "$$(^Associate)"
    Pop $$CheckBox_Associate
    
    $${NSD_CreateCheckBox} 8u 72u 250u 10u "$$(^VLC)"
    Pop $$CheckBox_VLC
    
    $${NSD_CreateLabel} 8u 85u 187u 10u "$$(^Shortcut)"
    Pop $$Label_Shortcut
    
    $${NSD_CreateCheckbox} 8u 98u 50u 10u "$$(^StartMenu)"
    Pop $$CheckBox_StartMenuShortcut

    $${NSD_CreateCheckbox} 68u 98u 50u 10u "$$(^Desktop)"
    Pop $$CheckBox_DesktopShortcut
    
    $${NSD_CreateCheckbox} 128u 98u 150u 10u "$$(^QuickLaunchBar)"
    Pop $$CheckBox_QuickLaunchShortcut
    
    $${If} $$CheckBox_Associate_State == $${BST_CHECKED}
      $${NSD_Check} $$CheckBox_Associate
    $${EndIf}

    $${If} $$CheckBox_VLC_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_VLC
    $${EndIf}
    
    $${If} $$CheckBox_StartMenuShortcut_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_StartMenuShortcut
    $${EndIf}
    
    $${If} $$CheckBox_DesktopShortcut_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_DesktopShortcut
    $${EndIf}
    
    $${If} $$CheckBox_QuickLaunchShortcut_State == $${BST_CHECKED}
    	$${NSD_Check} $$CheckBox_QuickLaunchShortcut
    $${EndIf}
    
    ReadRegStr $$VLC_Version HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VLC media player" "VersionMajor"
    $${If} $$VLC_Version != "2"
      EnableWindow $$CheckBox_VLC 0
    $${EndIf}
    nsDialogs::Show

    $${NSD_FreeIcon} $$Icon_Syncplay_Handle

  FunctionEnd
  
  Function DirectoryCustomLeave
    $${NSD_GetText} $$Text_Directory $$INSTDIR
    $${NSD_GetState} $$CheckBox_Associate $$CheckBox_Associate_State
    $${NSD_GetState} $$CheckBox_VLC $$CheckBox_VLC_State
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
    $${If} $$CheckBox_Associate_State == $${BST_CHECKED}
      Call Associate
      DetailPrint "Associated Syncplay with multimedia files"
    $${EndIf}
    
    $${If} $$CheckBox_StartMenuShortcut_State == $${BST_CHECKED}
      CreateDirectory $$SMPROGRAMS\Syncplay
      CreateShortCut "$$SMPROGRAMS\Syncplay\Syncplay.lnk" "$$INSTDIR\Syncplay.exe" "" 
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
      ReadRegStr $$VLC_Directory HKLM "Software\VideoLAN\VLC" "InstallDir"
      SetOutPath $$VLC_Directory\lua\intf
      File resources\syncplay.lua
    $${EndIf}
  FunctionEnd
    
  ;Associates extensions with Syncplay
  Function Associate
    !insertmacro ASSOCIATE avi
    !insertmacro ASSOCIATE mpg
    !insertmacro ASSOCIATE mpeg
    !insertmacro ASSOCIATE mpe
    !insertmacro ASSOCIATE m1v
    !insertmacro ASSOCIATE m2v
    !insertmacro ASSOCIATE mpv2
    !insertmacro ASSOCIATE mp2v
    !insertmacro ASSOCIATE mkv
    !insertmacro ASSOCIATE mp4
    !insertmacro ASSOCIATE m4v
    !insertmacro ASSOCIATE mp4v
    !insertmacro ASSOCIATE 3gp
    !insertmacro ASSOCIATE 3gpp
    !insertmacro ASSOCIATE 3g2
    !insertmacro ASSOCIATE 3pg2
    !insertmacro ASSOCIATE flv
    !insertmacro ASSOCIATE f4v
    !insertmacro ASSOCIATE rm
    !insertmacro ASSOCIATE wmv
    !insertmacro ASSOCIATE swf
    !insertmacro ASSOCIATE rmvb
    !insertmacro ASSOCIATE divx
    !insertmacro ASSOCIATE amv
  FunctionEnd
  
  Function WriteRegistry
    Call GetSize
    WriteRegStr HKLM SOFTWARE\Syncplay "Install_Dir" "$$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayName" "Syncplay"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "InstallLocation" "$$INSTDIR" 
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "UninstallString" '"$$INSTDIR\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayIcon" "$$INSTDIR\resources\icon.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "Publisher" "Syncplay"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayVersion" "$version"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "URLInfoAbout" "http://syncplay.pl/"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoRepair" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "EstimatedSize" "$$SizeHex"
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
    Delete $$SMPROGRAMS\Syncplay\Uninstall.lnk
    Delete $$SMPROGRAMS\Syncplay\SyncplayWebsite.url
    RMDir $$SMPROGRAMS\Syncplay
    Delete $$DESKTOP\Syncplay.lnk
    Delete $$QUICKLAUNCH\Syncplay.lnk
    ReadRegStr $$VLC_Directory HKLM "Software\VideoLAN\VLC" "InstallDir"
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
    RMDir $$INSTDIR\resources
    RMDir $$INSTDIR\lib
    RMDir $$INSTDIR

    $${If} $$Uninst_CheckBox_Config_State == $${BST_CHECKED}
      Delete $$APPDATA\.syncplay
    $${EndIf}
  SectionEnd
"""

class NSISScript(object):
    def create(self):
        fileList, totalSize = self.getBuildDirContents(OUT_DIR)
        print "Total size eq: {}".format(totalSize)
        installFiles = self.prepareInstallListTemplate(fileList) 
        uninstallFiles = self.prepareDeleteListTemplate(fileList)
        
        if(os.path.isfile(SETUP_SCRIPT_PATH)):
            raise RuntimeError("Cannot create setup script, file exists at {}".format(SETUP_SCRIPT_PATH))
        contents =  Template(NSIS_SCRIPT_TEMPLATE).substitute(
                                                              version = syncplay.version,
                                                              uninstallFiles = uninstallFiles,
                                                              installFiles = installFiles,
                                                              totalSize = totalSize,
                                                              )
        with open(SETUP_SCRIPT_PATH, "w") as outfile:
            outfile.write(contents)
        
    def compile(self):
        if(not os.path.isfile(NSIS_COMPILE)):
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
                if(not fileList.has_key(new_root)):
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
     'resources/timeline_marker.png'
    ]
resources = ["resources/syncplay.lua", "resources/icon.ico", "resources/syncplay.png"]
resources.extend(guiIcons)

common_info = dict(
    name='Syncplay',
    version=syncplay.version,
    author='Uriziel',
    author_email='urizieli@gmail.com',
    description='Syncplay',
)
    
info = dict(
    common_info,
    windows=[{"script":"syncplayClient.py", "icon_resources":[(1, "resources\\icon.ico")], 'dest_base': "Syncplay"}],
    console=['syncplayServer.py'],
    options={'py2exe': {
                         'dist_dir': OUT_DIR,
                         'packages': 'PySide.QtUiTools',
                         'includes': 'twisted, sys, encodings, datetime, os, time, math, PySide',
                         'excludes': 'venv, _ssl, doctest, pdb, unittest, win32clipboard, win32file, win32pdh, win32security, win32trace, win32ui, winxpgui, win32pipe, win32process',
                         'dll_excludes': 'msvcr71.dll, MSVCP90.dll, POWRPROF.dll',
                         'optimize': 2,
                         'compressed': 1
                         }
             },
    data_files = [("resources", resources)],
    zipfile = "lib/libsync",
    cmdclass = {"py2exe": build_installer},               
)

sys.argv.extend(['py2exe', '-p win32com ', '-i twisted.web.resource'])
setup(**info)

