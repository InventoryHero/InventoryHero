<template>
  <h1 id="homeTitle" >Home</h1>

  <div id="posStarredMessages">
    <h3>⭐ Starred Products</h3>
    <list-container :list=this.starred_products />
  </div>

  <div id="posLastUsed">
    <h3>⏰ Last Used Products</h3>
    <list-container :list="[{name: 'Müssen wir noch'}, {name:'abklären, wie wir'}, {name: 'das machen wollen'}, {name: '😁'}]" />
  </div>

  <SandwichMenu/>
  <add-button />
  <qr-button @click="this.openMenu()"/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import SandwichMenu from "@/components/SandwichMenu.vue";
import ListContainer from '@/components/ListContainer.vue';

import { DB_SB_getStarredProducts } from '@/db/supabase';

export default {
  name: 'App',
  components: {
    SandwichMenu,
    AddButton,
    QrButton,
    ListContainer
  },
  data() {
    return {
      showTitle: true,
      starred_products: [],
    }
  },
  methods: {
    openMenu() {
      console.log("open me")
    },
  },
  beforeMount() {
    DB_SB_getStarredProducts().then((res) => {
      this.starred_products = res;
    })
  }
}
</script>

<style>
a:visited {
  color: white;
}

#title {
  position: absolute;
  top: 3.8vh;
  left: 30vw;
  font-size: 1.5em;
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

#posStarredMessages {
  margin-top: 20vh;
  width: 100%;
}

#posLastUsed {
  margin-top: 5vh;
}

h3 {
  text-align: left;
  margin-left: 10%;
}
</style>
