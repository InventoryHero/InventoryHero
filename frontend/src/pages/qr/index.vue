<script setup lang="ts">
import { ref, reactive, defineComponent } from 'vue';
import {BoxResponseSchema, RoomResponseSchema} from "@/api/types/storage.ts";
import useAppStyling from "@/composables/useAppStyling.ts";
const {t} = useI18n();
const {storage} = useAxios()
const {mdAndUp} = useDisplay()
const {btnStyle, textFieldStyling} = useAppStyling()

const tab = ref<'rooms'|'boxes'|'items'>('rooms')
const search = ref<string|null|undefined>('')
const selectedItems = ref<{[key: string]: boolean}>({})
const stage = ref<"selectObject"|"designLabels">("selectObject")

const rooms = ref<Array<RoomResponseSchema>>([])
const boxes = ref<Array<BoxResponseSchema>>([])
const filteredRooms = computed(() => {
  if(!search.value || search.value === ""){
    return rooms.value
  }
  return rooms.value.filter(x => x.name.includes(search.value!))
})
const filteredBoxes = computed(() => {
  if(!search.value || search.value === ""){
    return boxes.value
  }
  return boxes.value.filter(x => x.name.includes(search.value!))
})

const numSelectedRooms = computed(() => getSelectedCountByPrefix('room-'))
const numSelectedBoxes = computed(() => getSelectedCountByPrefix('box-'))

const getSelectedCountByPrefix = (prefix: string) => {
  return Object.keys(selectedItems.value).filter(key =>
      key.startsWith(prefix) && selectedItems.value[key]
  ).length
}

watch(tab, () => {
  search.value = ""
})

onBeforeMount(() => {
  storage.getAllStorage("room").then(({success, data, error}) => {
    if(!success){
      // TODO
    }
    rooms.value = (data ?? []) as Array<RoomResponseSchema>
  })

  storage.getAllStorage("box").then(({success, data, error}) => {
    if(!success){
      // TODO
    }
    boxes.value = (data ?? []) as Array<BoxResponseSchema>
  })
})
</script>



<template>
  <v-container
      fluid
      class="pa-0 fill-width"
      v-if="stage === 'selectObject'"
  >
    <v-row
      justify="center"

    >
      <v-col
          cols="12"
          lg="10"
      >
        <p class="text-h4 font-weight-bold">{{ t('qr.label.title_1') }}</p>
        <p class="text-grey-lighten-1">{{ t('qr.label.description_1') }}</p>

        <div class="d-flex overflow-x-scroll ga-2 mt-4 mb-4">
          <v-btn
              rounded="lg"
              :variant="tab === 'rooms' ? 'tonal' : 'flat'"
              :color="tab === 'rooms' ? 'primary' : 'grey-darken-3'"
              @click="tab = 'rooms'"
              :text="t('qr.label.tabs.room', {
                      amount: rooms.length,
                      selected: numSelectedRooms
                    })"
          />
          <v-btn
              rounded="lg"
              :variant="tab === 'boxes' ? 'tonal' : 'flat'"
              :color="tab === 'boxes' ? 'primary' : 'grey-darken-3'"
              @click="tab = 'boxes'"
              :text="t('qr.label.tabs.box', {
                amount: boxes.length,
                selected: numSelectedBoxes
              })"

          />
          <!-- TODO IMPLEMENT THIS FOR SCANNING -->
          <v-btn
              v-if="false"
              rounded="lg"
              :variant="tab === 'items' ? 'tonal' : 'flat'"
              :color="tab === 'items' ? 'primary' : 'grey-darken-3'"
              @click="tab = 'items'"
              text="Items"
          />
        </div>
        <v-card elevation="4">
          <v-card-text>
            <v-text-field
                v-bind="textFieldStyling"
                v-model="search"
                :label="t(`qr.label.search_${tab}`)"
                prepend-inner-icon="mdi-magnify"
            />

            <!-- Scrollable List of Items -->
            <v-tabs-window
                v-model="tab"
            >
              <v-tabs-window-item
                  value="rooms"
              >
                <tab-view
                    v-model="selectedItems"
                    :objects="filteredRooms"
                    :num-selected-objects="numSelectedRooms"
                    type="room"
                />
              </v-tabs-window-item>
              <v-tabs-window-item
                  value="boxes"
              >
                <tab-view
                  v-model="selectedItems"
                  :objects="filteredBoxes"
                  :num-selected-objects="numSelectedBoxes"
                  type="box"
                />
              </v-tabs-window-item>
            </v-tabs-window>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col
        cols="12"
        lg="10"
        class="d-flex justify-end"
      >
        <v-btn
            v-bind="btnStyle"
            elevation="4"
            append-icon="mdi-chevron-right"
            :text="t('qr.label.customization_stage')"
            :disabled="numSelectedBoxes === 0 && numSelectedRooms === 0"
            @click="stage = 'designLabels'"
        />
      </v-col>
    </v-row>
  </v-container>
  <v-container
      fluid
      class="pa-0 fill-width"
      v-else-if="stage === 'designLabels'"
      height="55vh"
  >
    <v-row>
      <!-- Left Column: Customization -->
      <v-col cols="12" lg="5">
        <v-card class="pa-2" elevation="4">
          <v-card-text>
            <h2 class="text-h6 font-weight-semibold mb-4">2. Customize Label</h2>
            <v-row>
              <v-col cols="12" md="6">
                <v-select label="Label Size" :items="['Avery 5160 (30 per page)', '4x6 Shipping Label', '2x2 Square Label']" variant="outlined" density="compact" hide-details></v-select>
              </v-col>
              <v-col cols="12" md="6" class="d-flex align-center">
                <v-checkbox-btn label="Include item description" hide-details></v-checkbox-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Right Column: Desktop Page Preview -->
      <v-col cols="7" class="d-none d-lg-block">
        <page-preview
            v-model="selectedItems"
            :boxes="boxes"
            :rooms="rooms"
        />
      </v-col>
    </v-row>
  </v-container>
</template>



<style scoped>


.sticky-footer {
  background: linear-gradient(180deg, rgba(30, 30, 30, 0.7) 0%, rgb(var(--v-theme-surface)) 50%);
  backdrop-filter: blur(8px);
}
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

<route>
{
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": true,
    "title": "titles.qr"
  }
}
</route>