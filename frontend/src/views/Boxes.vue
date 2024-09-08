<script setup lang="ts">

import {computed, onMounted, ref, watch} from "vue";
import {ApiStorage, StorageTypes} from "@/types/api.ts";
import {useProducts, useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {BoxEndpoint} from "@/api/http";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import BoxOverlay from "@/components/storage/BoxOverlay.vue";
import {onBeforeRouteLeave} from "vue-router";

const storageStore = useStorage()
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")

const {scrolledDown, scrollToTop, hasScrolled} = useScrollToTop('scroller')
const { isVisible: boxOverlayVisible, openDialog, closeDialog, dialogProps } = useDialogConfig()

const filteredBoxes = computed(() => {
  if(search.value === "")
  {
    return storageStore.boxes
  }
  return storageStore.boxes.filter(box => box.name.toLowerCase().includes(search.value.toLowerCase()))
})

const allBoxes = computed(() => {
  return storageStore.boxes
})

const {preselectedBox=undefined, filteredFrom=undefined} = defineProps<{
  preselectedBox?: string,
  filteredFrom?: string,
}>()

const loadingBoxes = ref(false)
const search = ref("")

function showBoxContent(item: ApiStorage){
  storageStore.selectBox(item)
  openDialog()
}

function closeBoxOverlay(){
  closeDialog()
  storageStore.deselectBox()
}

function deleteBox(id: number){
  closeDialog()
  storageStore.deleteBox(id)
}

function loadBoxes(){
  loadingBoxes.value = true;
  boxEndpoint.getBoxes({
    id: preselectedBox,
    contained: true
  }).then((boxes: Array<ApiStorage>) => {
    loadingBoxes.value = false;
    storageStore.storeBoxes(boxes)
  })
}

watch(() => preselectedBox, (_: string|undefined, __: string|undefined) =>{
  loadBoxes()
});


onMounted(() => {
  loadBoxes()
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
        <box-overlay
            @deleted="deleteBox"
            @close="closeBoxOverlay"
        />
      </v-dialog>
      <v-card
          class="d-flex flex-column fill-height"
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
          <qr-code-filter
              :pre-selected="preselectedBox !== undefined"
              v-model:search="search"
              pre-selection-close-action="/storage/boxes"
              :pre-selection-title="$t('boxes.prefiltered', {box: filteredFrom})"
              :storage="allBoxes"
          />
        </v-card-title>
        <v-card-text
            class="d-flex position-relative flex-1-1"
        >
          <div class="scroller-wrapper">
            <recycle-scroller
                ref="scroller"
                class="scroller"
                :buffer="0"
                :item-size="90"
                :items="filteredBoxes"
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
                        :type="StorageTypes.Box"
                        @click.stop="showBoxContent(item)"
                    >
                    </storage-card>
                  </v-col>
                </v-row>

              </template>
              <template #after v-if="preselectedBox === undefined">
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
                          v-if="loadingBoxes"
                        >
                          {{ $t('boxes.loading') }}
                        </p>
                        <p
                            class="pb-1"
                            v-else-if="allBoxes.length !== 0 && filteredBoxes.length !== 0"
                        >
                          {{ $t('boxes.all_displayed') }}
                        </p>
                        <p
                            class="pb-1"
                            v-else-if="allBoxes.length !== 0 && filteredBoxes.length === 0"
                        >
                          {{ $t('boxes.no_matches')}}
                        </p>
                        <p
                            class="pb-1"
                            v-else
                        >
                          {{ $t('boxes.no_boxes')}}
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
                            v-if="allBoxes.length === 0 && !loadingBoxes"
                        >
                          {{ $t('boxes.no_matches') }}
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