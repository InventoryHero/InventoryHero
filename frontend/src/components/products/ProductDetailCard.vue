<script lang="ts">
import {defineComponent, PropType, ref} from 'vue'
import {ProductLocations, Storage, StorageTypes} from "@/types";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import AppStorageTitle from "@/components/ui/AppStorageTitle.vue";
import QuickActions from "@/components/products/QuickActions.vue";
import useStorageTitle from "@/composables/useStorageTitle.ts";


export default defineComponent({
  name: "ProductDetailCard",
  components: {QuickActions, AppStorageTitle, FontAwesomeIcon},
  emits:{
    "product-mapping:update"(mapping: ProductLocations, update: Partial<ProductLocations>, callback: () => void){
      return true
    },
    "product-mapping:delete"(mappingId: number, productId: number, callback: () => void){
      return true
    },
    showMappingOverlay(mapping: ProductLocations)
    {
      return true;
    },
    redirectToStorage(payload: Storage, from: string)
    {
      return true
    }
  },
  props: {
    item: {
      type: Object as PropType<ProductLocations>,
      required: true
    },
    productName: {
      type: String,
      default: ""
    }
  },
  computed: {
    amount(){
      return this.item.amount
    },
    storageTitle(){
      return useStorageTitle(ref(this.item.storage))
    }
  },
  data(){
    return{
      requestInProgress: false,
      overlayItem: undefined as undefined|ProductLocations
    }
  },
  methods:{
    redirect(){
      this.$emit('redirectToStorage', this.item?.storage as Storage,  this.$t('product', {name: this.productName}))
    },
    adjustAmount(increment: number){
      this.requestInProgress = true
      this.$emit('product-mapping:update', this.item, {
        amount: this.amount+increment
      }, this.callback)
    },
    async deleteMe()
    {
      // TODO CONFIRMATION MODAL
      this.requestInProgress = true;
      this.$emit('product-mapping:delete', this.item.id,  this.item.product_id, this.callback)
      // TODO NOTIFY
    },
    callback(){
      this.requestInProgress = false
    },

  }
})
</script>

<template>
  <v-row
      :no-gutters="true"
      justify="space-between"
  >
    <v-col
        class="d-flex justify-start align-center"
    >
      <slot name="title">
        <app-storage-title
            :icon="storageTitle.icon"
            color="primary"
            :title="storageTitle.name"
            variant="tonal"
            @click="redirect()"
        />
      </slot>

    </v-col>
  </v-row>
  <v-row
      :no-gutters="true"
      justify="space-between"

  >
    <v-col
    >
      {{ $t("products.product.amount") }}
    </v-col>
    <v-col
        cols="2"
        class="d-flex justify-end"
    >
      {{ amount }}
    </v-col>
  </v-row>
  <v-row
      :no-gutters="true"
      justify="space-between"

  >
    <v-col
    >
      {{ $t('products.product.last_used')}}
    </v-col>
    <v-col
        cols="2"
        class="d-flex justify-end"
    >
      {{ $d(new Date(item.updated_at)) }}
    </v-col>
  </v-row>
  <quick-actions
      :request-in-progress="requestInProgress"
      @delete-me="deleteMe()"
      @update-amount="adjustAmount($event)"
      @show-details="$emit('showMappingOverlay', item)"
  />

  <v-divider class="border-opacity-75"/>
</template>

<style scoped lang="scss">

</style>