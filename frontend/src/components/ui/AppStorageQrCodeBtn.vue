<script setup lang="ts">

import useDialogConfig from "@/composables/useDialogConfig.ts";
import {useStorage} from "@/store";
import {useNotification} from "@kyvg/vue3-notification";

const storageStore = useStorage()
const {t} = useI18n()
const {notify} = useNotification()

defineOptions({
  inheritAttrs: false
})

const {
  isVisible: selectionDialogVisible,
  openDialog: openSelectionDialog,
  closeDialog: closeSelectionDialog,
  dialogProps: selectionDialogProps
} = useDialogConfig()

const {
  isVisible: printConfigDialogVisible,
  openDialog: openPrintConfigDialog,
  closeDialog: closePrintConfigDialog,
  dialogProps: printConfigDialogProps
} = useDialogConfig()


const storageSelected = computed(() => {
  return Object.values(storageStore.printSelection).some(s => s ?? false)
})

function printSelection(){
  if(storageSelected.value){
    openPrintConfigDialog()
  } else {
    notify({
      title: t("toasts.title.info.no_storage_selected"),
      text: t("toasts.text.info.no_storage_selected"),
      type: "info"
    })
  }
  closeSelectionDialog()
}

function openSelection(){

  if(usePreselected){
    printSelection()
  } else {
    openSelectionDialog()
  }
}

const {usePreselected=false} = defineProps<{usePreselected?: boolean}>()

onBeforeRouteLeave(()=> {
  closeSelectionDialog()
  closePrintConfigDialog()
})

</script>

<template>
  <v-dialog
      v-model="selectionDialogVisible"
      v-bind="selectionDialogProps"
  >
    <storage-selection-modal
        class="included"
        @close="() => {
          storageStore.clearPrintSelection()
          closeSelectionDialog()
        }"
        @selection-confirmed="printSelection"
    />
  </v-dialog>

  <v-dialog
      v-model="printConfigDialogVisible"
      v-bind="printConfigDialogProps"
  >
    <print-qr-codes-modal
        @close="() => {
          storageStore.clearPrintSelection()
          closePrintConfigDialog()
        }"
    />
  </v-dialog>

  <app-icon-btn
      class="flex-0-0"
      icon="mdi-qrcode"
      size="x-large"
      v-bind="$attrs"
      @click="openSelection"
  />
</template>

<style scoped lang="scss">

</style>