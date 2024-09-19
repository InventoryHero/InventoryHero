<script setup lang="ts">

import {computed, ref} from "vue";
import {ApiStorage, StorageTypes} from "@/types/api.ts";
import {useContentFilterStore, useStorage} from "@/store";
import useScrollToTop from "@/composables/useScrollToTop.ts";

const storageStore = useStorage()
const contentFilterStore = useContentFilterStore()
const {t: $t} = useI18n()
const router = useRouter()
const route = useRoute()
const {styling} = useAppStyling()

provide('storageType', StorageTypes.Box)

const {
  scrolledDown,
  scrollToTop,
  hasScrolled,
  visible
} = useScrollToTop('scroller')


const filteredBoxes = computed(() => {
  if(search.value === null)
  {
    return storageStore.boxes
  }
  return storageStore.boxes.filter(box => box.name.toLowerCase().includes(search.value?.toLowerCase() ?? ''))
})

const allBoxes = computed(() => {
  return storageStore.boxes
})


const loadingBoxes = computed(() => storageStore.loadingStorage)
const search = ref<string|null>(null)
const hideScrollToTop = ref(false)


function showBoxContent(item: ApiStorage){
  storageStore.selectBox(item.id)
  contentFilterStore.pushConfig(route.fullPath, filteredBoxes.value.findIndex(p => p.id === item.id), search.value)
  router.push(`${route.fullPath}/box/${item.id}`)
}

onMounted(() => {
  search.value = contentFilterStore.popFilter(route.fullPath)
})

const afterText = computed(() => {
  if(loadingBoxes.value){
    return $t('boxes.loading')
  }
  if(allBoxes.value.length !== 0 && filteredBoxes.value.length !== 0){
    return $t('boxes.all_displayed')
  }
  if(allBoxes.value.length !== 0 && filteredBoxes.value.length === 0){
    return $t('boxes.no_matches')
  }
  return $t('boxes.no_boxes')
})

</script>

<template>
  <v-card
      class="d-flex flex-column fill-height fill-width"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="loadingBoxes"
          color="primary"
      />
    </template>
    <v-card-title
        class="flex-0-1"
    >
      <v-text-field
        v-model="search"
        v-bind="styling"
        density="compact"

        :placeholder="$t('boxes.filter')"
      >
        <template v-slot:append>
          <app-storage-qr-code-btn
              v-model:active="hideScrollToTop"
          />
        </template>
      </v-text-field>
    </v-card-title>
    <div
      class="flex-1-1 position-relative"
    >
      <v-card-text
          class="pt-0 wrapper"
      >
        <recycle-scroller
              ref="scroller"
              class="scroll"
              :buffer="0"
              :item-size="85"
              :items="filteredBoxes"
              :emit-update="true"
              @update="hasScrolled"
              @visible="visible(route.fullPath, filteredBoxes.length-1)"
          >
            <template v-slot="{item}">
              <storage-card
                  v-bind:storage="item"
                  :type="StorageTypes.Box"
                  @click.stop="showBoxContent(item)"
              >
              </storage-card>
            </template>
            <template #after >
              <app-content-scroll-after
                :text="afterText"
              />
            </template>
          </recycle-scroller>
      </v-card-text>

    </div>
  </v-card>
  <app-scroll-to-top-btn
    v-if="!hideScrollToTop"
    :scrolled-down="scrolledDown"
    @click.stop="scrollToTop"
  />
</template>

<style scoped lang="scss">

</style>