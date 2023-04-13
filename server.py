import struct
import uinput

import asyncio
from websockets.server import serve

device = uinput.Device(
    [getattr(uinput, x) for x in dir(uinput) if x.startswith("KEY_")]
)
size = struct.calcsize("IIi")

async def inject(websocket):
    async for event in websocket:
        type_, code, value = struct.unpack("IIi", event)
        
        device.emit((type_, code), value, False)

async def main():
    async with serve(inject, "0.0.0.0", 8765):
        print('WebSocket running')

        await asyncio.Future() 

asyncio.run(main())

