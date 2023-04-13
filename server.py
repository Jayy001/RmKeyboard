import struct
import uinput
import logging
import asyncio
import signal
import ssl
import websockets
import sys
import argparse


async def inject(websocket):
    token = await websocket.recv()

    if token != pwd:
        await websocket.close(1011, "Unauthorized (Wrong token)")
    else:
        await websocket.send("OK")

    try:
        async for event in websocket:
            type_, code, value = struct.unpack("IIi", bytes(event.encode("utf-8")))

            logging.debug(f"Emitting event: {(type_, code), value}")
            device.emit((type_, code), value, False)
    except websockets.exceptions.ConnectionClosed:
        logging.error("Client disconnected")


async def main():
    logging.debug("Attempting to start WebSocket")

    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    if ssl_check:
        logging.info("Using SSL")
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain("certs/cert.pem", keyfile="certs/key.pem")
    else:
        ssl_context = None

    async with websockets.serve(
        inject, address, port, ssl=ssl_context, compression=None
    ):
        logging.info(f"WebSocket running: {address}, {port}")

        await stop


parser = argparse.ArgumentParser(
    prog="RmKeyboard Server",
    description="RmKeyboard Server to recieve events from the client over a websocket and inject them into the virtual device",
    epilog="Example: python3 server.py Password",
)
parser.add_argument(
    "-a", "--address", help="The address to bind to [0.0.0.0]", default="0.0.0.0"
)
parser.add_argument(
    "-t",
    "--token",
    help="The token for the websocket server [Password]",
    default="Password",
)
parser.add_argument(
    "-p", "--port", help="The port for the websocket server [8765]", default=8765
)
parser.add_argument(
    "-s", "--secure", help="Use secure socket layer", action="store_true", default=False
)
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose logging"
)

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

pwd = args.token
address = args.address
port = args.port
ssl_check = args.secure

device = uinput.Device(
    [getattr(uinput, x) for x in dir(uinput) if x.startswith("KEY_")]
)
logging.debug(f"Using device events: {device._Device__events}")
logging.debug(f"Using token: {pwd}")

asyncio.run(main())
