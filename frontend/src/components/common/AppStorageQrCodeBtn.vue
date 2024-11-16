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

const active = defineModel<boolean>("active")

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
      title: t("toasts.titles.info.no_storage_selected"),
      text: t("toasts.text.info.no_storage_selected"),
      type: "info"
    })
  }
}

function openSelection(){
  active.value = true
  if(usePreselected){
    printSelection()
  } else {
    storageStore.clearPrintSelection()
    openSelectionDialog()
  }
}

const {usePreselected=false} = defineProps<{usePreselected?: boolean}>()



onBeforeRouteLeave(()=> {
  if(printConfigDialogVisible.value || selectionDialogVisible.value){
    closeSelectionDialog()
    closePrintConfigDialog()
  }
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
          closeSelectionDialog()
          active = false
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
          closePrintConfigDialog()
          active = false
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