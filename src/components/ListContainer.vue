<template>
    <div class="containerListContainer" :class="this.theme">
        <p v-for="l in this.list" :key=l.key> ○ &nbsp; {{ l.name }} </p>
    </div>
</template>

<script>
import {getSettings} from "@/db/dexie"

export default {
name: 'containerListContainer',
props: ["list"],
data() {
    return {
      theme: "",
    }
},
beforeMount()
{

    getSettings().then((settings) => {
        this.theme = settings.theme;
        console.log(this.theme);
    })
}
}

</script>

<style scoped>
.containerListContainer {
    margin-left: 10%;
    width: 80%;
    border-radius: 10px;
    padding: 10px 10px 10px 20px;
    text-align: left;
}

.light-theme  {
    background-color: var(--color-light-theme-darker);
}
.dark-theme  {
    background-color: var(--color-dark-theme-darker);
}

</style>
  
