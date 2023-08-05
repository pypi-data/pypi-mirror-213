import _toori

import urllib
import socket
import asyncio
import socketio
from concurrent.futures import ThreadPoolExecutor

# Increase the packet buffer
from engineio.payload import Payload

Payload.max_decode_packets = 2500000

_executor = ThreadPoolExecutor(1)

sio = socketio.AsyncClient()

loop = asyncio.get_event_loop()

LOCAL_IP = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

def resolve_address(address):
    hostname = address.split("//")[-1:][0]
    ip = socket.gethostbyname(hostname)

    return ip


@sio.on("message")
async def print_message(msg):
    print(msg)


@sio.on("connect")
async def on_connect():
    print("Connected to server")


@sio.on("in")
async def handle_incoming(data):
    # await loop.run_in_executor(_executor, _toori.inj, data)
    _toori.inj(data)
    # await asyncio.sleep(0.0)


async def start_client(address, requested_ip, filter_string):
    headers = {"req_ip": requested_ip, "loc_ip": LOCAL_IP}

    try:
        await sio.connect(f"{address}", auth=headers)
    except socketio.exceptions.ConnectionError:
        print(f"Unable to connect to the address {address}")
        exit()

    _toori.init(
        filter_string,
        LOCAL_IP,
    )

    while True:
        data = await loop.run_in_executor(_executor, _toori.get)
        # data = _toori.get()
        if len(data) > 0:
            try:
                await sio.emit(event="out", data=data)
            except Exception:
                pass

        # await asyncio.sleep(0.0001)


def start(address, filter_string=None, requested_ip=None, no_dns=False):
    parsed_url = urllib.parse.urlparse(address)
    server_port = parsed_url.port

    # Derive port if not explicitly stated in url
    if not server_port:
        if parsed_url.scheme == "http":
            server_port = 80
        else:
            server_port = 443

    base_filter = f"outbound && !loopback"

    # Whitelist encapsulated tunnel traffic from being intercepted by WinDivert
    base_filter += f" && (ip.DstAddr != {resolve_address(address)} || tcp.DstPort != {server_port})"

    if filter_string is None:
        filter_string = f"ip"

    if no_dns:
        filter_string += f" && (!udp || udp.DstPort != 53)"

    try:
        loop.run_until_complete(start_client(address, requested_ip, f"{base_filter} && {filter_string}"))
    except KeyboardInterrupt:
        _toori.stop()
        print("Exited, have a nice day :)")
