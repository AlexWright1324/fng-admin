import type { LayoutServerLoad } from "./$types"
import { error } from "@sveltejs/kit"
import { computers as computerSet } from "$lib/server/websocket"

export const load: LayoutServerLoad = async ({ parent }) => {
	const { session } = await parent()

	const admin = session?.user?.groups?.includes("exec")

    if (!admin) {
        throw error(403, "Unauthorized")
    }

    const computers = Array.from(computerSet.keys())


    return {
        computers,
    }
}
