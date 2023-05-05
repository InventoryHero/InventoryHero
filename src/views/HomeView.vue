<template>
  <h1 id="title" v-if="this.showTitle">Inventory Hero</h1>
  <h1 id="homeTitle" >Home</h1>
  <Slide @openMenu="this.showTitle=false" @closeMenu="this.showTitle=true" :crossIcon="false" :closeOnNavigation="true" enableOutsideClick>
    <a id="home" href="#">
      <span>Home</span>
    </a>
    <a href="">
      <span>
        Boxes
      </span>
    </a>
    <a href="">
      <span>
        Locations
      </span>
    </a>
    <a href="">
      <span>
        Products
      </span>
    </a>
  </Slide>

  <add-button />
  <qr-button />
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import { Slide } from 'vue3-burger-menu';

export default {
  name: 'App',
  components: {
    Slide,
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
#title {
  position: absolute;
  top: 15px;
  left: 50%;
  transform: translateX(-50%);
}
#homeTitle {
  position: absolute;
  top: 10vh;
  left: 50%;
  transform: translateX(-50%);
}

.bm-menu {
      background-color: rgb(0, 0, 0); /* Black*/
    }

.bm-burger-bars {
  background-color: white;
}
</style>
