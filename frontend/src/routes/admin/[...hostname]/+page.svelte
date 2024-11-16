<script lang="ts">
    import { enhance } from "$app/forms";
    import { page } from "$app/stores";
    import { source } from "sveltekit-sse";
    import { Xterm, XtermAddon } from "@battlefieldduck/xterm-svelte";

    const log = source($page.url.pathname).select("log");

    import type {
        ITerminalOptions,
        ITerminalInitOnlyOptions,
        Terminal,
    } from "@battlefieldduck/xterm-svelte";

    let options: ITerminalOptions & ITerminalInitOnlyOptions = {
        cursorBlink: false,
        convertEol: true,
    };

    async function onLoad(terminal: Terminal) {
        const fitAddon = new (await XtermAddon.FitAddon()).FitAddon();
        terminal.loadAddon(fitAddon);
        fitAddon.fit();
        log.subscribe((data) => {
            terminal.write(data);
        });
    }
</script>

<h1>{$page.params.hostname}</h1>
<form action="?/logout" method="post" use:enhance>
    <label>
        <span>Force</span>
        <input type="checkbox" name="force" />
    </label>
    <button class="app-btn" type="submit">Logout</button>
</form>

<Xterm {options} {onLoad} />

<form action="?/command" method="post" use:enhance>
    <label>
        <span>Command</span>
        <input type="text" name="command" />
    </label>
    <button class="app-btn" type="submit">Enter</button>
</form>
