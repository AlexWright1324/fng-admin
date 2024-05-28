#!/usr/bin/env python

import uvloop
import asyncio
from os import getenv
from typing import Set
from websockets.server import serve, WebSocketServerProtocol as WSSP

import admin
import client


async def handler(websocket: WSSP) -> None:
    match websocket.path:
        case "/admin":
            await admin.login(websocket, PASSWORD, clients, admins)
        case "/client":
            await client.client(websocket, clients, admins)
        case _:
            pass


async def main():
    async with serve(handler, "localhost", 8000):
        await asyncio.Future()

PASSWORD = getenv("PASSWORD")
clients: Set[client.Client] = set()
admins: Set[admin.Admin] = set()

if __name__ == "__main__":
    if PASSWORD is None:
        print("PASSWORD variable not defined")
        exit()

    uvloop.run(main())
