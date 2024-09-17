<script setup lang="ts">

import {computed, onMounted, ref, watch} from "vue";
import {ApiStorage, StorageTypes} from "@/types/api.ts";
import {useProducts, useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {LocationEndpoint} from "@/api/http";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import {onBeforeRouteLeave} from "vue-router";

const storageStore = useStorage()
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")

provide('storageType', StorageTypes.Location)

const {scrolledDown, scrollToTop, hasScrolled} = useScrollToTop('scroller')
const { isVisible: boxOverlayVisible, openDialog, closeDialog, dialogProps } = useDialogConfig()

const filteredLocations = computed(() => {
  if(search.value === "")
  {
    return storageStore.locations
  }
  return storageStore.locations.filter(l => l.name.toLowerCase().includes(search.value.toLowerCase()))
})

const allLocations = computed(() => {
  return storageStore.locations
})

const {preselectedLocation=undefined, filteredFrom=undefined} = defineProps<{
  preselectedLocation?: string,
  filteredFrom?: string,
}>()

const loadingLocations = ref(false)
const search = ref("")

function showLocationContent(item: ApiStorage){
  storageStore.selectLocation(item)
  openDialog()
}

function closeLocationOverlay(){
  closeDialog()
  storageStore.deselectLocation()
}

function deleteLocation(id: number){
  closeDialog()
  storageStore.deleteLocation(id)
}

function loadLocations(){
  loadingLocations.value = true;
  locationEndpoint.getLocations({
    id: preselectedLocation,
    contained: true
  }).then((locations: Array<ApiStorage>) => {
    loadingLocations.value = false;
    storageStore.storeLocations(locations)
  })
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
watch(() => preselectedLocation, (_: string|undefined, __: string|undefined) =>{
  loadLocations()
});


onMounted(() => {
  loadLocations()
})

onBeforeRouteLeave(() => {
  const productStore = useProducts()
  productStore.reset()
  storageStore.reset()
})
</script>

<template>
  <v-row
      :no-gutters="true"
      justify="center"
      class="fill-height"
  >
    <v-col
        cols="12"
        lg="6"
        class="position-relative"
    >
      <v-dialog
          v-model="boxOverlayVisible"
          v-bind="dialogProps"

      >
        <location-overlay
            @deleted="deleteLocation"
            @close="closeLocationOverlay"
        />
      </v-dialog>
      <v-card
          class="d-flex flex-column fill-height"
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
          <qr-code-filter
              :pre-selected="preselectedLocation !== undefined"
              v-model:search="search"
              pre-selection-close-action="/storage/locations"
              :pre-selection-title="$t('locations.prefiltered', {prefilter: filteredFrom ?? $t('scan.from')})"
              @qr-selection-toggled="scrollToTop"
          />
        </v-card-title>
        <v-card-text
            class="d-flex position-relative flex-1-1"
        >
          <div class="wrapper">
            <recycle-scroller
                ref="scroller"
                class="scroll"
                :buffer="0"
                :item-size="110"
                :items="filteredLocations"
                :emit-update="true"
                @update="hasScrolled"
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
              <template #after v-if="preselectedLocation === undefined">
                <v-row
                    :no-gutters="true"
                    justify="center"
                >

                  <v-col
                      cols="11"
                  >
                    <v-card
                        :elevation="0"
                    >
                      <v-card-title
                          class="text-center text-wrap"
                      >
                        <p
                            class="pb-1"
                            v-if="loadingLocations"
                        >
                          {{ $t('locations.loading') }}
                        </p>
                        <p
                            class="pb-1"
                            v-else-if="allLocations.length !== 0 && filteredLocations.length !== 0"
                        >
                          {{ $t('locations.all_displayed') }}
                        </p>
                        <p
                            class="pb-1"
                            v-else-if="allLocations.length !== 0 && filteredLocations.length === 0"
                        >
                          {{ $t('locations.no_matches')}}
                        </p>
                        <p
                            class="pb-1"
                            v-else
                        >
                          {{ $t('locations.no_locations')}}
                        </p>
                      </v-card-title>
                    </v-card>
                  </v-col>
                </v-row>
              </template>
              <template #after v-else>
                <v-row
                    :no-gutters="true"
                    justify="center"
                >

                  <v-col
                      cols="11"
                  >
                    <v-card
                        :elevation="0"
                    >
                      <v-card-title
                          class="text-center text-wrap"
                      >
                        <p
                            class="pb-1"
                            v-if="allLocations.length === 0 && !loadingLocations"
                        >
                          {{ $t('locations.no_matches') }}
                        </p>
                      </v-card-title>
                    </v-card>
                  </v-col>
                </v-row>
              </template>
            </recycle-scroller>

          </div>
        </v-card-text>
      </v-card>
      <app-scroll-to-top-btn
          :scrolled-down="scrolledDown"
          @click.stop="scrollToTop"
      />
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>