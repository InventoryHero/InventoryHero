<script setup lang="ts">
import {useQRCode} from '@vueuse/integrations/useQRCode'
import {useConfigStore, usePrintSettings} from "@/store";
import {ApiStorage, StorageTypes} from "@/types";
import useStorageIcon from "@/composables/useStorageIcon.ts";

const storageType = inject('storageType') as StorageTypes
const {t} = useI18n()

const configStore = useConfigStore()
const printSettingStore = usePrintSettings()

const icon = useStorageIcon(storageType)


const {
  isPreview=true,
  storage=undefined,
} = defineProps<{
  isPreview?: boolean,
  storage?: ApiStorage
}>()

const margins = computed(() => {
  return printSettingStore.margins
})

const storageLabelVisible = computed(() => {
  return printSettingStore.storageLabelVisible
})
const storageNameVisible = computed(() => {
  return printSettingStore.storageNameVisible
})
const storageIconVisible = computed(() => {
  return printSettingStore.storageIconVisible
})
const borderThickness = computed(() => {
  return printSettingStore.borderThickness
})
const qrCodeVisible = computed(() => {
  return printSettingStore.qrCodeVisible
})
const qrCodeIconVisible = computed(() => {
  return printSettingStore.qrCodeIconVisible
})
const qrCodeIconWidth = computed(() => {
  return `${printSettingStore.qrCodeIconWidth}px`
})
const storageIconSize = computed(() => {
  return printSettingStore.storageIconSize
})
const fontSize = computed(() => {
  return printSettingStore.fontSize
})
const selectedRows = computed(() => {
  return printSettingStore.rows
})

const selectedCols = computed(() => {
  return printSettingStore.columns
})

const selectedPaper = computed(() => {
  return printSettingStore.paper
})

const fontSizeInPx = computed(() => {
  return `${fontSize.value}px`
})

const labelHeightInMm = computed(() => {
  return `${(selectedPaper.value.height-margins.value.top-margins.value.bottom)/selectedRows.value}mm`
})

const labelHeightCap = computed(() => {
  if(!isPreview){
    return '';
  }
  return `${selectedPaper.value.height/8}mm`
})

const labelWidthInMm = computed(() => {
  return `${(selectedPaper.value.width-margins.value.left-margins.value.right)/selectedCols.value}mm`
})

const contentLayout = computed(() => {
  if(qrCodeIconVisible.value && storageLabelVisible.value){
    return '';
  }
  return 'center';
})

const border = computed(() => {
  if(borderThickness.value === 0){
    return ''
  }
  return `${configStore.primary} ${printSettingStore.borderThickness}px solid`
})


const qrCodeScale = computed(() => {
  if(selectedRows.value <= 8){
    return selectedPaper.value.scales['default']
  }
  if(selectedRows.value > 15){
    return selectedPaper.value.scales['default']
  }
  return selectedPaper.value.scales[selectedRows.value.toString()]
})

const text = computed(() => {
  if(isPreview){
    return t('print.example_text')
  }
  return storage?.name
})

const elementId = computed(() => {
  if(isPreview){
    return "example"
  }
  return (storage?.id?.toString()) ?? ''
})

const qrCodePayload = computed(() => {

  let route = "example"
  if(storageType ===StorageTypes.Box){
    route = "boxes/box"
  } else if(storageType === StorageTypes.Location){
    route = "locations/location"
  }
  if(isPreview){
    return `${window.location.origin}/${route}/example`
  }
  return `${window.location.origin}/${route}/${storage?.id ?? ''}`
})


// otherwise the qr code wouldn't react to size changes
const qrcode = computed(() => {
  return useQRCode(qrCodePayload.value, {
    errorCorrectionLevel: 'H',
    margin: 0,
    width: qrCodeScale.value
  })
})

</script>

<template>
<div
  v-if="storage !== undefined || isPreview"
  class="label"
  :id="elementId"
>
  <div class="label-wrapper">
    <div
        v-if="qrCodeVisible"
        class="qr-code-wrapper"
    >
      <img
          :src="qrcode.value"
          alt="QR Code"
          class="qr-code"
      />
      <!-- Use the favicon in the center of the QR code -->
      <img
          v-if="qrCodeIconVisible"
          src="/favicon.ico"
          alt="Favicon"
          class="center-image"
      />
    </div>
    <div
        v-if="storageLabelVisible"
        class="text-container"
    >
      <div
          class="label-text"
          v-if="storageNameVisible"
      >
        {{ text }}
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
</div>

</template>

<style scoped lang="scss">
.label {
  position: sticky;

  border:  v-bind(border);
  padding: 4px;
  height: v-bind(labelHeightCap);
  width: v-bind(labelWidthInMm);
  background: white;
  box-sizing: border-box;

  // cap preview, to still look nice in frontend
  max-width: 100%;

  .label-wrapper{
    display: flex;
    justify-content: v-bind(contentLayout);
    height: v-bind(labelHeightInMm);
    max-height: v-bind(labelHeightCap);
    .qr-code-wrapper {
      position: relative;
      display: inline-block;
      margin-right: 8px;
      padding: 0;
      flex-shrink: 0;
      align-self: center;
      .qr-code {
        display: block;
        width: 100%;
        height: auto;
      }
      .center-image {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: v-bind(qrCodeIconWidth);
        height: v-bind(qrCodeIconWidth);
        border-radius: 100%;
      }
    }
    .text-container {
      flex: 1 ;
      position: relative;
      padding-left: 4px;

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
        bottom: 4px;
        right: 4px;
        z-index: 10;
      }
    }
  }

}













</style>