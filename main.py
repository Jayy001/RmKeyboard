import socket
import struct
import uinput

device = uinput.Device(
    [getattr(uinput, x) for x in dir(uinput) if x.startswith("KEY_")]
)
size = struct.calcsize("IIi")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("0.0.0.0", 65432))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(size)
                if not data:
                    break

                type, code, value = struct.unpack("IIi", data)
                print(
                    (
                        type,
                        code,
                        value,
                    )
                )
                device.emit((type, code), value, False)
