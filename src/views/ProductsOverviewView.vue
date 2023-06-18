<template>
    <SandwichMenu v-if="!this.from_qrcode"  :title="this.title"/>

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
            @productDeleted="refreshData"
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


  export default {
    name: 'App',
    props: {
      room_id: {
        type: Number,
        default: -1
      },
      box_id: {
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
      },
      get_starred: {
        type: Boolean,
        default: false,
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
            title: "Products",
            loading: true
        }
    },
    methods: {
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
        }
    },
    beforeMount() {
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

                  this.title = "Products in " + box[0].name;
                  if (this.get_starred) {
                    this.title = "Starred p" + this.title.substring(1);
                  }
                }
              });
            }
            else if(this.rooms !== -1)
            {
              DB_SB_get_room(this.room_id, user).then((room) => {
                if(room.length !== 0)
                  this.title = "Products in " + room[0].name;
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