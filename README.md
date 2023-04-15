<p align="center">
<img src="assets/demo.gif">

# RmKeyboard
Utilizes the `uniput` device on 3.x.x versions of the ReMarkable device to inject keystrokes as a virtual keyboard device. There are many ways to use this but in this case I've decided to use python with websockets to send keystrokes over the network to the RM from another device. 

# How to use
On the device you want to hook & send the keystrokes from (client) all you need to do is run the `client.py` script with the required arguments

On the ReMarkable:
```
opkg install python3 gcc libudev
wget https://bootstrap.pypa.io/get-pip.py | python3
pip install websockets python-uinput
modprobe uinput
```
Then run `server.py` with the required arguments.

Basic example:
```
python3 client.py -t supersecure -a 10.11.99.1 
python3 server.py -t supersecure 
```
This runs the websocket over a basic, unsecure connection (no SSL/TLS) - you shouldn't worry about this unless you want to expose it over the internet. `10.11.99.1` is the address the RM is located at, by defult the websocket binds to all addresses on the RM (`0.0.0.0`) 

To use SSL, you must provide a `cert.pem` and `key.pem` in the `certs` folder. An example, self-signed, one for `10.11.99.1` & `192.168.0.36` are alredy provided for you with a `san.cnf` file. To generate these certificates you can use

```
openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout key.pem -out cert.pem -config san.cnf
```

# Limitations
1) Currently you will need python on the RM device which means installing toltec which only has partial support for 3.x.x versions. However, I will be compiling a binary soon for a server implemtnation written in rust

2) You will need a middle device for the client software to run on (which takes keyboard input). This could even be your phone if it is rooted - Looking into being able to use your phone without root. 

# Thanks
Thanks to everyone at the reMarkable [discord](https://discord.com/invite/JSSGnFY) as always for the amzing work that they do and @Eeems for providing the base python client & original idea 💖
