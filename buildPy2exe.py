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

  LoadLanguageFile "$${NSISDIR}\Contrib\Language files\English.nlf"
  LoadLanguageFile "$${NSISDIR}\Contrib\Language files\Polish.nlf"
  
  Name "Syncplay"
  OutFile "Syncplay.exe"
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
  
  PageEx license
    LicenseData resources\license.txt
  PageExEnd
  Page directory
  Page instFiles
     
  UninstPage uninstConfirm
  UninstPage instFiles
    
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
  
  ;Associates extensions with Syncplay
  Function Associate
    !insertmacro APP_ASSOCIATE "mkv" "Syncplay.mkv" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "mp4" "Syncplay.mp4" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "avi" "Syncplay.avi" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "flv" "Syncplay.flv" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "mpg" "Syncplay.mpg" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "rmvb" "Syncplay.rmvb" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "vob" "Syncplay.vob" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "swf" "Syncplay.swf" "$$INSTDIR\Syncplay.exe,%1%" \
     "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
    !insertmacro APP_ASSOCIATE "wmv" "Syncplay.wmv" "$$INSTDIR\Syncplay.exe,%1%" \
    "Open with Syncplay" "$$INSTDIR\Syncplay.exe $$\"%1$$\""
  FunctionEnd
  
  Function WriteRegistry
    WriteRegStr HKLM SOFTWARE\Syncplay "Install_Dir" "$$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayName" "Syncplay"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "UninstallString" '"$$INSTDIR\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayIcon" "$$INSTDIR\lib\icon.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "Publisher" "Syncplay"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "URLInfoAbout" "http://syncplay.pl/"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoRepair" 1
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
    $uninstallFiles
  FunctionEnd
  
  ;Prevents from running more than one instance of installer
  Function .onInit
    System::Call 'kernel32::CreateMutexA(i 0, i 0, t "myMutex") i .r1 ?e'
    Pop $$R0
    StrCmp $$R0 0 +3
    MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
      Abort
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
     
  Section "Install"
    SetOverwrite on
    SetOutPath $$INSTDIR
    WriteUninstaller uninstall.exe
    Call Associate
    Call WriteRegistry
    
    $installFiles
  SectionEnd
     
  Section "Uninstall"
    Call un.AssociateDel
    Call un.DeleteFiles
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay"
    DeleteRegKey HKLM SOFTWARE\Syncplay
    Delete $$INSTDIR\uninstall.exe
    RMDir $$INSTDIR
  SectionEnd
"""

class NSISScript(object):
    def create(self):
        fileList = self.getBuildDirContents(OUT_DIR)
        installFiles = self.prepareInstallListTemplate(fileList) 
        uninstallFiles = self.prepareDeleteListTemplate(fileList)
        
        if(os.path.isfile(SETUP_SCRIPT_PATH)):
            raise RuntimeError("Cannot create setup script, file exists at {}".format(SETUP_SCRIPT_PATH))
        contents =  Template(NSIS_SCRIPT_TEMPLATE).substitute(
                                                              version = syncplay.version,
                                                              uninstallFiles = uninstallFiles,
                                                              installFiles = installFiles,
                                                              )
        with open(SETUP_SCRIPT_PATH, "w") as outfile:
            outfile.write(contents)
        
    def compile(self):
        subproc = subprocess.Popen([NSIS_COMPILE, SETUP_SCRIPT_PATH], env=os.environ)
        subproc.communicate()
        retcode = subproc.returncode
        os.remove(SETUP_SCRIPT_PATH)
        if retcode:
            raise RuntimeError("NSIS compilation return code: %d" % retcode)
   
    def getBuildDirContents(self, path):
        fileList = {}
        for root, _, files in os.walk(path):
            for file_ in files:
                new_root = root.replace(OUT_DIR, "").strip("\\")
                if(not fileList.has_key(new_root)):
                    fileList[new_root] = []
                fileList[new_root].append(file_)
        return fileList           
    
    
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

        
common_info = dict(
    name='Syncplay',
    version=syncplay.version,
    author='Uriziel',
    author_email='urizieli@gmail.com',
    description='Syncplay',
)
    
info = dict(
    common_info,
    console=[{"script":"syncplayClient.py", "icon_resources":[(1, "resources\\icon.ico")], 'dest_base': "Syncplay"}, 'syncplayServer.py'],
    options={'py2exe': {
                         'dist_dir': OUT_DIR,
                         'includes': 'cairo, pango, pangocairo, atk, gobject, twisted',
                         'excludes': 'venv, _ssl, doctest, pdb, unittest, difflib, win32clipboard, win32event, win32file, win32pdh, win32security, win32trace, win32ui, winxpgui, win32pipe, win32process',
                         'dll_excludes': 'msvcr71.dll',
                         'optimize': 2,
                         'compressed': 1
                         }
             },
    data_files = [("resources", ["resources/icon.ico",])],
    zipfile = "lib/libsync",
    cmdclass = {"py2exe": build_installer},               
)

sys.argv.extend(['py2exe', '-p win32com ', '-i twisted.web.resource'])
setup(**info)

