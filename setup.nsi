    !include LogicLib.nsh
    !include nsDialogs.nsh
     
    Name "Syncplay"
    OutFile "Syncplay.exe"
    InstallDir $PROGRAMFILES\Syncplay
    RequestExecutionLevel admin
    XPStyle on
    Icon resources\icon.ico   ;Change DIR
    SetCompressor /SOLID lzma
     
    PageEx license
    LicenseData resources\license.txt
    PageExEnd
    Page custom Associate
    Page directory
    Page instfiles
     
    UninstPage uninstConfirm
    UninstPage instfiles
     
    LoadLanguageFile "${NSISDIR}\Contrib\Language files\English.nlf"
    LoadLanguageFile "${NSISDIR}\Contrib\Language files\Polish.nlf"
     
    LangString Assoc ${LANG_ENGLISH} "Associate Syncplay with following extensions."
    LangString Assoc ${LANG_POLISH} "Skojarz Syncplay z nastêpuj¹cymi rozszerzeniami."
     
    Var hCtl_Associate
    Var hCtl_Associate_Label1
    Var hCtl_Associate_Bitmap1
    Var hCtl_Associate_Bitmap1_hImage
    Var hCtl_Associate_mkv
    Var hCtl_Associate_mp4
    Var hCtl_Associate_avi
    Var hCtl_Associate_flv
    Var hCtl_Associate_mpg
    Var hCtl_Associate_rmvb
    Var hCtl_Associate_vob
    Var hCtl_Associate_swf
    Var hCtl_Associate_wmv
    Var State_mkv
    Var State_mp4
    Var State_avi
    Var State_flv
    Var State_mpg
    Var State_rmvb
    Var State_vob
    Var State_swf
    Var State_wmv
    Var ImageHandle
     
    ; dialog create function
    Function fnc_Associate_Create
     
      ; === Associate (type: Dialog) ===
      nsDialogs::Create 1018
      Pop $hCtl_Associate
      ${If} $hCtl_Associate == error
        Abort
      ${EndIf}
     
      ; === Label1 (type: Label) ===
      ${NSD_CreateLabel} 25u 0u 269u 12u "$(Assoc)"
      Pop $hCtl_Associate_Label1
     
      ; === Bitmap1 (type: Bitmap) ===
      ${NSD_CreateIcon} 0u 0u 22u 20u ""
      Pop $hCtl_Associate_Bitmap1
     
      ${NSD_SetIcon} $hCtl_Associate_Bitmap1 resources\icon.ico $ImageHandle   ;ChangeDir
     
      ; === mkv (type: Checkbox) ===
      ${NSD_CreateCheckbox} 5u 26u 68u 14u ".mkv"
      Pop $hCtl_Associate_mkv
     
      ; === mp4 (type: Checkbox) ===
      ${NSD_CreateCheckbox} 5u 43u 68u 14u ".mp4"
      Pop $hCtl_Associate_mp4
     
      ; === avi (type: Checkbox) ===
      ${NSD_CreateCheckbox} 5u 60u 68u 14u ".avi"
      Pop $hCtl_Associate_avi
     
      ; === flv (type: Checkbox) ===
      ${NSD_CreateCheckbox} 87u 26u 68u 14u ".flv"
      Pop $hCtl_Associate_flv
     
      ; === mpg (type: Checkbox) ===
      ${NSD_CreateCheckbox} 87u 43u 68u 14u ".mpg"
      Pop $hCtl_Associate_mpg
     
      ; === rmvb (type: Checkbox) ===
      ${NSD_CreateCheckbox} 87u 60u 68u 14u ".rmvb"
      Pop $hCtl_Associate_rmvb
     
      ; === vob (type: Checkbox) ===
      ${NSD_CreateCheckbox} 169u 26u 68u 14u ".vob"
      Pop $hCtl_Associate_vob
     
      ; === swf (type: Checkbox) ===
      ${NSD_CreateCheckbox} 169u 43u 68u 14u ".swf"
      Pop $hCtl_Associate_swf
     
      ; === wmv (type: Checkbox) ===
      ${NSD_CreateCheckbox} 169u 60u 68u 14u ".wmv"
      Pop $hCtl_Associate_wmv
     
    FunctionEnd
     
    ; dialog show function
    Function Associate
            Call fnc_Associate_Create
            nsDialogs::Show $hCtl_Associate
            ${NSD_FreeImage} $ImageHandle
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
     
    !macro APP_ASSOCIATE EXT FILECLASS DESCRIPTION COMMANDTEXT COMMAND
            WriteRegStr HKCR ".${EXT}" "" "${FILECLASS}"
            WriteRegStr HKCR "${FILECLASS}" "" `${DESCRIPTION}`
            WriteRegStr HKCR "${FILECLASS}\shell" "" "open"
            WriteRegStr HKCR "${FILECLASS}\shell\open" "" `${COMMANDTEXT}`
            WriteRegStr HKCR "${FILECLASS}\shell\open\command" "" `${COMMAND}`
    !macroend
     
    Section "Install"
            SetOverwrite on
            SetOutPath $INSTDIR
            File /r "syncplay v1.2.5\*"
       
            WriteRegStr HKLM SOFTWARE\Syncplay "Install_Dir" "$INSTDIR"
            WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "DisplayName" "Syncplay"
            WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "UninstallString" '"$INSTDIR\uninstall.exe"'
            WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoModify" 1
            WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay" "NoRepair" 1
            ${NSD_GetState} $hCtl_Associate_mkv $State_mkv
            ${If}  $State_mkv == 0
                    !insertmacro APP_ASSOCIATE "mkv" "Syncplay.mkv" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""  
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_mp4 $State_mp4
            ${If}  $State_mp4 == 0
                    !insertmacro APP_ASSOCIATE "mp4" "Syncplay.mp4" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_avi $State_avi
            ${If}  $State_avi == 0
                    !insertmacro APP_ASSOCIATE "avi" "Syncplay.avi" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_flv $State_flv
            ${If}  $State_flv == 0
                    !insertmacro APP_ASSOCIATE "flv" "Syncplay.flv" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_mpg $State_mpg
            ${If}  $State_mpg == 0
                    !insertmacro APP_ASSOCIATE "mpg" "Syncplay.mpg" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_rmvb $State_rmvb
            ${If}  $State_rmvb == 0
                    !insertmacro APP_ASSOCIATE "rmvb" "Syncplay.rmvb" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""  
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_vob $State_vob
            ${If}  $State_vob == 0
                    !insertmacro APP_ASSOCIATE "vob" "Syncplay.vob" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_swf $State_swf
            ${If}  $State_swf == 0
                    !insertmacro APP_ASSOCIATE "swf" "Syncplay.swf" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""
            ${EndIf}
            ${NSD_GetState} $hCtl_Associate_wmv $State_wmv
            ${If}  $State_wmv == 0
                    !insertmacro APP_ASSOCIATE "wmv" "Syncplay.wmv" "$INSTDIR\Syncplay.exe,%1%" \
                    "Open with Syncplay" "$INSTDIR\Syncplay.exe $\"%1$\""  
            ${EndIf}
            WriteUninstaller uninstall.exe
           
    SectionEnd
     
    Section "Uninstall"
            DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Syncplay"
            DeleteRegKey HKLM SOFTWARE\Syncplay
            RMDir /r $INSTDIR
    SectionEnd
