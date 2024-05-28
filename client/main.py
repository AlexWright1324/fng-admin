#!/usr/bin/env python

from dbus_next.aio import MessageBus
import json
import asyncio
import platform
import websockets
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Type:
    type: str
    force: bool


async def logout(force: bool):
    try:
        bus = await MessageBus().connect()
        if force:
            introspection = await bus.introspect('org.kde.Shutdown', '/Shutdown')
            ksmserver = bus.get_proxy_object('org.kde.Shutdown', '/Shutdown', introspection)
            interface = ksmserver.get_interface('org.kde.Shutdown')
            await interface.call_logout()
        else:
            introspection = await bus.introspect('org.kde.LogoutPrompt', '/LogoutPrompt')
            ksmserver = bus.get_proxy_object('org.kde.LogoutPrompt', '/LogoutPrompt', introspection)
            interface = ksmserver.get_interface('org.kde.LogoutPrompt')
            await interface.call_prompt_logout()
    except Exception as e:
        print(f"An error occurred: {e}")


async def main():
    uri = "ws://localhost:8000/client"
    async with websockets.connect(uri) as websocket:

        # First Message
        msg = {"hostname": platform.node()}
        await websocket.send(json.dumps(msg))

        async for message in websocket:
            msg = Type.schema().loads(message)
            if msg.type == "logout":
                await logout(False)

if __name__ == "__main__":
    asyncio.run(main())
