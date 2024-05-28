#!/usr/bin/env python

from typing import Set
from json import JSONDecodeError
from dataclasses import dataclass
from marshmallow import ValidationError
from dataclasses_json import dataclass_json
from websockets.server import WebSocketServerProtocol as WSSP

from admin import updateAdmins


@dataclass(unsafe_hash=True)
class Client:
    hostname: str
    websocket: WSSP


@dataclass_json
@dataclass
class ClientFirstMessage:
    hostname: str


async def client(websocket: WSSP, clients: Set[Client], admins: Set):
    try:
        msg = ClientFirstMessage.schema().loads(await websocket.recv())
    except JSONDecodeError:
        return
    except ValidationError:
        return
    try:
        client = Client(msg.hostname, websocket)
        clients.add(client)
        await updateAdmins(clients, admins)

        async for message in websocket:
            pass

    finally:
        clients.remove(client)
        await updateAdmins(clients, admins)
