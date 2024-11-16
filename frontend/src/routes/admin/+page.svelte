<script lang="ts">
    import type { PageData } from "./$types";
    let { data }: { data: PageData } = $props();
</script>

<h1>Computers</h1>
<form action="?/logoutAll" method="post">
    <label >
        <span>Force</span>
        <input type="checkbox" name="force">
    </label>
    <button class="app-btn" type="submit">Logout all</button>
</form>
{#each data.computers as computer}
    <a class="app-btn" href="/admin/{computer}">{computer}</a>
{/each}
