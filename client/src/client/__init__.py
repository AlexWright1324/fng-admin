#!/usr/bin/env python

import os
import asyncio
import platform
from dbus_next.aio import MessageBus
from typing import Optional
from websockets.asyncio.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosed
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Message:
    command: str
    data: Optional[dict] = None


async def logout(data: dict[str, any]):
    force = data.get("force", False)
    try:
        bus = await MessageBus().connect()
        if force:
            introspection = await bus.introspect("org.kde.Shutdown", "/Shutdown")
            ksmserver = bus.get_proxy_object(
                "org.kde.Shutdown", "/Shutdown", introspection
            )
            interface = ksmserver.get_interface("org.kde.Shutdown")
            await interface.call_logout()
        else:
            introspection = await bus.introspect(
                "org.kde.LogoutPrompt", "/LogoutPrompt"
            )
            ksmserver = bus.get_proxy_object(
                "org.kde.LogoutPrompt", "/LogoutPrompt", introspection
            )
            interface = ksmserver.get_interface("org.kde.LogoutPrompt")
            await interface.call_prompt_logout()
    except Exception as e:
        print(f"An error occurred while logging out: {e}")


async def command(websocket: ClientConnection, data: dict[str, any]):
    command = data.get("command")
    if command is None:
        return
    proc = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    await websocket.send(
        Message(command=command, data={"stdout": stdout.decode(), "stderr": stderr.decode()}).to_json()
    )


async def main():
    if os.getenv("DEV"):
        uri = "ws://localhost:5173/ws"
    else:
        uri = "wss://fng-admin.containers.uwcs.co.uk/ws"
    uri += f"?hostname={platform.node()}"
    msgSchema = Message.schema()
    print(f"Connecting to {uri} ...")
    while True:
        try:
            async with connect(uri) as websocket:
                print("Connected!")
                async for message in websocket:
                    try:
                        msg: Message = msgSchema.loads(message)
                    except Exception as e:
                        print(f"An error occurred while parsing message: {e}")
                        continue

                    match msg.command:
                        case "logout":
                            await logout(msg.data)
                        case "command":
                            await command(websocket, msg.data)
        except ConnectionClosed as e:
            print(f"Code {e.code}, waiting for 5 seconds before retrying...")
            await asyncio.sleep(5)
        except Exception as e:
            #print(f"An error occurred: {e}")
            print("Waiting for 5 seconds before retrying...")
            await asyncio.sleep(5)
