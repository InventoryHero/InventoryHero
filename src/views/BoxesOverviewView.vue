<template>
  <SandwichMenu :title="this.title"/>
  <v-virtual-scroll
      class="virtual-scroll-bg"
      :height="80+'vh'"
      :items="boxes"
  >
      <template v-slot:default="{ item }">
          <BoxCard @addItemToBox="displayModal"  class="card" :id="item.id" :boxName="item.name" :numProducts="item.product_cnt" :numStarredProducts="item.starred_product_cnt"/>
      </template>
  </v-virtual-scroll>
  <add-modal :preselected_box="this.preselectedBox" :navbarItems="this.displayedNavbarItems" :defaultAddView="Constants.BoxesView" v-if="this.addModalVisibility" @closeModal="closeModal()"/>
  <add-button @click="this.addModalVisibility = true"/>
  <qr-button/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import BoxCard from "@/components/BoxCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";

import {
  DB_SB_get_boxes,
  DB_SB_getStarredProducts,
  DB_SB_get_room,
  DB_SB_get_box_name
} from '@/db/supabase';
import {getUser} from "@/db/dexie";
import AddModal from "@/modals/AddModal.vue";
import { Constants } from "@/global/constants";


export default {
  name: 'App',
  props: {
    room_id: {
      type: Number,
      default: -1,
    }
  },
  components: {
      AddModal,
      BoxCard,
      AddButton,
      QrButton,
      SandwichMenu
  },
  data() {
      return {
          boxes: [],
          currentUser: "",
          addModalVisibility: false,
          Constants,
          title: "Boxes",
          preselectedBox: "",
          displayedNavbarItems: Constants.All
      }
  },
  methods: {
      displayModal(id){
        DB_SB_get_box_name(id).then((box) => {
          console.log(box);
          this.preselectedBox = box;
          this.defaultModalView = Constants.ProductsView;
          this.displayedNavbarItems = [Constants.ProductsView];
          this.addModalVisibility = true;
        })
      },
      get_boxes() {
          DB_SB_get_boxes(this.currentUser.username, this.room_id).then((boxes) => {
              this.boxes = boxes;
          });
      },
      closeModal() {
        this.addModalVisibility = false;
        this.defaultModalView = Constants.BoxesView;
        this.displayedNavbarItems = Constants.All;
        this.preselectedBox = "";
        this.get_boxes();
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
          if(this.room_id !== -1)
          {
            DB_SB_get_room(this.room_id, user).then((room) => {
              if(room.length !== 0)
                this.title = "Boxes in " + room[0].name;
            });
          }

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
