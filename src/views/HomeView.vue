<template>
  <div>
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
  
  
    <div id="posStarredMessages">
      <h3>⭐ Starred Products</h3>
      <list-container :list=this.starred_products />
    </div>
  
    <div id="posLastUsed">
      <h3>⏰ Last Used Products</h3>
      <list-container :list="[{name: 'Müssen wir noch'}, {name:'abklären, wie wir'}, {name: 'das machen wollen'}, {name: '😁'}]" />
    </div>
  
    <add-button @click="this.addModalVisibility = true"/>
    <qr-button />
  </div>

  <add-modal v-if="this.addModalVisibility" @closeModal="this.addModalVisibility = false;"/>

</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import ListContainer from '@/components/ListContainer.vue';
import AddModal from '@/modals/AddModal.vue'; 

import { Slide } from 'vue3-burger-menu';

import { DB_SB_getStarredProducts } from '@/db/supabase';

export default {
  name: 'App',
  components: {
    Slide,
    AddButton,
    QrButton,
    ListContainer,
    AddModal
  },
  data() {
    return {
      showTitle: true,
      starred_products: [],
      addModalVisibility: false
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
a:visited {
  color: white;
}
<style>
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
