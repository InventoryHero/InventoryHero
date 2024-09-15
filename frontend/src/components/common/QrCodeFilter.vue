<script setup lang="ts">


import StorageSelectionModal from "@/components/widgets/QrCode/Print/StorageSelectionModal.vue";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import {useStorage} from "@/store";
import {useNotification} from "@kyvg/vue3-notification";

const storageStore = useStorage()
const {t} = useI18n()
const {notify} = useNotification()

const emit = defineEmits<{
  (e: 'qrSelectionToggled'): void
}>()

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


const search = defineModel<string>("search")
const {
  preSelected=false,
  preSelectionCloseAction="",
  preSelectionTitle=""
} = defineProps<{
  preSelected?: boolean,
  preSelectionCloseAction?: string,
  preSelectionTitle?: string
}>()

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
  emit('qrSelectionToggled')
  openSelectionDialog()
}

</script>

<template>

  <v-dialog
      v-model="selectionDialogVisible"
      v-bind="selectionDialogProps"
  >
    <storage-selection-modal
      @close="closeSelectionDialog"
      @selection-confirmed="printSelection"
    />
  </v-dialog>

  <v-dialog
    v-model="printConfigDialogVisible"
    v-bind="printConfigDialogProps"
  >
    <print-qr-codes-modal
      @close="closePrintConfigDialog"
    />
  </v-dialog>

  <div
    class="d-flex align-center"
  >
    <div
      class="flex-1-1"
    >
      <text-filter
          v-if="!preSelected"
          v-model:filter="search"
      />
      <app-preselection-filter
          v-else
          @click:close="$router.push(preSelectionCloseAction)"
          :title="preSelectionTitle"
      />
    </div>

    <app-icon-btn
        class="flex-0-0"
        icon="mdi-qrcode"
        size="x-large"
        @click="openSelection"
    />
  </div>
</template>

<style scoped lang="scss">

</style>