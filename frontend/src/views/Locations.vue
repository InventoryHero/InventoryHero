<script lang="ts">
import {defineComponent, ref} from "vue";
import {useAuthStore, useConfigStore} from "@/store";
import {Location} from "@/types";
import useUpdateStorage from "@/composables/useUpdateStorage";
import useNewAxios from "@/composables/useAxios.ts";
import {LocationEndpoint} from "@/api/http";

export default defineComponent({
  name:"Locations",
  components: {},
  setup(){
    const authData = useAuthStore()
    const config = useConfigStore()
    const {axios} = useNewAxios("location")
    return {authData, config, axios: axios as LocationEndpoint}
  },
  watch: {
    async preselectedLocation() {
      this.overlayLocation = undefined
      this.locations = []
      await this.loadLocations()
    }
  },
  props:{
    preselectedLocation:{
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
      loadingLocations: false,
      search: "",
      locations: [] as Array<Location>,
      overlayLocation: undefined as Location | undefined,
      visibleStartIdx: 0
    }
  },
  computed: {
    filteredItems() {
      if (this.search === "") {
        return this.locations
      }
      return this.locations.filter(box => box.name.toLowerCase().includes(this.search.toLowerCase()))
    },
    scrolledDown(){
      return this.visibleStartIdx !== 0
    }
  },
  methods:{
    async loadLocations(){
      this.loadingLocations = true
      this.locations = await this.axios.getLocations({
        id: this.preselectedLocation,
        contained: true
      })
      this.loadingLocations = false
    },
    updateFilter(filter: string)
    {
      this.search = filter
    },
    updateOverlayLocation(item: Location, event: boolean)
    {
      if(event)
      {
        this.overlayLocation = item
      }
      else
      {
        this.overlayLocation = undefined
      }
    },
    updateLocation(toUpdate: Location){
      const {storage, index} = useUpdateStorage(ref(this.locations), toUpdate, ref(this.overlayLocation))
      if(storage === undefined)
      {
        // load all boxes new
        this.$notify({
          'title': "error",
          "text": "An error occured, need to reload"
        })
        setTimeout(() => {
          this.overlayLocation = undefined
          this.loadLocations()
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
    contentChanged(id: number, newId: number|undefined){
      this.loadLocations()
    }
  },
  async mounted(){
    await this.loadLocations()
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
    lg="8"
    class="position-relative d-flex flex-column fill-height"
  >
    <location-overlay
        v-model="overlayLocation"
        @box-moved="loadLocations()"
        @box-deleted="loadLocations()"
        @deleted="loadLocations()"
        @updated="updateLocation($event)"
        @content-changed="contentChanged"
    />

    <qr-code-filter
        class="flex-0-1"
        :pre-selected="preselectedLocation !== undefined"
        :search="search"
        pre-selection-close-action="/storage/boxes"
        :pre-selection-title="$t('locations.prefiltered', {prefilter: filteredFrom})"
        @update-filter="updateFilter"
        :storage="locations"
    />
    <v-card
        ref="wrapper"
        class="mt-4 flex-1-1"
    >
      <v-progress-linear
          :indeterminate="true"
          :active="loadingLocations"
          color="primary"
      />
      <v-card-text
          class="pt-1 pl-0 pr-0 pb-0"
      >
        <app-scroll-to-top-btn
            v-model="scrolledDown"
            @click="scrollToTop()"
        />
        <RecycleScroller
            ref="scroller"
            :item-size="110"
            :buffer="0"
            :items="filteredItems"
            style="height: 100%;"
            :emit-update="true"
            @update="onUpdate"
        >
          <template #default="{item}">
            <location-card
                :id="item.id"
                :name="item.name"
                :creation-date="item.creation_date"
                :product-amount="item.products ?? 0"
                :boxes-amount="item.boxes ?? 0"
                @show-overlay="updateOverlayLocation(item, true)"
            >
            </location-card>
          </template>
          <template #after>
            <v-row
                :no-gutters="true"
                justify="center"
            >

              <v-card
                  :elevation="0"
              >
                <v-card-title
                    class="text-center text-wrap"
                >
                  <p
                      class="pb-1"
                      v-if="locations.length !== 0 && filteredItems.length !== 0"
                  >
                    {{ $t('locations.all_displayed') }}
                  </p>
                  <p
                      class="pb-1"
                      v-else-if="locations.length !== 0 && filteredItems.length === 0"
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
            </v-row>
          </template>
        </RecycleScroller>
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