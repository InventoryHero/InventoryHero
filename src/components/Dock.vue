<template>
  <div id="dock" class="d-flex justify-space-evenly">
    <v-list-item class="button" @click="this.$emit('addButton')" density="compact" >
      <v-icon  size="x-large" icon="mdi-plus" />
    </v-list-item>
    <v-list-item v-if="this.show_qr" class="button" @click="this.$emit('qrButton')" density="compact" >
      <v-icon  size="x-large" icon="fa:fas fa-qrcode" />
    </v-list-item>
  </div>
</template>

<script>
export default {
  name: 'App',
  props: {
    show_qr: {
      type: Boolean,
      default: true,
    },
  }
}
</script>

<style scoped>
#dock{
    position: fixed;
    bottom: 10px;
    left: 0;
    width: 100%;
    height: 50px;
    z-index: 999;
}
.button{
    height: 50px;
    border-radius: 10px;
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
    cursor: pointer;
}
</style>