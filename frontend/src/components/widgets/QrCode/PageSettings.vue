<script setup lang="ts">
import {usePrintSettings} from "@/store"
import {Paper, supportedPapers} from "@/store/printSettings";
import MarginSetting from "@/components/widgets/QrCode/MarginSetting.vue";

const printSettingStore = usePrintSettings()
const pageSettingsVisible = ref(false)

const columns = computed({
  get(){
    return printSettingStore.columns
  },
  set(value: number){
    printSettingStore.setColumns(value)
  }
})

const rows = computed({
  get(){
    return printSettingStore.rows
  },
  set(value: number){
    printSettingStore.setRows(value)
  }
})

const paper = computed({
  get(){
    return printSettingStore.paper.name
  },
  set(value: Paper){
    printSettingStore.setPaper(value)
  }
})





</script>

<template>
  <v-card
  >
    <v-card-title
      :class="{
        'shadowed': pageSettingsVisible,
      }"
      class="d-flex justify-space-between pa-0 pl-2 pr-2"
    >
      {{ $t('print.page_settings.title')}}
      <app-icon-btn
          @click="pageSettingsVisible=!pageSettingsVisible"
          :icon="pageSettingsVisible ? 'mdi-menu-up' : 'mdi-menu-down'"
          size="large"
      />
    </v-card-title>
    <v-expand-transition>
      <div
          v-if="pageSettingsVisible"
          class="mt-2"
      >
        <app-setting
            :r-cols="7"
            :title="$t('print.page_settings.paper')"
        >
          <v-select
              v-model="paper"
              :items="supportedPapers"
              color="primary"
              density="compact"
              hide-details
          />

        </app-setting>
        <v-divider/>
        <app-setting
            :r-cols="2"
            :title="$t('print.page_settings.num_cols')"
        >
          <v-text-field
              type="number"
              v-model.number="columns"
              :hide-details="true"
              density="compact"
              variant="solo-filled"
              color="primary"
              :disabled="true"
          />
          <template #subTitle2>
            <v-slider
                v-model="columns"
                :max="5"
                :min="1"
                :step="1"
                hide-details
                density="compact"
                color="primary"
            />
          </template>
        </app-setting>
        <v-divider/>
        <app-setting
            :r-cols="3"
            :title="$t('print.page_settings.num_rows')"
        >
          <v-text-field
              type="number"
              v-model.number="rows"
              :hide-details="true"
              density="compact"
              variant="solo-filled"
              color="primary"
              :disabled="true"
          />
          <template #subTitle2>
            <v-slider
                v-model="rows"
                :max="15"
                :min="1"
                :step="1"
                :hide-details="true"
                density="compact"
                color="primary"
            />
          </template>
        </app-setting>
        <v-divider/>
        <margin-setting margin="left"/>
        <margin-setting margin="top"/>
        <margin-setting margin="right"/>
        <margin-setting margin="bottom"/>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<style scoped lang="scss">

</style>