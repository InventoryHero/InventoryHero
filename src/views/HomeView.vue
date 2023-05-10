<template>
  <div id="posStarredMessages">
    <h3>⭐ Starred Products</h3>
    <list-container :list=this.starred_products />
  </div>

    <div id="posLastUsed">
      <h3>⏰ Last Used Products</h3>
      <list-container :list="[{name: 'Müssen wir noch'}, {name:'abklären, wie wir'}, {name: 'das machen wollen'}, {name: '😁'}]" />
    </div>
    

  <add-modal v-if="this.addModalVisibility" @closeModal="this.addModalVisibility = false;"/>

  <add-button @click="this.addModalVisibility = true"/>
  <qr-button />
  <SandwichMenu title="Home"/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import SandwichMenu from "@/components/SandwichMenu.vue";
import ListContainer from '@/components/ListContainer.vue';
import AddModal from '@/modals/AddModal.vue'; 

import { Slide } from 'vue3-burger-menu';

import { DB_SB_getStarredProducts } from '@/db/supabase';

export default {
  name: 'App',
  components: {
    SandwichMenu,
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

<style scoped>
a:visited {
  color: white;
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
