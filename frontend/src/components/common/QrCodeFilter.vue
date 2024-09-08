<script lang="ts">
import {defineComponent} from 'vue'
import {Storage} from "@/types";

export default defineComponent({
  name: "QrCodeFilter",
  emits: {
    updateFilter(payload: string){
      return true;
    },
    'update:search'(payload: string){
      return true
    }
  },
  props: {
    preSelected: {
      type: Boolean,
      default: false
    },
    preSelectionTitle: {
      type: String,
      default: ""
    },
    preSelectionCloseAction:{
      type: String,
      default: ''
    },
    search: {
      type: String,
      default: ''
    },
    storage: {
      type: Array<ApiStorage>,
      default: []
    }
  },
  computed:{
    searchString:{
      get(){
        return this.search
      }, set(value: string){
        this.$emit('update:search', value)
      }
    }
  },
  data(){
    return{
      selectForQrCodePrinting: false
    }
  }
})
</script>

<template>
  <v-row
      :no-gutters="true"
      v-bind="$attrs"
  >
    <v-col>
      <text-filter
          v-if="!preSelected"
          v-model:filter="searchString"
          width="100%"

      />

      <app-preselection-filter
          v-else
          @click:close="$router.push(preSelectionCloseAction)"
          :title="preSelectionTitle"
      />
    </v-col>
    <v-col
        cols="1"
        lg="1"
        class="d-flex justify-end align-center ms-2"
    >
      <app-icon-btn
          icon="mdi-qrcode"
          size="large"
          @click="selectForQrCodePrinting = true"
      />
    </v-col>
  </v-row>

  <print-qr-modal
      v-model="selectForQrCodePrinting"
      :storage="storage"
  />
</template>

<style scoped lang="scss">

</style>