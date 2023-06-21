<template>


  <SandwichMenu v-if="!this.from_qrcode" :title="this.title" @reloadboxes="reloadMe"/>
  <div class="scrollableDiv">
    <search-bar :do_transform="this.from_qrcode ? '' : 'transform'" @valueUpdated="sortBoxes"/>
    <load-animation v-if="this.loading"></load-animation>
    <box-card v-for="b in boxes" class="card"
        :key="b.id"
        :id="b.id"
        :boxName="b.name"
        :numProducts="b.product_cnt"
        :numStarredProducts="b.starred_product_cnt"
        @boxDeleted="get_boxes"
        @addItemToBox="displayModal"
        @refreshData="get_boxes"
    />
    <div :id="this.styling"></div>

  </div>

  <add-modal
      @closeModal="closeModal()"
      v-bind:preselected_box="this.preselectedBox"
      :navbarItems="this.displayedNavbarItems"
      :defaultAddView="this.defaultModalView"
      v-model="this.addModalVisibility"
      :data_changed="this.data_changed"
      @initAck="this.data_changed=false"
  />

  <dock
          :show_qr="false"
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


import {DB_SB_get_box_name, DB_SB_get_boxes, DB_SB_get_room, DB_SB_getStarredProducts} from '@/db/supabase';
import {getSettings, getUser} from "@/db/dexie";
import {Constants} from "@/global/constants";
import {rankBoxesBySearch} from "@/scripts/sort";
import QrDataModal from "@/modals/QrDataModal.vue";
import QrReaderModal from "@/modals/QrReaderModal.vue";
import {useToast} from "vue-toastification";



export default {
  name: 'App',

  props: {
    roomid: {
      type: Number,
      default: -1,
    },
    from_qrcode: {
      type: Boolean,
      default: false
    },
    styling: {
      type: String,
      default: "cardScrollSpacingOverview",
    }
  },
  components: {
    QrReaderModal, QrDataModal,
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
          Constants,
          title: "Boxes",
          preselectedBox: {id: -1, name: this.$t('add_modal.box_placeholder')},
          displayedNavbarItems: Constants.All,
          defaultModalView: Constants.BoxesView,
          loading: true,
          room_id: -1,
          theme: "",
          data_changed: false,
      }
  },
  methods: {
      async reloadMe()
      {
        this.room_id = -1;
        this.title = this.$t('boxes');
        await this.get_boxes();
        this.$router.push({path: "/BoxesOverview"})
      },
      async displayModal(id){
        this.defaultModalView = Constants.ProductsView;
        this.displayedNavbarItems = [Constants.ProductsView];
        this.preselectedBox = {id: id, name: await DB_SB_get_box_name(id)};

        this.addModalVisibility = true;
      },
      async get_boxes() {
          this.data_changed = true;
          const boxes = await DB_SB_get_boxes(this.currentUser.username, this.room_id);
          this.boxes = rankBoxesBySearch(boxes, "");
          this.loading = false;
          return boxes
      },
      closeModal() {
        this.addModalVisibility = false;
        this.defaultModalView = Constants.BoxesView;
        this.displayedNavbarItems = Constants.All;
        this.preselectedBox = {id: -1, name: this.$t('add_modal.box_placeholder')};
        this.get_boxes();
          DB_SB_getStarredProducts().then((res) => {
              this.starred_products = res;
          })
      },
      async sortBoxes(search_word) {
        const boxes = await this.get_boxes();
        this.boxes = rankBoxesBySearch(boxes, search_word);
      },
      getFromQuery()
      {
        if(this.$route.query.room_id !== undefined) {
          this.room_id = this.$route.query.room_id;
        }
      },
      getFromProps()
      {
        if(this.room_id === -1) {
          console.log(this.roomid);
          this.room_id = this.roomid;
        }
      }
  },
  beforeMount() {
      this.getFromQuery();
      this.getFromProps();
      getUser().then((user) => {
          if(user === undefined)
          {
              this.$router.push("/");
          }  
          this.currentUser = user;
          this.get_boxes();
          if(this.room_id !== -1)
          {
            DB_SB_get_room(this.room_id, user).then((room) => {
              if(room.length !== 0)
                this.title = this.$t('boxes_overview.boxes_in', {location: room[0].name});
            });
          }

      });
      getSettings().then((settings) => {
        this.theme =  settings.theme;
      })

  }

}
</script>

<style scoped>
  .card {
      padding-left: 2.5%;
      padding-right: 2.5%;
  }
  .v-virtual-scroll{
      background: var(--color-dark-theme-background);
  }


  ::-webkit-scrollbar { width: 0px;  }


</style>
