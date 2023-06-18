<template>
    <SandwichMenu
            v-if="!this.from_qrcode"
            :title="this.title"
            @reloadproducts="reloadMe"
    />

  <div :style="this.styling">
    <search-bar :do_transform="this.from_qrcode ? '' : 'transform'" @valueUpdated="sortProducts"/>

    <products-card
            v-for="p in products" class="card"
            :id="p.id"
            :mapping_id="p.mapping_id"
            :productName="p.name"
            :amount="p.amount"
            :room_id="p.room_id"
            :box_id="p.box_id"
            :box_name="p.box_name"
            :room_name="p.room_name"
            :product_starred="p.starred"
            @productDeleted="deleteProduct"
            @reloadProducts="refreshData"
            @toggledStarred="updateStarred"
    />
  </div>
    <add-modal
            v-model="this.addModalVisibility"
            :defaultAddView="Constants.ProductsView"
            @closeModal="closeModal()"
    />
    <load-animation v-if="this.loading"></load-animation>
    <div v-if="!this.from_qrcode" id="spacing"></div>

    <dock
          :show_qr="false"
          @addButton="this.addModalVisibility = true"
          v-if="!this.from_qrcode"
    />
  </template>
  
  <script>

  import ProductsCard from "@/components/ProductsCard.vue";
  import SandwichMenu from "@/components/SandwichMenu.vue";
  import AddModal from "@/modals/AddModal.vue";


  import {
    DB_SB_get_all_products,
    DB_SB_get_box,
    DB_SB_get_products_per_box,
    DB_SB_get_products_per_room,
    DB_SB_get_room
  } from '@/db/supabase';
  import {getUser} from "@/db/dexie";

  import {Constants} from "@/global/constants";
  import LoadAnimation from "@/components/LoadAnimation.vue";
  import Dock from "@/components/Dock.vue";
  import BoxCard from "@/components/BoxCard.vue";
  import SearchBar from "@/components/SearchBar.vue";
  import {rankBoxesBySearch} from "@/scripts/sort";
  import QrDataModal from "@/modals/QrDataModal.vue";
  import QrReaderModal from "@/modals/QrReaderModal.vue";
  import {useToast} from "vue-toastification";


  export default {
    name: 'App',

    props: {
      roomid: {
        type: Number,
        default: -1
      },
      boxid: {
        type: Number,
        default: -1
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
      QrReaderModal, QrDataModal,
      SearchBar, BoxCard,
      Dock,
      LoadAnimation,
      AddModal,
      ProductsCard,
      SandwichMenu
    },
    data() {
        return {
            products: [],
            currentUser: "",
            addModalVisibility: false,
            Constants,
            title: this.$t('products'),
            loading: true,
            box_id: -1,
            room_id: -1,
            get_starred: false,
        }
    },
    methods: {
        reloadMe()
        {
          this.box_id = -1;
          this.room_id = -1;
          this.get_starred = false;
          this.title = this.$t('products');
          this.refreshData();
        },
        deleteProduct()
        {

          this.refreshData();
        },
        refreshData(){


          this.get_products();
        },
        async get_products() {
          if(this.room_id === -1 && this.box_id === -1)
          {
            this.products = await DB_SB_get_all_products(this.currentUser.username);
          }
          else if(this.box_id !== -1)
          {
            this.products = await DB_SB_get_products_per_box(this.box_id, this.currentUser.username)
          }
          else if(this.room_id !== -1)
          {
            this.products = await DB_SB_get_products_per_room(this.room_id, this.currentUser.username)
          }

          if(this.get_starred)
          {
            this.products = this.products.filter(product => product.starred)
          }
          this.loading = false;

        },
        closeModal() {
          this.get_products();
          this.addModalVisibility = false;
        },
        async sortProducts(needle)
        {
          this.products = rankBoxesBySearch(this.products, needle);
        },
        updateStarred(id)
        {
          this.products.forEach(function(product){
            if(product.id === id)
              product.starred = !product.starred;
          })
        },
        getFromQuery()
        {
          if(this.$route.query.box_id !== undefined) {
            this.box_id = this.$route.query.box_id;
          }

          if(this.$route.query.room_id !== undefined) {
            this.room_id = this.$route.query.room_id;
          }

          if(this.$route.query.starred !== undefined) {
            this.get_starred = true;
          }
        },
        getFromProps()
        {
          if(this.room_id === -1) {
            this.room_id = this.roomid;
          }

          if(this.box_id === -1) {
            this.box_id = this.boxid;
          }

        }
    },
    beforeMount() {
        this.getFromQuery();
        this.getFromProps();

        getUser().then((user) => {
            if(user === undefined)
            {
                this.$router.push("/login");
            }
            this.currentUser = user;

            if(this.box_id !== -1)
            {
              DB_SB_get_box(this.box_id, user).then((box) => {
                if(box.length !== 0) {

                  let locString = "products_view.products_in";
                  if (this.get_starred) {
                    locString = "products_view.starred_in"
                  }

                  this.title = this.$t(locString, {name: box[0].name});
                }
              });
            }
            else if(this.rooms !== -1)
            {
              DB_SB_get_room(this.room_id, user).then((room) => {
                if(room.length !== 0)
                  this.title = this.$t("products_view.products_in", {name: room[0].name});
              });

            }
            this.get_products();
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