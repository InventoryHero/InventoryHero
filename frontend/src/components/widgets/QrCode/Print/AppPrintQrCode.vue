<script lang="ts">
import {defineComponent, ref, StyleValue} from 'vue'
import  {Level, RenderAs } from 'qrcode.vue'
import {downloadQrCodeImage} from "@/api/XhrRequests.ts";
import {useVueToPrint} from "vue-to-print";
import {Storage} from "@/types";

export default defineComponent({
  name: "AppPrintQrCode",
  emits:{
    closePrint(){
      return true;
    }
  },
  props:{
    activatorIcon: {
      type: String,
      default: "mdi-qrcode"
    },
    activatorSize:{
      type: String,
      default: undefined
    },
    title:{
      type: String,
      default: ''
    },
    modelValue:{
      type: Boolean
    },
    storage:{
      type: Array<Storage>,
      default: []
    }
  },
  computed:{
    logo(){
      return "/favicon.ico"
    },
    toPrint(){
      return this.storage
    },
    pagePreviewStyle(): StyleValue{
      return {
        display: this.showPagePreview ? "block" : "none",
        overflow: "auto",
        height: "70svh",
        margin: "16px"

      }
    },
    testData(): Storage {
      return {
        id: -1,
        household_id: "-1",
        name: this.$t('print.example_storage'),
        type: 1,
        creation_date: ""
      } as Storage
    },
    qrCodePreviewStyle(): StyleValue{
      return {
        flex: "0 1 auto",
      }
    }

  },
  data(){
    return {
      level: ref<Level>('M'),
      renderAs: ref<RenderAs>('canvas'),
      showQr: false,
      vueQrDownload: "",
      showPagePreview: false,
      settings: {
        showTitle: true,
        showStorageTypeIcon: true,
        showBorder: true,
        qrCodeIcon: true,
        printLabel: true,
        itemsPerRow: 3,
        borderColor: 'primary',
        marginTop: 10,
        marginBottom: 10,
        marginRight: 10,
        marginLeft: 10,
        previewScale: 0.5,
      },
      qrCodeSettingsVisible: false,
      pageSettingsVisible: false
    }
  },
  methods: {
    vueToPrint(){
      const { handlePrint } = useVueToPrint({
        content: () => this.$refs.componentRef,
        removeAfterPrint: true
      });
      handlePrint()
    },
    showPreview(){
      this.showPagePreview = true;
    },
  },

})
</script>

