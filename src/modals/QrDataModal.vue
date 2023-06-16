<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="auto"
    >
        <v-card
            height="100%"
            class="d-flex-column modal-container"
        >
            <v-toolbar
                class="toolbar justify-space-evenly"
            >
                    <v-list-item density="compact" >
                        <tag text="Product" @click="this.categoryChange(Constants.ProductsView)" :active="this.product_active.toString()"/>
                    </v-list-item>
                    <v-list-item density="compact">
                        <tag @click="this.categoryChange(Constants.BoxesView)" :active="this.box_active.toString()" text="Box" :hidden="!this.qrCodeData.is_room"/>
                    </v-list-item>
                    <v-spacer v-if="!this.qrCodeData.is_room"/>
                    <v-list-item  density="compact">
                    <v-icon  class="me-5" icon="fa:fas fa-times" @click="closeModal()"/>
                </v-list-item>
            </v-toolbar>

            <boxes-overview-view v-if="this.box_active" :from_qrcode="true" :room_id="this.qrCodeData.id"></boxes-overview-view>
            <products-overview-view v-if="this.product_active" :from_qrcode="true" v-bind="getRoomAndBoxIdProp()"></products-overview-view>
        </v-card>

    </v-dialog>

</template>

<script>
import Tag from '@/components/Tag.vue';
import BoxesOverviewView from "@/views/BoxesOverviewView.vue";
import ProductsOverviewView from "@/views/ProductsOverviewView.vue";

import {Constants} from  "@/global/constants";

export default {
name: 'App',
    computed: {
        Constants() {
            return Constants
        }
    },
props: {
    defaultAddView: {
        type: String,
        default: Constants.ProductsView
    },
    navbarItems: {
        type: [Array, String],
        default: Constants.All
    },
    qrCodeData: Object
},
components: {
    Tag,
    BoxesOverviewView,
    ProductsOverviewView
},
data() {
    return {
      product_active: true,
      box_active: false,
    }
},
  methods: {
    closeModal() {
        this.$emit('closeQrDataModal')
    },
      categoryChange(change_to) {

          if (change_to === Constants.ProductsView) {
              this.product_active = true;
              this.box_active = false;
          } else if (change_to === Constants.BoxesView)  {
              this.box_active = true;
              this.product_active = false;
          }
      },
      getRoomAndBoxIdProp()
      {
          const result = {room_id: -1, box_id: -1};
          if(this.qrCodeData.is_room)
          {
              result.room_id = this.qrCodeData.id;
          }
          if(this.qrCodeData.is_box)
          {
              result.box_id = this.qrCodeData.id;

          }
          console.log(result);
          return result;
      }

},
beforeMount() {
}
}
</script>

<style scoped>
.modal-container{
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
    border-radius: 10px;
    border: white solid 1px;
    height: 60vh;
    color: white;
}
.toolbar{
    background-color: transparent;
    border-bottom: white solid 1px;
    color: white;
}
</style>
  