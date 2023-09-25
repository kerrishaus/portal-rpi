# portal-rpi
interface between the rpi and the portal

# Networking
The system binds a listener to a TCP socket, utilising the port specified in `config.ini`, to receive commands from the Portal.

# Kiosk,Motion module.
The Kiosk or Motion modules require the use of a HC-SR501 PIR or RCWL-0516 radar sensor, and will power the current display off or on after a set period of user inactivity as reported by xscreensaver.

# Pins used
- The Motion modules use pin 17 for input from the sensor, and two pins of your choice for power and ground.
- The Lights module uses pins 13, 6, and 5, for the colors red, green, and blue, respectively, and a single pin of your choice for a ground.
