<template>
    <SandwichMenu v-if="!this.from_qrcode"  :title="this.title"/>
    <v-virtual-scroll
        class="virtual-scroll-bg"
        :height="80+'vh'"
        :items="products"
    >
        <template v-slot:default="{ item }">
            <ProductsCard  :id="item.id" :productName="item.name" :amount="item.amount" :room_id="item.room_id" :box_id="item.box_id" @productDeleted="refreshData"/>
        </template>
    </v-virtual-scroll>
      <add-modal :defaultAddView="Constants.ProductsView" v-if="this.addModalVisibility" @closeModal="closeModal()"/>
    <load-animation v-if="this.loading"></load-animation>
    <div id="spacing"></div>
    <dock
            @qrButton="this.qrReaderModalVisibility=true"
            @addButton="this.addModalVisibility = true"
            v-if="!this.from_qrcode"
    />
  </template>
  
  <script>
  import AddButton from '@/components/AddButton.vue'
  import QrButton from '@/components/QrButton.vue'
  import ProductsCard from "@/components/ProductsCard.vue";
  import SandwichMenu from "@/components/SandwichMenu.vue";

  import {
    DB_SB_get_all_products,
    DB_SB_get_all_products_per_storage_location, DB_SB_get_box, DB_SB_get_products_per_box, DB_SB_get_products_per_room,
    DB_SB_get_room,
    DB_SB_getStarredProducts
  } from '@/db/supabase';
  import {getUser} from "@/db/dexie";
  import AddModal from "@/modals/AddModal.vue";
  import { Constants } from "@/global/constants";
  import LoadAnimation from "@/components/LoadAnimation.vue";
  import Dock from "@/components/Dock.vue";
  
  
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
    },
    components: {
      Dock,
      LoadAnimation,
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
            qrReaderModalVisibility: false,
            Constants,
            title: "Products",
            loading: true
        }
    },
    methods: {
        refreshData(){
          this.get_boxes();
        },
        get_boxes() {
          if(this.room_id === -1 && this.box_id === -1)
          {
            DB_SB_get_all_products(this.currentUser.username).then((products) => {
              this.products = products;
              this.loading = false;
            });
          }
          else if(this.box_id !== -1)
          {
            DB_SB_get_products_per_box(this.box_id, this.currentUser.username).then((products) => {
              if(products !== undefined && products.data !== undefined)
                this.products = products.data;
                this.loading = false;
            })
          }
          else if(this.room_id !== -1)
          {
            DB_SB_get_products_per_room(this.room_id, this.currentUser.username).then((products) => {
              if(products !== undefined && products.data !== undefined)
                this.products = products.data;
                this.loading = false;
            })
          }

        },
        getFilteredProducts()
        {
          DB_SB_get_all_products_per_storage_location(this.room_id, this.box_id).then( (products) => {
            this.products = products;
          })
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

            if(this.box_id !== -1)
            {
              DB_SB_get_box(this.box_id, user).then((box) => {
                if(box.length !== 0)
                  this.title = "Products in " + box[0].name ;
              });
            }
            else if(this.rooms !== -1)
            {
              DB_SB_get_room(this.room_id, user).then((room) => {
                if(room.length !== 0)
                  this.title = "Products in " + room[0].name;
              });

            }
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