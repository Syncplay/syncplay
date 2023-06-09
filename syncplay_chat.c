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

const int64_t KEY_ACTION_MASK_ON  = 0x7FFFFFFFFFFFFFFF;
const int64_t KEY_ACTION_MASK_OFF = 0;

vlc_thread_t th;
input_thread_t *input = NULL;
vlc_mutex_t lock;
bool writing = false;
int port = 0;

char message[200];
int message_size = 0;

static int GetPort(vlc_object_t* libvlc) {
    char* lua_config = var_GetNonEmptyString(libvlc, "lua-config");
    if (!lua_config) return 0;
    
    char* config = malloc(strlen(lua_config) + 1);
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
    var_Change( libvlc, "key-action", VLC_VAR_SETMINMAX, &min, max);
}


// Detect playlist change event and aquire the input
static int PlaylistEvent( vlc_object_t *p_this, char const *psz_var,
                          vlc_value_t oldval, vlc_value_t val, void *p_data )
{
    input = val.p_address;
    msg_Info(p_this, "Playlist state changed");
    port = GetPort(p_this->obj.libvlc);
    return VLC_SUCCESS;
}

// Updates OSD indirectly to avoid an unknown bug
static void ShowText(vlc_object_t* libvlc) {
    var_SetInteger(libvlc, "syncplay-text", message_size);
}

// Hides the text
static void HideText(vlc_object_t* libvlc) {
    message_size = 0;
    ShowText(libvlc);
}

// Thread that currently draws the bliking cursor
static void *RunIntf(void*data) {
    vlc_object_t* libvlc = data;
    while(writing) {
        // SHOW CURSOR
        message[message_size] = '|';
        message[message_size + 1] = 0;
        if (input != NULL) {
            vout_OSDText(input_GetVout(input), 1, VOUT_ALIGN_TOP | VOUT_ALIGN_LEFT, 0xfffffffffff, message);
        }

        for (int i=0; i < 10; i++) {
            if (!writing) return; // REMOVE LATENCY -- Don't forget this is a thread
            msleep(50000);
        }

        // HIDE CURSOR
        message[message_size] = 0;
        if (input != NULL) {
            vout_OSDText(input_GetVout(input), 1, VOUT_ALIGN_TOP | VOUT_ALIGN_LEFT, 0xfffffffffff, message);
        }
        for (int i=0; i < 10; i++) {
            if (!writing) return; // REMOVE LATENCY -- Don't forget this is a thread
            msleep(50000);
        }
    }
}

// Display OSD text
static int SynplayText( vlc_object_t *libvlc, char const *psz_var,
                        vlc_value_t oldval, vlc_value_t newval, void *p_data )
{
    if (input != NULL) {
        message[message_size] = 0;
        vout_OSDText(input_GetVout(input), 1, VOUT_ALIGN_TOP | VOUT_ALIGN_LEFT, 0xfffffffffff, message);
    }
    return 0;
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

    msg_Info(intf, "key Code: %d", key_code);
    msg_Info(intf, "Key: %d", key);
    msg_Info(intf, "Sup key: %d", sup_key);
    msg_Info(intf, "config: %s", var_GetNonEmptyString(libvlc, "lua-config"));
    msg_Info(intf, "port: %d", port);

    if (writing) {
        switch(key) {
            case KEY_BACKSPACE:
                message_size > 0 ? message_size-- : 0;
                break;

            case KEY_ENTER:
            case KEY_ESC:
                writing=false;
                SetKeyActionMask(libvlc, &KEY_ACTION_MASK_ON);
                break;

            default:
                if (key <= 127) {
                    if (key == 32 && message_size > 0 && message[message_size - 1] != 32 || key != 32) {
                        char ch = key;
                        if (sup_key == 512 && isalpha(ch)) ch -= 0x20;
                        message[message_size++] = ch;
                    }
                }
                break;
        }

        switch(key) {
            case KEY_ENTER: 
            {
                // Stops the thread
                vlc_cancel(th);

                msg_Info(intf, "message: %s", message);
                var_SetString(intf->obj.libvlc, "chat-message", message);
                
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
                SetKeyActionMask(libvlc, &KEY_ACTION_MASK_OFF);
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