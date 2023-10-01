# portal-rpi
interface between the rpi and the portal

# Networking
The system binds a listener to a TCP socket, utilising the port specified in `config.ini`, to receive commands from the Portal.

# Modules
To reduce complexity and resource requirements, the system is broken up into several modules.

## Kiosk
This module requires the `Motion` module to turn the screen off after a period of inactivity, reported by `xscreensaver` using [xprintidle](https://github.com/g0hl1n/xprintidle).

If you wish to access streaming services, it may be necessary to install Widevine.  
`sudo apt install libwidevinecdm0`

## Motion
This module requires a method of sensing, and particularly supports either a HC-SR501 PIR or an RCWL-0516 radar sensor.

# Pins used
- The Motion modules use pin 17 for input from the sensor, and two pins of your choice for power and ground.
- The Lights module uses pins 13, 6, and 5, for the colors red, green, and blue, respectively, and a single pin of your choice for a ground.
