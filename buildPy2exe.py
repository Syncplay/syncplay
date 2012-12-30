#!/usr/bin/env python
#coding:utf8
from distutils.core import setup
from py2exe.build_exe import py2exe

import syncplay
import sys
import os.path
import subprocess
#
#NSIS_SCRIPT_TEMPLATE = r"""
#!define py2exeOutputDirectory '{output_dir}\'
#!define exe '{program_name}.exe'
#
#; Uses solid LZMA compression. Can be slow, use discretion.
#SetCompressor /SOLID lzma
#
#; Sets the title bar text (although NSIS seems to append "Installer")
#Caption "{program_desc}"
#
#Name '{program_name}'
#OutFile ${{exe}}
#Icon '{icon_location}'
#; Use XPs styles where appropriate
#XPStyle on
#
#; You can opt for a silent install, but if your packaged app takes a long time
#; to extract, users might get confused. The method used here is to show a dialog
#; box with a progress bar as the installer unpacks the data.
#;SilentInstall silent
#AutoCloseWindow true
#ShowInstDetails nevershow
#
#Section
#    DetailPrint "Extracting application..."
#    SetDetailsPrint none
#    
#    InitPluginsDir
#    SetOutPath '$PLUGINSDIR'
#    File /r '${{py2exeOutputDirectory}}\*'
#
#    GetTempFileName $0
#    ;DetailPrint $0
#    Delete $0
#    StrCpy $0 '$0.bat'
#    FileOpen $1 $0 'w'
#    FileWrite $1 '@echo off$\r$\n'
#    StrCpy $2 $TEMP 2
#    FileWrite $1 '$2$\r$\n'
#    FileWrite $1 'cd $PLUGINSDIR$\r$\n'
#    FileWrite $1 '${{exe}}$\r$\n'
#    FileClose $1
#    ; Hide the window just before the real app launches. Otherwise you have two
#    ; programs with the same icon hanging around, and it's confusing.
#    HideWindow
#    nsExec::Exec $0
#    Delete $0
#SectionEnd
#"""
#
#class NSISScript(object):
#    
#    NSIS_COMPILE = "C:\\Program Files (x86)\\NSIS\\makensis.exe"
#    
#    def __init__(self, program_name, program_desc, dist_dir, icon_loc):
#        self.program_name = program_name
#        self.program_desc =  program_desc
#        self.dist_dir = dist_dir
#        self.icon_loc = icon_loc
#        self.pathname = "setup_%s.nsi" % self.program_name
#    
#    def create(self):
#        contents = NSIS_SCRIPT_TEMPLATE.format(
#                    program_name = self.program_name,
#                    program_desc = self.program_desc,
#                    output_dir = self.dist_dir,
#                    icon_location = os.path.join(os.path.dirname(self.dist_dir), self.icon_loc))
#        with open(self.pathname, "w") as outfile:
#            outfile.write(contents)
#
#    def compile(self):
#        print os.stat(self.NSIS_COMPILE)
#        subproc = subprocess.Popen(
#            # "/P5" uses realtime priority for the LZMA compression stage.
#            # This can get annoying though.
#            [self.NSIS_COMPILE, self.pathname, "/P5"], env=os.environ)
#        return 
#        subproc.communicate()
#        
#        retcode = subproc.returncode
#        
#        if retcode:
#            raise RuntimeError("NSIS compilation return code: %d" % retcode)
#
#class build_installer(py2exe):
#    # This class first builds the exe file(s), then creates an NSIS installer
#    # that runs your program from a temporary directory.
#    def run(self):
#        # First, let py2exe do it's work.
#        py2exe.run(self)
#        # Create the installer, using the files py2exe has created.
#        script = NSISScript('Syncplay',
#                            'Syncplay',
#                            self.dist_dir,
#                            "resources\\icon.ico")
#        print "*** creating the NSIS setup script***"
#        script.create()
#        print "*** compiling the NSIS setup script***"
#        script.compile()

sys.argv.extend(['py2exe', '-p win32com ', '-i twisted.web.resource'])
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
                         'dist_dir': "syncplay v%s" % syncplay.version,
                         'includes': 'cairo, pango, pangocairo, atk, gobject, twisted',
                         'excludes': 'venv, _ssl, doctest, pdb, unittest, difflib, win32clipboard, win32event, win32file, win32pdh, win32security, win32trace, win32ui, winxpgui, win32pipe, win32process',
                         'dll_excludes': 'msvcr71.dll',
                         'optimize': 2,
                         'compressed': 1
                         }
             },
    zipfile = "lib/libsync",
#    cmdclass = {"py2exe": build_installer},                      
)

setup(**info)

