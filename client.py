import sys
import struct
import socket
import keyboard
import time

import asyncio
import logging
from websockets.sync.client import connect

logging.basicConfig(level=logging.DEBUG)


def main(port=8765):
    address = sys.argv[-1] if len(sys.argv) > 1 else "10.11.99.1"

    EV_KEY = 0x01
    EV_SYN = 0x00
    SYN_REPORT = 0x00

    logging.info(f"Attempting to connect to {address}:{port}")
    with connect(f"ws://{address}:{port}") as websocket:
        logging.info(f"Connection sucessfull")

        def emit(type_, code, value):
            logging.debug(f"Sent event: {type_}, {code}, {value}")
            websocket.send(struct.pack("IIi", type_, code, value))

        def hook(event):
            logging.debug(
                "Caught event: {event.event_type}, {event.scan_code}, {event.name}"
            )
            if event.event_type == keyboard.KEY_DOWN:
                emit(EV_KEY, event.scan_code, 1)
            elif event.event_type == keyboard.KEY_UP:
                emit(EV_KEY, event.scan_code, 0)
            else:
                return

            emit(EV_SYN, SYN_REPORT, 0)

        keyboard.hook(hook)
        keyboard.wait()


if __name__ == "__main__":
    main()
