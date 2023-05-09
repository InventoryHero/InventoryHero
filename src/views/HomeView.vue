<template>
  <SandwichMenu/>
  <add-button />
  <qr-button />
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import SandwichMenu from "@/components/SandwichMenu.vue";

export default {
  name: 'App',
  components: {
    SandwichMenu,
    AddButton,
    QrButton
  },
  data() {
    return {
      showTitle: true,
    }
  },
  methods: {
    openMenu() {
      console.log("open me")
    },
  }
}
</script>
a:visited {
  color: white;
}
<style>

</style>
