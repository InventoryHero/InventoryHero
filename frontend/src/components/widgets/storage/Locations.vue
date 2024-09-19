<script setup lang="ts">

import {computed, ref} from "vue";
import {ApiStorage, StorageTypes} from "@/types/api.ts";
import {useContentFilterStore, useStorage} from "@/store";
import useScrollToTop from "@/composables/useScrollToTop.ts";

const storageStore = useStorage()
const contentFilterStore = useContentFilterStore()
const {styling} = useAppStyling()
const route = useRoute()
const router = useRouter()
const {t} = useI18n()


provide('storageType', StorageTypes.Location)
const {
  scrolledDown,
  scrollToTop,
  hasScrolled,
  visible
} = useScrollToTop('scroller')

const filteredLocations = computed(() => {
  if(!search.value)
  {
    return storageStore.locations
  }
  return storageStore.locations.filter(l => l.name.toLowerCase().includes(search.value?.toLowerCase() ?? ''))
})

const allLocations = computed(() => {
  return storageStore.locations
})


const loadingLocations = computed(() => storageStore.loadingStorage)
const search = ref<string|null>(null)
const hideScrollToTop = ref(false)

function showLocationContent(item: ApiStorage){
  storageStore.selectLocation(item.id)
  contentFilterStore.pushConfig(route.fullPath, filteredLocations.value.findIndex(l => l.id === item.id), search.value)
  router.push(`${route.fullPath}/location/${item.id}`)
}

onMounted(() => {
  search.value = contentFilterStore.popFilter(route.fullPath)
})

const afterText = computed(() => {
  if(loadingLocations.value){
    return t('locations.loading')
  }
  if(allLocations.value.length !== 0 && filteredLocations.value.length !== 0){
    return t('locations.all_displayed')
  }
  if(allLocations.value.length !== 0 && filteredLocations.value.length === 0){
    return t('locations.no_matches')
  }
  return t('locations.no_locations')
})

</script>

<template>

  <v-card
      class="d-flex flex-column fill-height fill-width"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="loadingLocations"
          color="primary"
      />
    </template>
    <v-card-title
        class="flex-0-1"
    >
      <v-text-field
          v-model="search"
          v-bind="styling"
          :placeholder="$t('locations.filter')"
          density="compact"
      >
        <template v-slot:append>
          <app-storage-qr-code-btn
              v-model:active="hideScrollToTop"
          />
        </template>
      </v-text-field>
    </v-card-title>
    <v-card-text
        class="d-flex position-relative flex-1-1"
    >
      <div class="wrapper">
        <recycle-scroller
            ref="scroller"
            class="scroll"
            :buffer="0"
            :item-size="105"
            :items="filteredLocations"
            :emit-update="true"
            @update="hasScrolled"
            @visible="visible(route.fullPath, filteredLocations.length-1)"
        >
          <template v-slot="{item}">

            <v-row
                :no-gutters="true"
                justify="center"
            >
              <v-col
                  cols="11"
              >
                <storage-card
                    v-bind:storage="item"
                    :type="StorageTypes.Location"
                    @click.stop="showLocationContent(item)"
                >
                </storage-card>
              </v-col>
            </v-row>

          </template>
          <template #after>
            <app-content-scroll-after
              :text="afterText"
            />
          </template>
        </recycle-scroller>

      </div>
    </v-card-text>
  </v-card>
  <app-scroll-to-top-btn
      v-if="!hideScrollToTop"
      :scrolled-down="scrolledDown"
      @click.stop="scrollToTop"
  />

</template>

<style scoped lang="scss">

</style>