import { WebSocketServer, WebSocket } from "ws";
import { writable, type Writable } from "svelte/store";

interface Computer {
    webSocket: WebSocket;
    log: Writable<string>;
}

export const computers = new Map<string, Computer>()

export const webSocketServer = (server) => {
    const webSocketServer = new WebSocketServer({ server });

    webSocketServer.on("connection", (socket, request) => {
        // Janky way to get the hostname
        const url = new URL(`http://127.0.0.1/${request.url ? request.url : ""}`);

        const hostname = url.searchParams.get("hostname");
        if (!hostname) {
            console.log("NO")
            socket.close(3000, "No hostname");
            return;
        }

        computers.get(hostname)?.webSocket.close(3000, "New connection established elsewhere");
        computers.set(hostname, { webSocket: socket, log: writable("") });

        console.log(`${hostname} connected`)

        socket.on("message", (data, isBinary) => {
            const computer = computers.get(hostname);
            if (!computer) {
                return;
            }
            try {
                const log = JSON.parse(data.toString());
                computer.log.set(log.data.stdout + log.data.stderr);
            } catch (e) {
            }
        });

        socket.on("close", () => {
            console.log(`${hostname} disconnected`);
            computers.delete(hostname);
        });
    });
}