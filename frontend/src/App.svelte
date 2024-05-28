<script lang="ts">
  import { slide } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import Login from './lib/Login.svelte';

  let authenticated = false;
  let socket: WebSocket;
  let clients: any[] = [];

  const handleLoginSuccess = (event: CustomEvent) => {
    socket = event.detail.socket;
    socket.addEventListener('close', handleSocketClose);
    socket.addEventListener('message', handleSocketMessage);
    authenticated = true;
  };

  const handleSocketClose = () => {
    authenticated = false;
  };

  const handleSocketMessage = (event: MessageEvent) => {
    const json = JSON.parse(event.data);
    clients = json.clients;
  };

  let selected = "";

  const handleLogout = (force: boolean) => {
    socket.send(JSON.stringify({"type": "logout", "data": {"name": selected, "force": force}}));
  };

  const handleSendCommand = () => {
    console.log("Send Command button clicked");
    // Implement send command logic here
  };

  const select = (name: string) => {
    if (selected === name) {
      selected = "";
    } else {
      selected = name;
    }
  }
</script>

{#if authenticated}
  <main>
    <div id="computers">
      <h2>Computers</h2>
      <ul>
        {#each clients as client}
          <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <li class:selected={selected === client.name} on:click={()=>select(client.name)}>
            <img src="/" alt="">
            <p>{client.name}</p>

          </li>
        {:else}
          <li>No computers online...</li>
        {/each}
      </ul>
    </div>
    {#if selected != ""}
    <div id="sidebar" transition:slide={{ duration: 500, easing: quintOut, axis: 'x' }}>
      <ul>
        <li><button on:click={()=>handleLogout(false)}>Logout</button></li>
        <li><button on:click={()=>handleLogout(true)}>Force Logout</button></li>
        <li><button on:click={handleSendCommand}>Send Command</button></li>
    </ul>
    </div>
    {/if}
  </main>
{:else}
  <Login on:loginSuccess={handleLoginSuccess} />
{/if}
