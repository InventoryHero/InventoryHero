<template>
  <SandwichMenu/>
  <v-virtual-scroll
      class="virtual-scroll-bg"
      :height="80+'vh'"
      :items="boxes"
  >
      <template v-slot:default="{ item }">
          <BoxCard class="card" :id="item.id" :boxName="item.name" :numProducts="item.product_cnt" :numStarredProducts="item.starred_product_cnt"/>
      </template>
  </v-virtual-scroll>
  <add-button/>
  <qr-button/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import BoxCard from "@/components/BoxCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";

import { DB_SB_get_boxes } from '@/db/supabase';
import {getUser} from "@/db/dexie";


export default {
  name: 'App',
  components: {
      BoxCard,
      AddButton,
      QrButton,
      SandwichMenu
  },
  data() {
      return {
          boxes: [],
          currentUser: "",
      }
  },
  methods: {
      get_boxes() {
          DB_SB_get_boxes(this.currentUser.username).then((boxes) => {
              this.boxes = boxes;
          });
      }
  },
  beforeMount() {

      getUser().then((user) => {
          if(user === undefined)
          {
              this.$router.push("/login");
          }
          this.currentUser = user;
          this.get_boxes();
      });
  }

}
</script>

<style scoped>
  .card {
      padding-left: 2.5%;
      padding-right: 2.5%;
  }
  .v-virtual-scroll{
      background: var(--color-blue);
  }
  ::-webkit-scrollbar { width: 0px;  }
</style>
