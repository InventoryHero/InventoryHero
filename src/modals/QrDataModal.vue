<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="auto"
        persistent
        no-click-animation
        height="100%"
    >
      <div class="d-flex-column modal-container">
        <div class="modal-toolbar">
          <v-toolbar
                  class="justify-space-evenly vuetify-toolbar-override"
          >
            <v-list-item density="compact" >
              <tag
                      :text="this.$t('product')"
                      @click="this.categoryChange(Constants.ProductsView)"
                      :active="this.product_active.toString()"/>
            </v-list-item>
            <v-list-item density="compact">
              <tag
                      @click="this.categoryChange(Constants.BoxesView)"
                      :active="this.box_active.toString()"
                      :text="this.$t('box')"
                      :hidden="!this.qrCodeData.is_room"/>
            </v-list-item>
            <v-spacer v-if="!this.qrCodeData.is_room"/>
            <v-list-item  density="compact">
              <v-icon  class="me-5" icon="fa:fas fa-times" @click="closeModal()"/>
            </v-list-item>
          </v-toolbar>
        </div>
        <div class="data-modal-content">
          <boxes-overview-view
                  v-if="this.box_active"
                  :from_qrcode="true"
                  :roomid="getId()"
                  styling="cardScrollSpacingModal"
          />

          <products-overview-view
                  v-if="this.product_active"
                  :from_qrcode="true"
                  v-bind="getRoomAndBoxIdProp()"
                  styling="cardScrollSpacingModal"
          />
        </div>
      </div>


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
    qrCodeData: Object,
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
    getId()
    {
      return this.qrCodeData.id;
    },
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
          const result = {roomid: -1, boxid: -1};
          if(this.qrCodeData.is_room)
          {
              result.roomid = this.qrCodeData.id;
          }
          if(this.qrCodeData.is_box)
          {
              result.boxid = this.qrCodeData.id;

          }
          return result;
      }

},
beforeMount() {
}
}
</script>

<style scoped>

</style>
  