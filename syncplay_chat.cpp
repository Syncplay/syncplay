#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdlib.h>
#include <ctype.h>
/* VLC core API headers */
#include <vlc_common.h>
#include <vlc_plugin.h>
#include <vlc_interface.h>
#include <vlc_input.h>
#include <vlc_aout.h>
#include <vlc_viewpoint.h>
#include <vlc_vout_osd.h>
#include <vlc_playlist.h>
#include <vlc_actions.h>
#include <vlc_messages.h>
#include <vlc_events.h>
#include <vlc_variables.h>
#include <vlc_keystore.h>
#include <vlc_extensions.h>
#include <vlc_configuration.h>
#include <vlc_config.h>
#include <vlc_config_cat.h>
#include <vlc/vlc.h>

#include <string>
#include <unordered_map>
#include <regex>

int64_t KEY_ACTION_MASK_ON  = 0x7FFFFFFFFFFFFFFF;
int64_t KEY_ACTION_MASK_OFF = 0;

std::unordered_map<std::string, std::string> emojies = {
    { "joy", "\xF0\x9F\x98\x82" },
    { "sob", "\xF0\x9F\x98\xAD" },
    { "disappointed", "\xF0\x9F\x98\x9E" },
    { "angry", "\xF0\x9F\x98\xA0" },
    { "heart", "\xE2\x9D\xA4" },
    { "smirking", "\xF0\x9F\x98\x8F" },
    { "unamused", "\xF0\x9F\x98\x92" }
};

vlc_thread_t th;
input_thread_t *input = NULL;
vlc_mutex_t lock;
bool writing = false;
int port = 0;

std::string message;

static int GetPort(vlc_object_t* libvlc) {
    char* lua_config = var_GetNonEmptyString(libvlc, "lua-config");
    if (!lua_config) return 0;
    
    char* config = (char*)malloc(strlen(lua_config) + 1);
    strcpy(config, lua_config);

    char* prt = strstr(config, "port=") + 6;
    if (!prt) return 0;

    *strchr(prt, '"') = '\0';
    int port = atoi(prt);

    free(config);
    return port;
}

// Changes the minimum and maximum value for the key-action thought simulating disabling the keyboard actions
static void SetKeyActionMask(vlc_object_t* libvlc, int64_t *max) {
    int64_t min = 0;
    var_Change(libvlc, "key-action", VLC_VAR_SETMINMAX, (vlc_value_t*)&min, (vlc_value_t*)max);
}


// Detect playlist change event and aquire the input
static int PlaylistEvent( vlc_object_t *p_this, char const *psz_var,
                          vlc_value_t oldval, vlc_value_t val, void *p_data )
{
    input = (input_thread_t*)val.p_address;
    msg_Info(p_this, "Playlist state changed");
    port = GetPort((vlc_object_t*)p_this->obj.libvlc);
    return VLC_SUCCESS;
}

// Updates OSD indirectly to avoid an unknown bug
static void ShowText(vlc_object_t* libvlc) {
    var_SetInteger(libvlc, "syncplay-text", message.size());
}

// Hides the text
static void HideText(vlc_object_t* libvlc) {
    message="";
    ShowText(libvlc);
}

// Thread that currently draws the bliking cursor
static void *RunIntf(void*data) {
    vlc_object_t* libvlc = (vlc_object_t*)data;
    while(writing) {
        // SHOW CURSOR
        std::string displayMessage = message + '|';
        if (input != NULL) {
            vout_OSDText(input_GetVout(input), 1, VOUT_ALIGN_TOP | VOUT_ALIGN_LEFT, 0xfffffffffff, displayMessage.c_str());
        }

        for (int i=0; i < 10; i++) {
            if (!writing) return 0; // REMOVE LATENCY -- Don't forget this is a thread
            msleep(50000);
        }

        // HIDE CURSOR
        if (input != NULL) {
            vout_OSDText(input_GetVout(input), 1, VOUT_ALIGN_TOP | VOUT_ALIGN_LEFT, 0xfffffffffff, message.c_str());
        }
        for (int i=0; i < 10; i++) {
            if (!writing) return 0; // REMOVE LATENCY -- Don't forget this is a thread
            msleep(50000);
        }
    }
    return 0;
}

