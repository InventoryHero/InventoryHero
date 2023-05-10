<template>
<div class="containerListContainer">
    <p v-for="l in this.list" :key=l.key> ○ &nbsp; {{ l.name }} </p>
</div>
</template>

<script>
export default {
name: 'containerListContainer',
props: ["list"]};
</script>

<style scoped>
.containerListContainer {
    margin-left: 10%;
    width: 80%;
    background-color: var(--color-darker-back);
    border-radius: 10px;
    padding: 10px 10px 10px 20px;
    text-align: left;
}

</style>
  
  