import { computers } from '$lib/server/websocket'

export const actions = {
    logoutAll: async ({ request }) => {
        const formData = await request.formData()
        const force = formData.get("force") ? true : false

        computers.forEach((computer) => {
            computer.ws.send(JSON.stringify(
                {
                    command: "logout",
                    data: {
                        force,
                    },
                }
            ))
        })
    },
}