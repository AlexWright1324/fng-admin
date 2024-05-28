#!/usr/bin/env python

import json
from typing import Set
from json import JSONDecodeError
from websockets import broadcast
from dataclasses import dataclass
from marshmallow import ValidationError
from dataclasses_json import dataclass_json
from websockets.server import WebSocketServerProtocol as WSSP


@dataclass(unsafe_hash=True)
class Admin:
    websocket: WSSP


@dataclass_json
@dataclass
class AdminFirstMessage:
    password: str

@dataclass_json
@dataclass
class Type:
    type: str
    data: dict


async def updateAdmins(clients: Set, admins: Set[Admin]):
    admin_websockets = (admin.websocket for admin in admins)
    message = {
        "clients": [{"name": client.hostname} for client in clients]
    }
    broadcast(admin_websockets, json.dumps(message))


async def login(websocket: WSSP, PASSWORD: str, clients: Set, admins: Set[Admin]):
    try:
        msg = AdminFirstMessage.schema().loads(await websocket.recv())
    except JSONDecodeError:
        return
    except ValidationError:
        return

    if msg.password == PASSWORD:
        await websocket.send(json.dumps({
            "auth": "success"
        }))
    else:
        await websocket.send(json.dumps({
            "auth": "failure"
        }))
        return

    admin = Admin(websocket)

    try:
        admins.add(admin)

        await updateAdmins(clients, admins)

        async for message in websocket:
            try:
                msg = Type.schema().loads(message)
            except Exception as e:
                print(e)
                continue

            if msg.type == "logout":
                name = msg.data.get("name")
                force = msg.data.get("force")
                if force is None:
                    force = False
                for client in clients:
                    if client.hostname == name:
                        await client.websocket.send(json.dumps({
                            "type": "logout",
                            "force": force
                        }))
                        break

    finally:
        admins.remove(admin)
