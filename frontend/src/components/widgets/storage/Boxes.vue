<script setup lang="ts">

import {computed, onMounted, ref, watch} from "vue";
import {ApiStorage, StorageTypes} from "@/types/api.ts";
import {useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {BoxEndpoint} from "@/api/http";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import {onBeforeRouteLeave} from "vue-router";

const storageStore = useStorage()
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const {t: $t} = useI18n()
const router = useRouter()
const route = useRoute()

provide('storageType', StorageTypes.Box)

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

const loadingBoxes = computed(() => storageStore.loadingStorage)
const search = ref("")

function showBoxContent(item: ApiStorage){
  storageStore.selectBox(item)
  //openDialog()
  router.push(`${route.fullPath}/box/${item.id}`)
}



// eslint-disable-next-line @typescript-eslint/no-unused-vars
watch(() => preselectedBox, (_: string|undefined, __: string|undefined) =>{
  //loadBoxes()
});

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
      <qr-code-filter
          :pre-selected="preselectedBox !== undefined"
          v-model:search="search"
          pre-selection-close-action="/boxes"
          :pre-selection-title="$t('boxes.prefiltered', {box: filteredFrom ?? $t('scan.from')})"
          @qr-selection-toggled="scrollToTop"
      />
    </v-card-title>
    <div
      class="flex-1-1 position-relative"
    >
      <v-card-text
          class="wrapper"
      >
        <recycle-scroller
              ref="scroller"
              class="scroll"
              :buffer="0"
              :item-size="85"
              :items="filteredBoxes"
              :emit-update="true"
              @update="hasScrolled"
          >
            <template v-slot="{item}">
              <storage-card
                  v-bind:storage="item"
                  :type="StorageTypes.Box"
                  @click.stop="showBoxContent(item)"
              >
              </storage-card>
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

      </v-card-text>

    </div>
  </v-card>
  <app-scroll-to-top-btn
    :scrolled-down="scrolledDown"
    @click.stop="scrollToTop"
  />
</template>

<style scoped lang="scss">

</style>