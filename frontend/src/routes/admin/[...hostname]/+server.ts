import { computers } from '$lib/server/websocket.js'
import { produce, type Unsafe } from 'sveltekit-sse'
import { get } from 'svelte/store'

export const POST = ({ params }) => {
    return produce(async function start({ emit, lock }) {
        await new Promise(async function start(resolve) {
            const computer = computers.get(params.hostname)
            if (!computer) {
                return
            }
            computer.commandLog.subscribe(async (data) => {
                const { error } = emit("log", data)
                if (error) {
                    resolve(error)
                }
            })
        })
        return function stop() {
        }
    },{
        ping: 100,
        stop() {
        }
    })
}