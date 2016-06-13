import autopy
import copy
import ctypes
import json
import sys
import time

GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
GetKeyState = ctypes.windll.user32.GetKeyState
GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState
GetWindowText = ctypes.windll.user32.GetWindowTextA

def getForegroundWindowText():
    hwndForeground = GetForegroundWindow()
    strptr = ctypes.create_string_buffer(100)
    ret = GetWindowText(hwndForeground, strptr, len(strptr))
    if ret == 0:
        print "GetWindowText returned 0"
    return strptr.value

in_chat = False

# Virtual Key Codes
# https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731%28v=vs.85%29.aspx
# 0x14 = CAPS LOCK
# 0x0D = enter

config_file = open(sys.argv[1])
config = json.load(config_file)
config_file.close()

print config

tick_rate = config["tick_rate"]
key_rate = config["keys"]


last_keyed = {}

def reset_last_keyed():
    for key in key_rate.keys():
        last_keyed[key] = 1



reset_last_keyed()
while True:
    if GetKeyState(0x14):
        if getForegroundWindowText() == "Diablo III":
            for key in last_keyed.keys():
                if last_keyed[key] == 0:
                    actual_key = str(key)
                    if actual_key == "SHIFT+LCLICK":
                        autopy.key.toggle(autopy.key.MOD_SHIFT, True)
                        autopy.mouse.click()
                        autopy.key.toggle(autopy.key.MOD_SHIFT, False)
                    else:
                        autopy.key.tap(str(key))
                    last_keyed[key] = key_rate[key]
                last_keyed[key] -= 1
    else:
        reset_last_keyed()
    time.sleep(tick_rate)
