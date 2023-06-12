<template>
  <SandwichMenu :title="this.title" />
  <BoxCard v-for="b in boxes" class="card" 
                      :key="b.id"
                      :id="b.id" 
                      :boxName="b.name" 
                      :numProducts="b.product_cnt" 
                      :numStarredProducts="b.starred_product_cnt" 
                      @boxDeleted="refreshData" />

  <add-modal  v-if="this.addModalVisibility"
              @closeModal="closeModal()"
              :preselected_box="this.preselectedBox" 
              :navbarItems="this.displayedNavbarItems" 
              :defaultAddView="Constants.BoxesView" />

  <load-animation v-if="this.loading"></load-animation>
  <add-button @click="this.addModalVisibility = true"/>
  <qr-button/>
</template>

<script>
import AddButton from '@/components/AddButton.vue'
import QrButton from '@/components/QrButton.vue'
import BoxCard from "@/components/BoxCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";
import LoadAnimation from "@/components/LoadAnimation.vue";

import {
  DB_SB_get_boxes,
  DB_SB_getStarredProducts,
  DB_SB_get_room,
  DB_SB_get_box_name
} from '@/db/supabase';
import { getUser } from "@/db/dexie";
import { Constants } from "@/global/constants";

import AddModal from "@/modals/AddModal.vue";



export default {
  name: 'App',
  props: {
    room_id: {
      type: Number,
      default: -1,
    }
  },
  components: {
    LoadAnimation,
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
          displayedNavbarItems: Constants.All,
          loading: true,
      }
  },
  methods: {
      refreshData()
      {
        this.get_boxes();
      },
      displayModal(id){
        DB_SB_get_box_name(id).then((box) => {
          this.preselectedBox = box;
          this.defaultModalView = Constants.ProductsView;
          this.displayedNavbarItems = [Constants.ProductsView];
          this.addModalVisibility = true;
        })
      },
      get_boxes() {
          DB_SB_get_boxes(this.currentUser.username, this.room_id).then((boxes) => {
              this.boxes = boxes;
              this.loading = false;
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