// Display OSD text
static int SynplayText( vlc_object_t *libvlc, char const *psz_var,
                        vlc_value_t oldval, vlc_value_t newval, void *p_data )
{
    if (input != NULL) {
        vout_OSDText(input_GetVout(input), 1, VOUT_ALIGN_TOP | VOUT_ALIGN_LEFT, 0xfffffffffff, message.c_str());
    }
    return 0;
}

// Converts text to emojis using the discord format
std::string parseEmojies(std::string msg) {
    for(auto emoji : emojies)
        msg = std::regex_replace(msg, std::regex(":"+emoji.first+":"), emoji.second);
    return msg;
}

std::string removeLastChar(std::string msg) {
    if (msg.size() > 3 && msg[msg.size() - 4] == '\xF0')
        return msg.substr(0, msg.size() - 4);
    if (msg.size() > 2 && msg[msg.size() - 3] == '\xE2')
        return msg.substr(0, msg.size() - 3);
    if (msg.size() > 0)
        msg.pop_back();
    return msg;
}

// Handle key events
static int KeyPressed( vlc_object_t *libvlc, char const *psz_var,
                        vlc_value_t oldval, vlc_value_t newval, void *p_data )
{
    intf_thread_t *intf = (intf_thread_t *)p_data;

    msg_Info(intf, "Synclpay: keypressed");

    int key_code = var_GetInteger(libvlc, "key-pressed");

    int key = key_code & 0xffff;
    int sup_key = (key_code >> 16) & 0xffff;

    // Some debug messages for ... debugging

    msg_Info(intf, "Key: %d", key);
    msg_Info(intf, "Sup key: %d", sup_key);

    if (writing) {
        switch(key) {
            case KEY_BACKSPACE:
                message = removeLastChar(message);
                break;

            case KEY_ENTER:
            case KEY_ESC:
                writing=false;
                SetKeyActionMask(libvlc, &KEY_ACTION_MASK_ON);
                break;

            default:
                if (key == 32) {
                    if (message.size() > 0 && message.back() != 32)
                        message.push_back(char(32));
                }
                else if (isalpha(key) || key == ':') {
                    char ch = key;
                    if (sup_key == 512) ch -= 0x20;
                    message.push_back(ch);
                    message = parseEmojies(message);
                }
                break;
        }

        switch(key) {
            case KEY_ENTER: 
            {
                // Stops the thread
                vlc_cancel(th);

                msg_Info(intf, "message: %s", message);

                var_SetString(intf->obj.libvlc, "chat-message", message.c_str());
                
            }
            case KEY_ESC:
                HideText(libvlc);
                break;
            default:
                ShowText(libvlc);
        }
    } else {
        switch(key) {
            case KEY_ENTER:
                SetKeyActionMask(libvlc, (int64_t*)&KEY_ACTION_MASK_OFF);
                writing = true;
                // Starts the thread
                vlc_clone(&th, RunIntf, intf->obj.libvlc, VLC_THREAD_PRIORITY_LOW);
                break;
        }
    }

    return VLC_SUCCESS;
}

static int Open(vlc_object_t *obj)
{
    intf_thread_t *intf = (intf_thread_t *)obj;

    vlc_mutex_init(&lock);

    var_Create( intf->obj.libvlc, "syncplay-text", VLC_VAR_INTEGER);
    var_Create(intf->obj.libvlc, "chat-message", VLC_VAR_STRING);
    var_AddCallback(intf->obj.libvlc, "syncplay-text", SynplayText, intf );
    var_AddCallback( intf->obj.libvlc, "key-pressed", KeyPressed, intf );
    var_AddCallback( pl_Get(intf), "input-current", PlaylistEvent, intf );

    msg_Info(intf, "Synclpay");
    
    // Returns error even tho no error ? It's working so don't tuch it
    return 1;
}


static void Close(vlc_object_t *obj)
{
    intf_thread_t *intf = (intf_thread_t *)obj;
}

vlc_module_begin()
    set_shortname(N_("Syncplay Chat"))
    set_description(N_("Syncplay Chat"))
    set_capability("interface", 200)
    set_callbacks(Open, Close)
    set_category(CAT_INTERFACE)
    set_subcategory(SUBCAT_INTERFACE_CONTROL)
vlc_module_end ()