<script lang="ts">
    import UWCSLogo from '../assets/uwcs.svelte';
    import { createEventDispatcher } from 'svelte';
    import { connectWebSocket } from './websocketService';

    let password = '';
    let shakePassword = false;
    const dispatch = createEventDispatcher();

    const handleLogin = async (event: Event) => {
        event.preventDefault();
        await connectWebSocket('ws://127.0.0.1:8000/admin', password).then(
            socket => dispatch('loginSuccess', { socket })
        ).catch( (error) => {
            if (error === "auth") {
                shakePassword = true; // Trigger shake animation
                setTimeout(() => { shakePassword = false; }, 500);
            } else {
                alert("Error Connecting to Server");
            }
        });
    };
</script>
<div id="login">
    <form id="login-form" on:submit={handleLogin}>
        <UWCSLogo/>
        <h2>Friday Night Gaming Admin Panel</h2>
        <input type="password" bind:value={password} placeholder="Password" name="password" required class:shake={shakePassword} />
        <button type="submit">Login</button>
    </form>
</div>
