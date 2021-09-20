import subprocess

from net import kerrishausapi

def display_power_on():
    kerrishausapi.update(7)
    return subprocess.run('vcgencmd display_power 1', shell=True)

def display_power_off():
    kerrishausapi.update(6)
    return subprocess.run('vcgencmd display_power 0', shell=True)

def is_display_powered():
    # ask if the display is already powered on
    result = subprocess.run('vcgencmd display_power -1', shell=True, capture_output=True)
    output = str(result.stdout)
    if str(output) == "b'display_power=1\\n'":
        return True
    else:
        return False

def get_idle_time():
    result = subprocess.run('export DISPLAY=:0 && sudo -u pi xprintidle', shell=True, capture_output=True)
    output = str(result.stdout)
    output = output[2:len(output) - 3]
    idletime = int(output)
    return idletime