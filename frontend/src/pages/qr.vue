<template>
  <v-container
    fluid
    class="pa-0 fill-width"
    height="88svh"
  >
    <v-tabs-window
      v-model="stage"
      class="fill-height"
    >
      <v-tabs-window-item
        value="selectObjects"
        class="fill-height"
      >
        <v-row
          justify="center"
          dense
        >
          <v-col cols="12">
            <p class="text-h4 font-weight-bold">{{ t('qr.label.title_1') }}</p>
            <p class="text-grey-lighten-1">{{ t('qr.label.description_1') }}</p>

            <div class="d-flex overflow-x-scroll ga-2 mt-4">
              <v-btn
                rounded="lg"
                :variant="tab === 'rooms' ? 'tonal' : 'flat'"
                :color="tab === 'rooms' ? 'primary' : 'grey-darken-3'"
                @click="tab = 'rooms'"
                :text="
                  t('qr.label.tabs.room', {
                    amount: rooms.length,
                    selected: numSelectedRooms
                  })
                "
              />
              <v-btn
                rounded="lg"
                :variant="tab === 'boxes' ? 'tonal' : 'flat'"
                :color="tab === 'boxes' ? 'primary' : 'grey-darken-3'"
                @click="tab = 'boxes'"
                :text="
                  t('qr.label.tabs.box', {
                    amount: boxes.length,
                    selected: numSelectedBoxes
                  })
                "
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
          </v-col>
        </v-row>
        <v-row
          justify="center"
          :style="{
            height: mdAndUp ? '75%' : '65%'
          }"
        >
          <v-col
            cols="12"
            class="fill-height"
          >
            <v-tabs-window
              v-model="tab"
              class="fill-height"
            >
              <v-tabs-window-item
                value="rooms"
                class="fill-height"
              >
                <tab-view
                  v-model="selectedItems"
                  :objects="rooms"
                  :num-selected-objects="numSelectedRooms"
                  type="room"
                />
              </v-tabs-window-item>
              <v-tabs-window-item
                value="boxes"
                class="fill-height"
              >
                <tab-view
                  v-model="selectedItems"
                  :objects="boxes"
                  :num-selected-objects="numSelectedBoxes"
                  type="box"
                />
              </v-tabs-window-item>
            </v-tabs-window>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
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
      </v-tabs-window-item>
      <v-tabs-window-item
        value="designLabels"
        class="fill-height"
      >
        <v-row dense>
          <v-col cols="12">
            <p class="text-h4 font-weight-bold">{{ t('qr.label.title_2') }}</p>
            <p class="text-grey-lighten-1">{{ t('qr.label.description_2') }}</p>
            <div class="d-flex overflow-x-scroll ga-2 mt-4">
              <v-btn
                prepend-icon="mdi-arrow-left"
                :text="t('qr.label.back')"
                variant="plain"
                @click="stage = 'selectObjects'"
              />
            </div>
          </v-col>
        </v-row>
        <v-row
          :style="{
            height: mdAndUp ? '75%' : '65%'
          }"
        >
          <v-col
            cols="12"
            lg="5"
            class="fill-height"
          >
            <page-configuration />
          </v-col>

          <!-- Right Column: Desktop Page Preview -->
          <v-col
            cols="7"
            class="fill-height"
            v-if="mdAndUp"
          >
            <page-preview
              v-model="selectedItems"
              :boxes="boxes"
              :rooms="rooms"
            >
              <template v-slot:default="{ print }">
                <v-row class="mt-2">
                  <v-col
                    cols="12"
                    class="d-flex justify-end"
                  >
                    <v-btn
                      v-bind="btnStyle"
                      elevation="4"
                      prepend-icon="mdi-printer"
                      :text="t('qr.label.print')"
                      @click="print"
                    />
                  </v-col>
                </v-row>
              </template>
            </page-preview>
          </v-col>
        </v-row>

        <v-row v-if="!mdAndUp">
          <v-col
            cols="12"
            class="d-flex justify-end"
          >
            <v-dialog
              v-model="mobileDialogVisible"
              height="90vh"
              width="90vw"
            >
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="{
                    ...props,
                    ...btnStyle
                  }"
                  :text="t('qr.label.show_print_modal')"
                />
              </template>
              <v-card
                elevation="0"
                class="pa-4"
              >
                <page-preview
                  v-model="selectedItems"
                  :boxes="boxes"
                  :rooms="rooms"
                  ref="pagePreview"
                >
                  <template v-slot:default="{ print }">
                    <v-row class="mt-2">
                      <v-col
                        cols="12"
                        class="d-flex justify-end"
                      >
                        <v-btn
                          @click="mobileDialogVisible = false"
                          class="me-2"
                          :text="t('qr.label.close_print_dialog')"
                        />

                        <v-btn
                          v-bind="btnStyle"
                          elevation="4"
                          prepend-icon="mdi-printer"
                          :text="t('qr.label.print')"
                          @click="print"
                        />
                      </v-col>
                    </v-row>
                  </template>
                </page-preview>
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  BoxResponseSchema,
  RoomResponseSchema,
  StorageType
} from '@/api/types/storage.ts'
import useAppStyling from '@/composables/useAppStyling.ts'
import PageConfiguration from '@/components/qr/PageConfiguration.vue'

definePage({
  meta: {
    requiresAuth: true,
    requiresHousehold: true,
    title: 'titles.qr',
    layout: 'default'
  }
})

const { t } = useI18n()
const { storage } = useAxios()
const { mdAndUp } = useDisplay()
const { btnStyle } = useAppStyling()

const tab = ref<'rooms' | 'boxes' | 'items'>('rooms')
const stage = ref<'selectObjects' | 'designLabels'>('selectObjects')
const mobileDialogVisible = ref<boolean>(false)

const selectedItems = ref<{ [key in StorageType]: Array<string> }>({
  room: [],
  box: []
})

const rooms = ref<Array<RoomResponseSchema>>([])
const boxes = ref<Array<BoxResponseSchema>>([])

const numSelectedRooms = computed(() => selectedItems.value['room'].length)
const numSelectedBoxes = computed(() => selectedItems.value['box'].length)

onBeforeRouteLeave(() => {
  if (mobileDialogVisible.value) {
    mobileDialogVisible.value = false
    return false
  }
})

onBeforeMount(() => {
  storage.getAllStorage('room').then(({ success, data }) => {
    if (!success) {
      return
    }
    rooms.value = (data ?? []) as Array<RoomResponseSchema>
  })

  storage.getAllStorage('box').then(({ success, data }) => {
    if (!success) {
      return
    }
    boxes.value = (data ?? []) as Array<BoxResponseSchema>
  })
})
</script>

<style scoped></style>
