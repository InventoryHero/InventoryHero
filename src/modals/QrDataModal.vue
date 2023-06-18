<template>
    <v-dialog
        transition="dialog-bottom-transition"
        width="auto"
        persistent
        no-click-animation
    >

      <v-card
              height="100%"
              class="d-flex-column modal-container"
      >
        <v-toolbar
                class="toolbar justify-space-evenly"
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

        <boxes-overview-view
                v-if="this.box_active"
                :from_qrcode="true"
                :roomid="getId()"
                styling="height:80vh;background:var(--color-dark-theme-background)"
        />

        <products-overview-view
                v-if="this.product_active"
                :from_qrcode="true"
                v-bind="getRoomAndBoxIdProp()"
                styling="height:80vh;background:var(--color-dark-theme-background)"
        />
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
  