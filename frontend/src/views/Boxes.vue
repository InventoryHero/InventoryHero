<script lang="ts">
import {defineComponent, ref} from 'vue'
import BoxCard from "@/components/storage/box/BoxCard.vue";
import {useAuthStore, useConfigStore} from "@/store";

import { Box } from "@/types";
import useUpdateStorage from "@/composables/useUpdateStorage";
import AppScrollToTopBtn from "@/components/ui/AppScrollToTopBtn.vue";
import useNewAxios from "@/composables/useNewAxios.ts";
import {BoxEndpoint} from "@/api/http";

export default defineComponent({
  name: "Boxes",
  components: {
    AppScrollToTopBtn,
    BoxCard
  },
  setup(){
    const authData = useAuthStore()
    const config = useConfigStore()
    const {axios} = useNewAxios("box")
    return {authData, config, axios: axios as BoxEndpoint}
  },
  watch:{
    async preselectedBox(){
      this.boxes = []
      await this.loadBoxes()
    },
  },
  props:{
    preselectedBox:{
      type: String,
      default: undefined
    },
    filteredFrom:{
      type: String,
      default: undefined
    }
  },
  data(){
    return {
      loadingBoxes: true,
      boxes: [] as Array<Box>,
      search: '',
      overlayBox: undefined as Box|undefined,
      selectForQrCodePrinting: false,
      visibleStartIdx: 0
    }
  },
  computed: {
    filteredItems() {
      if (this.search === "") {
        return this.boxes
      }
      return this.boxes.filter(box => box.name.toLowerCase().includes(this.search.toLowerCase()))
    },
    scrolledDown(){
      return this.visibleStartIdx !== 0
    }
  },
  methods:{
    async loadBoxes(){
      this.loadingBoxes = true;
      let data = await this.axios.getBoxes({
        id: this.preselectedBox,
        contained: true
      }) as Array<Box>
      this.loadingBoxes = false
      this.boxes = data


    },
    updateFilter(filter: string)
    {
      this.search = filter
    },
    updateOverlayProduct(item: Box)
    {
      this.overlayBox = item
    },
    async deleteBox(id: number){
      await this.loadBoxes()
    },
    async updateBox(toUpdate: Box)
    {

      const {storage, index} = useUpdateStorage(ref(this.boxes), toUpdate, ref(this.overlayBox))
      if(storage === undefined)
      {
        // load all boxes new
        this.$notify({
          'title': "error",
          "text": "An error occured, need to reload"
        })
        setTimeout(() => {
          this.overlayBox = undefined
          this.loadBoxes()
        }, 2000)
        return
      }

    },
    onUpdate (viewStartIndex: number, viewEndIndex: number, visibleStartIndex: number, visibleEndIndex: number) {
      this.visibleStartIdx = visibleStartIndex
    },
    scrollToTop(){
      this.$refs.scroller.scrollToItem(0)
    },
    boxContentChanged(currentBox: number, newBox: number|undefined){
      this.loadBoxes()
    }
  },
  async mounted(){
    await this.loadBoxes()
  }
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
        class="position-relative d-flex flex-column fill-height"
    >
      <box-overlay
        v-model="overlayBox"
        @deleted="deleteBox()"
        @updated="updateBox($event)"
        @content-changed="boxContentChanged"
      />

      <qr-code-filter
          class="flex-0-1"
          :pre-selected="preselectedBox !== undefined"
          :search="search"
          pre-selection-close-action="/storage/boxes"
          :pre-selection-title="$t('boxes.prefiltered', {box: filteredFrom})"
          @update-filter="updateFilter"
          :storage="boxes"
      />
      <v-card
          ref="wrapper"
          class="mt-4 flex-1-1"
      >
        <v-progress-linear
            :indeterminate="true"
            :active="loadingBoxes"
            color="primary"
        />
        <v-card-text
          class="pt-1 pl-0 pr-0 pb-0"
        >
          <app-scroll-to-top-btn
              v-model="scrolledDown"
              @click="scrollToTop()"
          />
          <recycle-scroller
              ref="scroller"
              :item-size="90"
              :buffer="0"
              :items="filteredItems"
              style="height: 100%;"
              :emit-update="true"
              @update="onUpdate"
          >
            <template #default="{item}">

              <v-row
                  :no-gutters="true"
                  justify="center"
              >
                <v-col
                    cols="11"
                >
                  <box-card
                      @show-overlay="updateOverlayProduct(item)"
                      :id="item.id"
                      :name="item.name"
                      :creation-date="item.creation_date"
                      :product-amount="item.products ?? 0"
                  >
                  </box-card>
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
                          v-if="boxes.length !== 0 && filteredItems.length !== 0"
                      >
                        {{ $t('boxes.all_displayed') }}
                      </p>
                      <p
                          class="pb-1"
                          v-else-if="boxes.length !== 0 && filteredItems.length === 0"
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
                          v-if="boxes.length === 0 && !loadingBoxes"
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
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">


.v-card-text {
  overflow: hidden;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

</style>