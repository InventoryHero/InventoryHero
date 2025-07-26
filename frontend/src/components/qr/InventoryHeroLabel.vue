<script setup lang="ts">
import {useQRCode} from '@vueuse/integrations/useQRCode'

import usePrintSettingsStore from "@/store/usePrintSettingsStore.ts";
import {storeToRefs} from "pinia";
import {RoomResponseSchema, BoxResponseSchema} from "@/api/types/storage.ts";
import useStorageHelper from "@/composables/useStorageHelper.ts";

const printSettingStore = usePrintSettingsStore()

const {getStorageIcon, getStoragePath} = useStorageHelper()

// TODO MAKE QR CODE REALLY RESPONSIVE
const {
  object,
} = defineProps<{
  object: RoomResponseSchema | BoxResponseSchema,
}>()

const {
  storageNameVisible,
  storageIconVisible,
  storageIconSize,
  qrCodeVisible,
  qrCodeIconVisible,
  qrCodeIconWidth,
  fontSize
} = storeToRefs(printSettingStore)

const qrCodeIconWidthInPx = computed(() => {
  return `${qrCodeIconWidth.value}px`
})

const  fontSizeInPx = computed(() => {
  return `${fontSize.value}px`
})


const qrCodePayload = computed(() => {
  let route = getStoragePath(object.id, object.storage_type)
  return `${window.origin}${route?.fullPath}`
})

const icon = computed(() => {
  return getStorageIcon(object.storage_type)
})

const qrcode = useQRCode(qrCodePayload.value, {
  errorCorrectionLevel: 'H',
  margin: 0
})

</script>

<template>

<div
  class="label"
  :key="object.id"
  :id="object.id"
>
  <div
      v-if="qrCodeVisible"
      class="qr-code-wrapper"
  >
    <img
        :src="qrcode"
        alt="QR Code"
        class="qr-code"
    />

    <img
        v-if="qrCodeIconVisible"
        src="/favicon.ico"
        alt="Favicon"
        class="center-image"
    />
  </div>

  <div
      v-if="storageNameVisible || storageIconVisible"
      class="text-container overflow-hidden"
  >
    <div
        class="label-text"
        v-if="storageNameVisible"
    >
      {{ object.name }}
    </div>
    <div
        v-if="storageIconVisible"
        class="bottom-right-icon"
    >
      <v-icon
          :size="storageIconSize"
          :icon="icon"
          alt="Icon"
      />
    </div>

</div>
</div>

</template>

<style scoped lang="scss">


.label {

  height: 100%;
  width: 100%;
  background: white;
  display: flex;
  justify-content: center;
  overflow: hidden;
  .qr-code-wrapper {
    flex: 1;
    align-self: start;
    position: relative;
    padding: 0;
    height: 100%;

    .qr-code {
      height: 100%;
      width: auto;
      z-index: 2;
    }
    .center-image {
      z-index: 3;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: v-bind(qrCodeIconWidthInPx) !important;
      border-radius: 100%;
    }
  }

  .text-container {
    flex: 1 ;
    margin-left: 8px;
    position: relative;
    overflow: hidden;
    .label-text{
      font-size: v-bind(fontSizeInPx);
      color: black;
      white-space: normal;
      overflow: hidden;
      overflow-wrap: break-word;
      word-wrap: break-word;
    }
    .bottom-right-icon {
      color: black;
      position: absolute;
      bottom: 0;
      right: 0;
      z-index: 1;
    }
  }


}













</style>