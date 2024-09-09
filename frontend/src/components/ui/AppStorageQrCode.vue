<script lang="ts">
import {ApiStorage, StorageTypes} from "@/types";
import {PropType} from "vue";

export default defineComponent({
  name: "AppStorageQrCode",
  props:{
    class:{
      type: String,
      default: ''
    },
    storage:{
      type: Object as PropType<ApiStorage>,
      default: undefined
    },
    printLabel:{
      type: Boolean,
      default: true
    },
    showTitle:{
      type: Boolean,
      default: true
    },
    showStorageTypeIcon:{
      type: Boolean,
      default: true
    },
    showBorder:{
      type: Boolean,
      default: true
    },
    borderColor: {
      type: String,
      default: 'primary'
    },
    qrCodeSize: {
      type: Number,
      default: 120
    },
    showQrCodeIcon:{
      type: Boolean,
      default: true
    }
  },
  computed:{
    logo(){
      if(!this.showQrCodeIcon)
      {
        return undefined
      }
      return "/favicon.ico"
    },

    qrCodePayload(){
      return JSON.stringify({
        id: this.storage?.id ?? -1,
        household: this.storage?.household_id,
        storage_type: this.storage?.type
      })
    },
    title(){
      return this.storage?.name ?? "qrcode"
    },
    icon(){
      switch(this.storage?.type ?? -1)
      {
        case StorageTypes.Location:
          return "mdi-archive-marker"
        case StorageTypes.Box:
          return "mdi-package-variant"
        default:
          return "mdi-archive-off"
      }
    }
  },
  data(){
    return {
      showQr: false,
      vueQrDownload: ""
    }
  },
  methods: {
  },
})
</script>

<template>
  <div
      class="qr-code"
      :class="{
        'show-border': showBorder,
      }"
  >
    <v-row
      justify="center"
    >
      <v-col
        class="d-flex justify-center align-center"
      >
        <vue-qr
            ref="qrcode"
            :text="qrCodePayload"
            :margin="0"
            :correct-level="3"
            :logo-src="logo"
            :size="qrCodeSize"
            class="ma-2"
        />
      </v-col>
      <v-col v-if="printLabel">
        <v-row :no-gutters="true" class="fill-height flex-column">
          <v-col v-if="showTitle" class="text">

            {{ title }}

          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-icon
        v-if="showStorageTypeIcon && printLabel"
        :icon="icon"
        class="icon"
    />

  </div>
</template>

<style scoped lang="scss">
.qr-code{
  &.show-border{
    border: 2px solid rgba(var(--v-theme-primary), 1);
  }
  margin-bottom: 2px;
  position: relative
}
.icon{
  position: absolute;
  bottom: 4px;
  right: 8px;
}

.text{
  text-wrap: auto;
  word-break: break-all;
}
</style>