<template>
    <div class="containerAddButton">
        <svg xmlns="http://www.w3.org/2000/svg" fill="white" height="48" viewBox="0 96 960 960" width="48"><path d="M450 856V606H200v-60h250V296h60v250h250v60H510v250h-60Z"/></svg>
    </div>
</template>

<script>

export default {
name: 'containerAddButton',
components: {
}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.containerAddButton{ 
    position: absolute;
    right: 20px;
    bottom: 20px;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    background-color: var(--color-darker);
}
</style>
  