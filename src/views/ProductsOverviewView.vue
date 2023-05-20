<template>
  <SandwichMenu/>
  <v-virtual-scroll
      class="virtual-scroll-bg"
      :height="80+'vh'"
      :items="products"
  >
      <template v-slot:default="{ item }">
          <ProductsCard class="card" :id="item.id" :productName="item.name" :amount="item.amount"/>
      </template>
  </v-virtual-scroll>
    <add-modal :defaultAddView="Constants.ProductsView" v-if="this.addModalVisibility" @closeModal="closeModal()"/>
    <add-button @click="this.addModalVisibility = true"/>
  <qr-button/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import ProductsCard from "@/components/ProductsCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";

import {DB_SB_get_all_products, DB_SB_getStarredProducts} from '@/db/supabase';
import {getUser} from "@/db/dexie";
import AddModal from "@/modals/AddModal.vue";
import { Constants } from "@/global/constants";


export default {
  name: 'App',
  components: {
      AddModal,
    ProductsCard,
      AddButton,
      QrButton,
      SandwichMenu
  },
  data() {
      return {
          products: [],
          currentUser: "",
          addModalVisibility: false,
          Constants
      }
  },
  methods: {
      get_boxes() {
        DB_SB_get_all_products(this.currentUser.username).then((products) => {
              this.products = products;
              console.log(this.products);
              
          });
      },
      closeModal() {
          this.addModalVisibility = false;
          DB_SB_getStarredProducts().then((res) => {
              this.starred_products = res;
          })
      },
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