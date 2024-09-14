<script setup lang="ts">
import {usePrintSettings} from "@/store";
import {StorageIconSizes} from "@/store/printSettings";

const printSettingStore = usePrintSettings();
const {t: $t} = useI18n()

const qrCodeSettingsVisible = ref(false)

const storageTypeSizes = ref([
  {"size": "x-small", "text": $t('print.storage_icon_sizes.x-small')},
  {"size": "small", "text": $t('print.storage_icon_sizes.small')},
  {"size": "default", "text": $t('print.storage_icon_sizes.medium')},
  {"size": "large", "text": $t('print.storage_icon_sizes.large')},
  {"size": "x-large", "text": $t('print.storage_icon_sizes.x-large')}
])

const storageLabelVisible = computed({
  get(){
    return printSettingStore.storageLabelVisible
  },
  set(value: boolean){
    printSettingStore.setStorageLabel(value)
  }
})
const storageNameVisible = computed({
  get(){
    return printSettingStore.storageNameVisible
  }, set(value: boolean){
    printSettingStore.setStorageNameVisible(value)
  }
})
const storageIconVisible = computed({
  get(){
    return printSettingStore.storageIconVisible
  }, set(value: boolean){
    printSettingStore.setStorageIconVisible(value)
  }
})
const borderThickness = computed({
  get(){
    return printSettingStore.borderThickness
  }, set(value: number){
    printSettingStore.setBorderThickness(value)
  }
})
const qrCodeVisible = computed({
  get(){
    return printSettingStore.qrCodeVisible
  }, set(value: boolean){
    printSettingStore.setQrCodeVisible(value)
  }
})
const qrCodeIconVisible = computed({
  get(){
    return printSettingStore.qrCodeIconVisible
  }, set(value: boolean){
    printSettingStore.setQrCodeIconVisible(value)
  }
})
const qrCodeIconWidth = computed({
  get(){
    return printSettingStore.qrCodeIconWidth
  }, set(value: number){
    printSettingStore.setQrCodeIconWidth(value)
  }
})
const storageIconSize = computed({
  get(){
    return printSettingStore.storageIconSize
  },
  set(value: StorageIconSizes){
    printSettingStore.setStorageIconSize(value)
  }
})
const fontSize = computed({
  get(){
    return printSettingStore.fontSize
  }, set(value: number){
    printSettingStore.setFontSize(value)
  }
})

</script>

<template>
  <v-card>
    <v-card-title
        :class="{
          'shadowed': qrCodeSettingsVisible,
        }"
        class="d-flex justify-space-between pa-0 pl-2 pr-2"
    >
      {{ $t('print.qr_code_settings.title')}}
      <app-icon-btn
          @click="qrCodeSettingsVisible=!qrCodeSettingsVisible"
          :icon="qrCodeSettingsVisible ? 'mdi-menu-up' : 'mdi-menu-down'"
      />
    </v-card-title>
    <v-expand-transition>
      <div
          v-if="qrCodeSettingsVisible"
          class="mt-2"
      >
        <app-setting
            :title="$t('print.qr_code_settings.print_label')"
        >
          <v-checkbox
              :hide-details="true"
              density="compact"
              color="primary"
              v-model="storageLabelVisible"
          />
        </app-setting>
        <app-setting
            :title="$t('print.qr_code_settings.show_title')"
        >
          <v-checkbox
              :hide-details="true"
              density="compact"
              color="primary"
              :disabled="!storageLabelVisible"
              v-model="storageNameVisible"
          />
          <template v-slot:subTitle2>
            <v-slider
                v-model="fontSize"
                :max="20"
                :min="4"
                :step="1"
                show-ticks
                color="primary"
                :disabled="!storageNameVisible || !storageLabelVisible"
            />
          </template>
        </app-setting>
        <v-divider/>
        <app-setting
            :r-cols="3"
            :title="$t('print.qr_code_settings.storage_type_icon')"
        >
          <v-checkbox
              :hide-details="true"
              density="compact"
              color="primary"
              v-model="storageIconVisible"
              :disabled="!storageLabelVisible"
          />
          <template v-slot:subTitle2>
            <v-select
                v-model="storageIconSize"
                :items="storageTypeSizes"
                :label="$t('print.qr_code_settings.storage_type_icon_size')"
                density="compact"
                item-value="size"
                item-title="text"
                :disabled="!storageIconVisible || !storageLabelVisible"
            />
          </template>
        </app-setting>
        <v-divider/>
        <app-setting
            :r-cols="2"
            :title="$t('print.qr_code_settings.border_thickness')"
        >
          <v-text-field
              type="number"
              v-model.number="borderThickness"
              disabled
              hide-details
              density="compact"
              variant="solo-filled"
              color="primary"
          />
          <template v-slot:subTitle2>
            <v-slider
                v-model="borderThickness"
                :max="8"
                :min="0"
                :step="1"
                show-ticks
                color="primary"
            >
            </v-slider>
          </template>
        </app-setting>
        <v-divider/>
        <app-setting
            :r-cols="3"
            :title="$t('print.qr_code_settings.show_qr_code')"
        >
          <v-checkbox
              :hide-details="true"
              density="compact"
              color="primary"
              v-model="qrCodeVisible"
          />
        </app-setting>
        <v-divider/>
        <app-setting
            :r-cols="2"
            :title="$t('print.qr_code_settings.qr_code_icon')"
        >
          <v-checkbox
              :hide-details="true"
              density="compact"
              color="primary"
              v-model="qrCodeIconVisible"
              :disabled="!qrCodeVisible"
          />
          <template v-slot:subTitle2>
            <v-slider
                :disabled="!qrCodeIconVisible || !qrCodeVisible"
                v-model="qrCodeIconWidth"
                :max="50"
                :min="0"
                :step="10"
                show-ticks
                color="primary"
            >
            </v-slider>
          </template>
        </app-setting>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<style scoped lang="scss">

</style>