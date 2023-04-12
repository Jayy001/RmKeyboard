import sys
import struct
import socket
import keyboard
import time

address = sys.argv[-1] if len(sys.argv) > 1 else "10.11.99.1"

EV_KEY = 0x01
EV_SYN = 0x00
SYN_REPORT = 0x00

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    def emit(type, code, value):
        s.sendall(struct.pack("IIi", type, code, value))

    def hook(event):
        print(event)
        if event.event_type == keyboard.KEY_DOWN:
            emit(EV_KEY, event.scan_code, 1)
        elif event.event_type == keyboard.KEY_UP:
            emit(EV_KEY, event.scan_code, 0)
        else:
            return
        emit(EV_SYN, SYN_REPORT, 0)

    s.connect((address, 65432))

    keyboard.hook(hook)
    keyboard.wait()
