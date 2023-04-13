import struct
import keyboard
import logging
import ssl
import websocket
import sys
import argparse
import rel
import sys


def hook(event):
    logging.debug(f"Caught event: {event.event_type}, {event.scan_code}, {event.name}")
    if event.event_type == keyboard.KEY_DOWN:
        emit(EV_KEY, event.scan_code, 1)
    elif event.event_type == keyboard.KEY_UP:
        emit(EV_KEY, event.scan_code, 0)
    else:
        return
    emit(EV_SYN, SYN_REPORT, 0)


def emit(type_, code, value):
    logging.debug(f"Sent event: {type_}, {code}, {value}")
    wsapp.send(struct.pack("IIi", type_, code, value))


def on_open(wsapp):
    logging.info(f"Authenticating with: {token}")
    wsapp.send(token)


def on_message(wsapp, message):
    if message == "OK":
        logging.info("Authentication successful")
        keyboard.hook(hook)
    else:
        logging.debug(f"Message recieved: {message}")


def on_close(wsapp, close_status_code, close_msg):
    logging.error(f"WebSocket closed: [{close_status_code}] {close_msg}")
    rel.abort()
    exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="RmKeyboard Client",
        description="Basic WebSocket client for the RmKeyboard server",
        epilog="Example: python3 client.py 10.11.99.1 password",
    )
    parser.add_argument(
        "-a",
        "--address",
        help="The address of the websocket server [10.11.99.1]",
        default="10.11.99.1",
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
        "-s",
        "--secure",
        help="Use secure socket layer",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    address = args.address
    port = args.port
    token = args.token

    sslopt = {}
    if args.secure:
        logging.info("Using SSL")

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.load_verify_locations("certs/cert.pem")
        sslopt["context"] = ssl_context

        protocol = "wss"
    else:
        protocol = "ws"

    EV_KEY = 0x01
    EV_SYN = 0x00
    SYN_REPORT = 0x00

    wsapp = websocket.WebSocketApp(
        f"{protocol}://{address}:{port}",
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
    )

    logging.info(f"Attempting to connect to {address}:{port}")
    wsapp.run_forever(sslopt=sslopt, dispatcher=rel)

    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
