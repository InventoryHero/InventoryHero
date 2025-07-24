<script setup lang="ts">
import {storeToRefs} from "pinia";
import usePrintSettingsStore, {paperSizes} from "@/store/usePrintSettingsStore.ts";
import useAppStyling from "@/composables/useAppStyling.ts";

const printSettingStore = usePrintSettingsStore()
const {t} = useI18n()
const {numberInputStyling, selectStyling} = useAppStyling()

const {
  margins,
  borderThickness,
  rows,
  columns,
  paper,

  storageNameVisible,
  storageIconVisible,
  storageIconSize,
  qrCodeVisible,
  qrCodeIconVisible,
  qrCodeIconWidth,
  fontSize,
} = storeToRefs(printSettingStore)
</script>

<template>
  <v-card
      class="pa-2 fill-height"
      elevation="4"
  >
    <v-card-text
      class="fill-height overflow-auto"
    >
      <v-row>
        <v-col
            cols="12"
        >
          <v-select
              v-bind="selectStyling"
              v-model="paper"
              :items="Object.keys(paperSizes)"
              :label="t('qr.style.paper')"
              :clearable="false"
          />
        </v-col>

        <v-col
            cols="12"
        >
          <v-number-input
              v-bind="numberInputStyling"
              v-model="rows"
              :min="1"
              :max="8"
              :label="t('qr.style.rows')"
          />
        </v-col>
        <v-col
            cols="12"
        >
          <v-number-input
              v-bind="numberInputStyling"
              v-model="columns"
              :min="1"
              :max="5"
              :label="t('qr.style.cols')"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col
          cols="12"
        >
          <span class="text-subtitle-2 text-medium-emphasis">
            {{t('qr.style.margins.title')}}
          </span>
        </v-col>
        <number-input-slider
            v-model="margins.top"
            :title="t('qr.style.margins.top')"
            :unit="t('qr.style.margins.unit')"
        />
        <number-input-slider
            v-model="margins.right"
            :title="t('qr.style.margins.right')"
            :unit="t('qr.style.margins.unit')"
        />
        <number-input-slider
            v-model="margins.bottom"
            :title="t('qr.style.margins.bottom')"
            :unit="t('qr.style.margins.unit')"
        />
        <number-input-slider
            v-model="margins.left"
            :title="t('qr.style.margins.left')"
            :unit="t('qr.style.margins.unit')"
        />

        <number-input-slider
            v-model="borderThickness"
            :title="t('qr.style.border-thickness')"
            :min="0"
            :max="5"
            :step="1"
        />
      </v-row>
      <v-row>
        <v-col>
          label settings
        </v-col>
      </v-row>
      <v-row>
        <v-col
            cols="6"
        >
          <v-switch
              v-model="storageNameVisible"
              color="primary"
              :label="t('qr.style.name_visible')"
          />
        </v-col>
        <v-col
            cols="6"
        >
          <v-switch
              v-model="storageIconVisible"
              color="primary"
              :label="t('qr.style.icon_visible')"
          />
        </v-col>
        <v-col cols="6">
          <v-switch
              v-model="qrCodeVisible"
              color="primary"
              :label="t('qr.style.qr_visible')"
          />
        </v-col>
        <v-col cols="6">
          <v-switch
              v-model="qrCodeIconVisible"
              color="primary"
              :label="t('qr.style.qr_icon_visible')"
          />
        </v-col>
        <number-input-slider
            :disabled="!storageIconVisible"
            v-model="storageIconSize"
            :title="t('qr.style.label_icon_size')"
            :min="1"
            :max="50"
            :step="1"
        />
        <number-input-slider
            :disabled="!qrCodeIconVisible || !qrCodeVisible"
            v-model="qrCodeIconWidth"
            :title="t('qr.style.qr_code_icon_size')"
            :min="1"
            :max="50"
            :step="1"
        />
        <number-input-slider
            :disabled="!storageNameVisible"
            v-model="fontSize"
            :title="t('qr.style.font_size')"
            :min="1"
            :max="50"
            :step="1"
        />
      </v-row>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">

</style>