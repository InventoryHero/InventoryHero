<template>

  <SandwichMenu v-if="!this.from_qrcode" :title="this.title"/>
  <div :style="this.styling">
    <search-bar :do_transform="this.from_qrcode ? '' : 'transform'" @valueUpdated="sortBoxes"/>
    <box-card v-for="b in boxes" class="card"
                        :key="b.id"
                        :id="b.id"
                        :boxName="b.name"
                        :numProducts="b.product_cnt"
                        :numStarredProducts="b.starred_product_cnt"
                        @boxDeleted="get_boxes"
                        @addItemToBox="displayModal"
    />
  </div>
  <add-modal  v-model="this.addModalVisibility"
              @closeModal="closeModal()"
              :preselected_box="this.preselectedBox" 
              :navbarItems="this.displayedNavbarItems" 
              :defaultAddView="Constants.BoxesView" />

  <load-animation v-if="this.loading"></load-animation>
  <div v-if="!this.from_qrcode" id="spacing"></div>
  <dock
          @qrButton="this.qrReaderModalVisibility=true"
          @addButton="this.addModalVisibility = true"
          v-if="!this.from_qrcode"
  />
</template>

<script>
import BoxCard from "@/components/BoxCard.vue";
import SandwichMenu from "@/components/SandwichMenu.vue";
import LoadAnimation from "@/components/LoadAnimation.vue";
import SearchBar from '@/components/SearchBar.vue';
import Dock from "@/components/Dock.vue";


import AddModal from "@/modals/AddModal.vue";


import {
  DB_SB_get_boxes,
  DB_SB_getStarredProducts,
  DB_SB_get_room,
  DB_SB_get_box_name
} from '@/db/supabase';
import { getUser } from "@/db/dexie";
import { Constants } from "@/global/constants";
import { rankBoxesBySearch } from "@/scripts/sort";





export default {
  name: 'App',
  props: {
    room_id: {
      type: Number,
      default: -1,
    },
    from_qrcode: {
      type: Boolean,
      default: false
    },
    styling: {
      type: String,
      default: "",
    }
  },
  components: {
    LoadAnimation,
    AddModal,
    BoxCard,
    SandwichMenu,
    SearchBar,
    Dock
  },
  data() {
      return {
          boxes: [],
          currentUser: "",
          addModalVisibility: false,
          qrReaderModalVisibility: false,
          Constants,
          title: "Boxes",
          preselectedBox: "",
          displayedNavbarItems: Constants.All,
          loading: true,
      }
  },
  methods: {
      displayModal(id){
        DB_SB_get_box_name(id).then((box) => {
          this.preselectedBox = box;
          this.defaultModalView = Constants.ProductsView;
          this.displayedNavbarItems = [Constants.ProductsView];
          this.addModalVisibility = true;
        })
      },
      async get_boxes() {
          const boxes = await DB_SB_get_boxes(this.currentUser.username, this.room_id);
          this.boxes = rankBoxesBySearch(boxes, "");
          this.loading = false;
          return boxes
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
      async sortBoxes(search_word) {
        const boxes = await this.get_boxes();
        this.boxes = rankBoxesBySearch(boxes, search_word);
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
  #spacing{
      height: calc(5vh + 25px);
  }

  ::-webkit-scrollbar { width: 0px;  }
</style>
