import { computers } from '$lib/server/websocket'

export const actions = {
    logout: async ({ request, params }) => {
        const formData = await request.formData()
        const force = formData.get("force") ? true : false

        computers.get(params.hostname)?.ws.send(JSON.stringify(
            {
                command: "logout",
                data: {
                    force,
                },
            }
        ))
    },
    command: async ({ request, params }) => {
        const formData = await request.formData()
        const command = formData.get("command")

        computers.get(params.hostname)?.ws.send(JSON.stringify(
            {
                command: "command",
                data: {
                    command,
                },
            }
        ))
    },
}