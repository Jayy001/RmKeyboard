import struct
import uinput
import logging
import asyncio

from websockets.server import serve

logging.basicConfig(level=logging.DEBUG)

device = uinput.Device(
    [getattr(uinput, x) for x in dir(uinput) if x.startswith("KEY_")]
)
logging.debug(f"Using device events: {device._Device__events}")


async def inject(websocket):
    async for event in websocket:
        type_, code, value = struct.unpack("IIi", event)

        logging.debug(f"Emitting event: {(type_, code), value}")
        device.emit((type_, code), value, False)


async def main(address="0.0.0.0", port=8765):
    logging.debug("Attempting to start WebSocket")

    async with serve(inject, address, port):
        logging.info(f"WebSocket running: {address}, {port}")

        await asyncio.Future()


asyncio.run(main())
