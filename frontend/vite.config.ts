import { sveltekit } from "@sveltejs/kit/vite"
import { defineConfig, type Plugin } from "vite"

const websocket = (): Plugin => ({
  name: "WebSocket Plugin",
  async configureServer(server) {
    const handleWebsocket = (await import("$lib/server/websocket")).handleWebSocket
    Bun.serve({
      port: server.config.server.port,
      fetch(request, newServer) {
        console.log("wtf")
        handleWebsocket.upgrade(request, newServer.upgrade.bind(server))
      },
      websocket: {
        open: handleWebsocket.open as any,
        close: handleWebsocket.close as any,
        message: handleWebsocket.message as any,
      },
    })
  },
})

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    watch: {
      ignored: ["**/.direnv**"],
    },
  },
})
