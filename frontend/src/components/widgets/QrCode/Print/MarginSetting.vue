<script setup lang="ts">

import {usePrintSettings} from "@/store";

const printSettingStore = usePrintSettings()

const margins = computed(() => printSettingStore.margins)

function setMargin(value: number){
  printSettingStore.setMargin(margin, value)
}


const {margin} = defineProps<{
  margin: 'left'|'right'|'top'|'bottom'
}>()

</script>

<template>

  <app-setting
      :r-cols="3"
      :title="$t(`print.page_settings.margin_${margin}`)"
  >
    <v-text-field
        type="number"
        v-model.number="margins[margin]"
        :hide-details="true"
        density="compact"
        variant="solo-filled"
        color="primary"
        :disabled="true"
    />
    <template #subTitle2>
      <v-slider
          v-model="margins[margin]"
          @update:model-value="setMargin"
          :max="30"
          :min="0"
          :step="1"
          :hide-details="true"
          density="compact"
          color="primary"
      />
    </template>
  </app-setting>
  <v-divider/>
</template>

<style scoped lang="scss">

</style>