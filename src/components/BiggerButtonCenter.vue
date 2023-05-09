<template>
    <div id="containerBiggerButton">
        <p>{{ this.text }}</p>
    </div>
</template>

<script>

export default {
name: 'containerAddButton',
props: ["text"],
components: {
}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#containerBiggerButton{ 
    margin-top: 20px;
    margin-left: 10%;
    width: 80%;
    border-radius: 10px;
    padding: 10px 0px 10px 0px;
    background-color: var(--color-darker);
    cursor: pointer;
}
</style>
  