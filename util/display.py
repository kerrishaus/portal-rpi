import subprocess

from net import kerrishausapi

def display_power_on():
    kerrishausapi.notify_screen(7)
    return subprocess.run('export DISPLAY=:0 && xscreensaver-command -deactivate', shell=True)

def display_power_off():
    kerrishausapi.notify_screen(6)
    return subprocess.run('export DISPLAY=:0 && xscreensaver-command -activate', shell=True)

def is_display_powered():
    # ask if the display is already powered on
    result = subprocess.run('export DISPLAY=:0 && xscreensaver-command -time', shell=True, capture_output=True)
    output = str(result.stdout)
    if str(output) == "b'display_power=1\\n'":
        return True
    else:
        return False

def get_idle_time():
    result = subprocess.run('export DISPLAY=:0 && sudo -u kiosk xprintidle', shell=True, capture_output=True)
    output = str(result.stdout)
    output = output[2:len(output) - 3]

    if output == '':
        return -1

    idletime = int(output)
    return idletime