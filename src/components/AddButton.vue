<template>
    <v-list-item density="compact" >
        <v-icon class="containerAddButton" size="x-large" icon="mdi-plus" />
    </v-list-item>
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
    position: fixed;
    right: 20px;
    bottom: 20px;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
    cursor: pointer;
}
</style>
  