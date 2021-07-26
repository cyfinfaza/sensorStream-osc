# sensorstrem-osc
A websocket server and TCP OSC client for streaming pan and tilt data to an ETC Eos lighting console. Easily control the pan and tilt of moving lights with your phone. Great if you are using Nomad, and you're stuck with a mouse/trackpad for ML controls. 
## Requirements
- LAN network with all devices connected to it (for example, start a hotspot on a phone or Windows device). You will need the IP address of some or all devices.
- Computer with a Python version between 3.6.1 and 3.8.x installed, connected to LAN, with the `websockets` module installed (`pip install websockets`)
- Reasonably up-to-date ETC Eos (or Eos Nomad) console, connected to LAN with OSC over TCP enabled on TCP port 3032 (the default port)
- Android device running a recent version of Chrome, connected to LAN
## How to use
1. Ensure OSC over TCP is enabled in Eos
2. Disable secure origin protection on the Android device (instructions below)
3. Set the console IP (instructions below)
4. Start `server.py`. This should start a websocket-enabled server on port 80, and connect to the console's OSC endpoint over TCP
5. Visit the IP address of the computer running `server.py` on the Android device's browser. Tap "Initiate" to start sending data to the server. You should see the "Data" section of the page changing as you move the device around. If it doesn't work, ensure you have the secure origin protection disabled correctly.
6. Select a moving light in Eos, and toggle the pan or tilt control on or off in the web client to control the light . 

Note that you can open the web client in more than one place to view current data, and to enable or disable pan or tilt control. This is useful if you are holding the phone in a weird position, and want to stop controlling the light from a different device so that you don't accidentally bump the phone and move the light the wrong way. **Do not click/tap "Initiate" on the second device.**
## Disabling Secure Origin Protection
In order for Chrome to allow access to sensor data on the client served over HTTP (not a secure origin), you must "treat given (insecure) origins as secure origins" in the Chrome flags.  
1. Visit chrome://flags
2. Search for "Insecure origins treated as secure"
3. Enable and add http://your.server.ip.address (replacing with actual IP of the computer running `server.py`)
4. Restart Chrome
## Set Console IP in `server.py`
The server is preconfigured to run on the same machine as the Eos instance, for example when using Nomad. This means it will attempt to connect to `127.0.0.1` on port `3032`. These values can be easily changed though, by editing the `c.connect` line near the top of `server.py`.
## Troubleshooting
I have no idea what is going to go wrong for you. Check your Python version, check your OSC configuration, and check secure origin protection. If nothing works, post an issue, or conact me @cyfinfaza on Telegram. Honestly, it would be surprising to know that anyone even read this.
## About the OSC Library (`OSC.py` and `SocketServer.py`)
Please don't ask me where I got it. I have no clue. I'm literally writing this readme 6 months later. All I know is that it was the only solution I could find. It is **not my work**, and I do not take credit for it.