import { sequence } from "@sveltejs/kit/hooks"
import { handle as handleAuth } from "$lib/server/auth"
import { useServer } from "vite-sveltekit-node-ws";
import { webSocketServer } from "$lib/server/websocket";

export const handle = sequence(handleAuth)

useServer(webSocketServer, (pathname: string) => {
    return pathname.startsWith('/ws')
})