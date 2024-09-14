<script setup lang="ts">
import {usePrintSettings, useStorage} from "@/store";
import {useVueToPrint} from "vue-to-print";
import {StorageTypes} from "@/types";
import {useTemplateRef} from "vue";
import { toBlob} from 'html-to-image';
import { saveAs } from 'file-saver';


const {t} = useI18n()
const printSettingsStore = usePrintSettings()
const storageStore = useStorage()
const storageType = inject('storageType') as StorageTypes

const paper = computed(() => printSettingsStore.paper)
const paperHeightInMm = computed(() => `${paper.value.height}mm`)
const paperWidthInMm = computed(() => `${paper.value.width}mm`)

const rows = computed(() => printSettingsStore.rows)
const cols = computed(() => printSettingsStore.columns)

const marginTop = computed(() => `${printSettingsStore.margins.top}mm`)
const marginBottom = computed(() => `${printSettingsStore.margins.bottom}mm`)
const marginLeft = computed(() => `${printSettingsStore.margins.left}mm`)
const marginRight = computed(() => `${printSettingsStore.margins.right}mm`)

const labelsPerPage = computed(() => {
  // Total number of QR code slots available per page
  return rows.value * cols.value;
});

const totalPages = computed(() => {
  // Total number of pages based on the total selected storage items
  const totalLabels = selectedStorage.value.length;
  return Math.ceil(totalLabels / labelsPerPage.value);
});



const paperStyle = computed(() => {
  return {
    height: paperHeightInMm.value,
    width: paperWidthInMm.value,
    padding: `${marginTop.value} ${marginRight.value} ${marginBottom.value} ${marginLeft.value}`,
    backgroundColor: 'white',
    color: 'black'
  }
})

const page = useTemplateRef("page")
const loadingPrint = ref(false)
const savingPictures = ref(false)


const { handlePrint } = useVueToPrint({
  content: () => page.value,
  onAfterPrint: () => {
    loadingPrint.value = false
  },
  removeAfterPrint: true
});

const previewScale = computed({
  get: () => printSettingsStore.previewScale,
  set: printSettingsStore.setPreviewScale
})

const selectedStorage = computed(() => storageStore.printSelection)
const storage = computed(() => storageStore.getStorage(storageType))

function getStorage(page: number, row: number, col: number){
  const index = (page - 1) * labelsPerPage.value + (row - 1) * cols.value + (col - 1);
  if(index >= selectedStorage.value.length){
    return undefined
  }
  return storage.value.find(s => s.id === selectedStorage.value[index])
}

function print(){
  loadingPrint.value = true
  handlePrint()
}
async function saveToImg(){
  savingPictures.value = true
  for(let i = 0; i < selectedStorage.value.length; i++){
    const label = document.getElementById(selectedStorage.value[i].toString())
    if(label === null)
    {
      continue
    }
    const blob = await toBlob(label)
    const storageItem = storage.value.find(s => s.id === selectedStorage.value[i])
    if(storageItem) {
      saveAs(blob, `${storageItem.name}.png`)
    }
  }
  savingPictures.value=false

}

</script>

<template>
  <v-card
      class="d-flex flex-column fill-height"
  >
    <v-card
        class="flex-0-0"
        elevation="0"
        density="compact"
    >
      <v-card-title

      >
        {{t('print.preview_page.scale')}}
      </v-card-title>
      <v-card-text
          class="pa-0 pr-2 pl-2"
      >
        <v-slider
            v-model="previewScale"
            max="100"
            min="0"
            step="0.1"
            title="scale"
            hide-details
            density="compact"
        />
      </v-card-text>
      <div
        class="pb-2 pr-2 pl-2 d-flex justify-end"

      >
        <v-btn
          @click="saveToImg"
          :loading="savingPictures"
          :disabled="savingPictures || loadingPrint"
          prepend-icon="mdi-image"
          color="primary"
          variant="plain"
          :text="t('print.preview_page.save_img')"
        />
        <v-btn
            prepend-icon="mdi-printer"
            color="primary"
            variant="plain"
            @click="print"
            :loading="loadingPrint"
            :disabled="loadingPrint"
            :text="t('print.preview_page.print')"
        />
      </div>
    </v-card>
    <v-container
        class="flex-1-1 overflow-auto"
    >
      <div
          class="paper-container"
          :style="`transform: scale(${previewScale/100})`"
      >
        <div
            ref="page"
        >
          <div
              v-for="page in totalPages"
              :style="paperStyle"
              :key="page"
          >
            <div
              v-for="row in rows"
              :key="row"
              style="display: flex"
            >
              <div
                v-for="col in cols"
                :key="col"
                style="display: flex; justify-content: center"
              >
                <app-qr-code
                  :storage="getStorage(page, row, col)"
                  :is-preview="false"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </v-container>
  </v-card>
</template>

<style scoped lang="scss">
.paper-container{
  transform-origin: left top 0;
}
</style>