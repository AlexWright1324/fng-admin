import { writable, type Writable } from "svelte/store"
import type { ServerWebSocket, WebSocketHandler } from "svelte-adapter-bun"

interface Computer {
  ws: ServerWebSocket<ServerData>
  commandLog: Writable<string>
}

interface ServerData {
  hostname: string
}

export const computers = new Map<string, Computer>()

export const handleWebSocket: WebSocketHandler<ServerData> = {
  open(ws) {
    const computer = computers.get(ws.data.hostname)
    if (computer) {
      return ws.close(0, "Connection established to hostname elsewhere")
    }

    computers.set(ws.data.hostname, { ws, commandLog: writable("") })
  },
  close(ws, code, message) {
      computers.delete(ws.data.hostname)
  },
  message(ws, message) {
    const computer = computers.get(ws.data.hostname)
    if (!computer) {
      return
    }
    try {
      const log = JSON.parse(message.toString())
      computer.commandLog.set(log.data.stdout + log.data.stderr)
    } catch (e) {}
  },
  upgrade(request, upgrade) {
    const url = new URL(request.url)
    if (!url.pathname.startsWith("/ws")) {
      return false
    }

    const hostname = url.searchParams.get("hostname")
    if (!hostname) {
      return false
    }

    return upgrade(request, {
      data: {
        hostname,
      },
    })
  },
}
