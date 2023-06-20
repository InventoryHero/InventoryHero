<template>
    <div id="containerTag" :class="this.active">
        <p class="text-center i-mog-nerma">{{ this.text }}</p>
    </div>
</template>

<script>

export default {
name: 'containerAddButton',
props: ["text", "active"],
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#containerTag{
    margin-right: 20px;
    border: 1px solid white;
    padding: 5px;
    border-radius: 100px;
    width: 20vw;
    max-width: 20vw;

    cursor: pointer;
}

.i-mog-nerma{
    color: white !important;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}

.true {
    background-color: var(--color-dark-theme-lighter);
}
</style>
  