<template>
  <template v-if="modelValue">
    <div v-bind="$attrs" :style="pagePreviewStyle" ref="componentRef">
      <app-print-preview
          class="print-preview"
          :style="`transform: scale(${settings.previewScale})`"
          v-model="toPrint"
          v-bind="settings"
      />
    </div>

    <v-card-text
        v-if="!showPagePreview"
        class="preview-settings"
        v-bind="$attrs"
    >

      <app-storage-qr-code
          :storage="testData"
          :show-title="settings.showTitle"
          :show-storage-type-icon="settings.showStorageTypeIcon"
          :show-border="settings.showBorder"
          :print-label="settings.printLabel"
          :style="qrCodePreviewStyle"
          :show-qr-code-icon="settings.qrCodeIcon"

      />
      <div
          style="overflow: auto !important; flex: 1 1 auto;"
          class="mt-4"
      >
        <v-card
            :elevation="8"
            density="compact"
        >
          <v-card-title
              :class="{
                'shadowed': qrCodeSettingsVisible
              }"
          >
            <v-row :no-gutters="true">
              <v-col
                  class="d-flex justify-start align-center"
              >
                {{ $t('print.qr_code_settings')}}
              </v-col>
              <v-col
                  cols="1"
                  class="d-flex justify-end align-center"
              >
                <app-icon-btn
                    @click="qrCodeSettingsVisible=!qrCodeSettingsVisible"
                    :icon="qrCodeSettingsVisible ? 'mdi-menu-up' : 'mdi-menu-down'"
                    size="large"
                />
              </v-col>
            </v-row>
          </v-card-title>
          <div
              v-if="qrCodeSettingsVisible"
          >
            <app-setting
                :title="$t('print.print_label')"
            >
              <v-checkbox
                  :hide-details="true"
                  density="compact"
                  color="primary"
                  v-model="settings.printLabel"
              />
            </app-setting>
            <app-setting
                :title="$t('print.show_title')"
            >
              <v-checkbox
                  :hide-details="true"
                  density="compact"
                  color="primary"
                  v-model="settings.showTitle"
              />
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.show_storage_type_icon')"
            >
              <v-checkbox
                  :hide-details="true"
                  density="compact"
                  color="primary"
                  v-model="settings.showStorageTypeIcon"
              />
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.show_border')"
            >
              <v-checkbox
                  :hide-details="true"
                  density="compact"
                  color="primary"
                  v-model="settings.showBorder"
              />
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.show_qr_code_icon')"
            >
              <v-checkbox
                  :hide-details="true"
                  density="compact"
                  color="primary"
                  v-model="settings.qrCodeIcon"
              />
            </app-setting>
          </div>
        </v-card>
        <v-card
            :elevation="8"
            density="compact"
            class="mt-4"
        >
          <v-card-title
              :class="{
              'shadowed': pageSettingsVisible
            }"
          >
            <v-row :no-gutters="true" justify="center">
              <v-col
                class="d-flex justify-start align-center"
              >
                {{ $t('print.page_settings')}}
              </v-col>
              <v-col
                  cols="1"
                  class="d-flex justify-end align-center"
              >
                <app-icon-btn
                    @click="pageSettingsVisible=!pageSettingsVisible"
                    :icon="pageSettingsVisible ? 'mdi-menu-up' : 'mdi-menu-down'"
                    size="large"
                />
              </v-col>
            </v-row>
          </v-card-title>
          <template v-if="pageSettingsVisible">
            <app-setting
                :r-cols="3"
                :title="$t('print.preview_scale')"
            >
              <v-text-field
                  type="number"
                  v-model.number="settings.previewScale"
                  :hide-details="true"
                  density="compact"
                  variant="solo-filled"
                  color="primary"
                  :disabled="true"
              />
              <template #subTitle2>
                <v-slider
                    v-model="settings.previewScale"
                    :max="1"
                    :min="0.01"
                    :step="0.01"
                    :hide-details="true"
                    density="compact"
                    color="primary"
                />
              </template>
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.items_per_row')"
            >
              <v-text-field
                  type="number"
                  v-model.number="settings.itemsPerRow"
                  :hide-details="true"
                  density="compact"
                  variant="solo-filled"
                  color="primary"
                  :disabled="true"
              />
              <template #subTitle2>
                <v-slider
                    v-model="settings.itemsPerRow"
                    :max="5"
                    :min="1"
                    :step="1"
                    :hide-details="true"
                    density="compact"
                    color="primary"
                />
              </template>
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.margin_top')"
            >
              <v-text-field
                  type="number"
                  v-model.number="settings.marginTop"
                  :hide-details="true"
                  density="compact"
                  variant="solo-filled"
                  color="primary"
                  :disabled="true"
              />
              <template #subTitle2>
                <v-slider
                    v-model="settings.marginTop"
                    :max="10"
                    :min="1"
                    :step="1"
                    :hide-details="true"
                    density="compact"
                    color="primary"
                />
              </template>
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.margin_bottom')"
            >
              <v-text-field
                  type="number"
                  v-model.number="settings.marginBottom"
                  :hide-details="true"
                  density="compact"
                  variant="solo-filled"
                  color="primary"
                  :disabled="true"
              />
              <template #subTitle2>
                <v-slider
                    v-model="settings.marginBottom"
                    :max="10"
                    :min="1"
                    :step="1"
                    :hide-details="true"
                    density="compact"
                    color="primary"
                />
              </template>
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.margin_right')"
            >
              <v-text-field
                  type="number"
                  v-model.number="settings.marginRight"
                  :hide-details="true"
                  density="compact"
                  variant="solo-filled"
                  color="primary"
                  :disabled="true"
              />
              <template #subTitle2>
                <v-slider
                    v-model="settings.marginRight"
                    :max="10"
                    :min="1"
                    :step="1"
                    :hide-details="true"
                    density="compact"
                    color="primary"
                />
              </template>
            </app-setting>
            <v-divider/>
            <app-setting
                :r-cols="3"
                :title="$t('print.margin_left')"
            >
              <v-text-field
                  type="number"
                  v-model.number="settings.marginLeft"
                  :hide-details="true"
                  density="compact"
                  variant="solo-filled"
                  color="primary"
                  :disabled="true"
              />
              <template #subTitle2>
                <v-slider
                    v-model="settings.marginLeft"
                    :max="10"
                    :min="1"
                    :step="1"
                    :hide-details="true"
                    density="compact"
                    color="primary"
                />
              </template>
            </app-setting>
          </template>
        </v-card>
      </div>

    </v-card-text>
    <v-card-actions
        :class="{
      'justify-space-between': showPagePreview,
      'justify-start': !showPagePreview
    }"
    >
      <v-btn
          @click="showPreview()"
          v-if="!showPagePreview"
      >
        {{$t('print.show_preview')}}
      </v-btn>
      <v-btn
          v-else
          @click="showPagePreview=false"
      >
        {{$t('print.close_preview')}}
      </v-btn>
      <v-btn
          @click="vueToPrint()"
          v-if="showPagePreview"
      >
        {{$t('print.print')}}
      </v-btn>
    </v-card-actions>



  </template>
</template>

<style scoped lang="scss">
.qr-code{
  background-color: white;
  color: black;
}

.preview-settings{
  display: flex;
  flex-flow: column;
  overflow: hidden;
  height: 70svh;
}


.print-preview{

  transform-origin: top left;
  display: block;
  border: 2px solid black;

}

@media print {
  @page {
    size: auto;
    margin: 0;
  }
  .print-preview {
    border: unset;
    transform: scale(1) !important;
  }
  .print-page {
    page-break-before: auto;
  }
  @media screen {
    .print-page {
      margin-top: 10mm;
    }
  }
}
</style>