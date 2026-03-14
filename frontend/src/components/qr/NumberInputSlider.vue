<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";

const {numberInputStyling} = useAppStyling()
const {t} = useI18n()
const model = defineModel<number>({
  required: true,
})

const {
  title,
  min=0,
  max=30,
  step=0.1,
  unit,
  disabled=false
} = defineProps<{
  title: string,
  min?: number,
  max?: number,
  step?: number,
  unit?: string,
  disabled?: boolean
}>()

</script>

<template>
  <v-col
      :cols=" unit !== undefined ? 6 : 7"
  >
    <span class="text-subtitle-2 text-medium-emphasis">{{title}}</span>
    <v-slider
        :disabled="disabled"
        v-model="model"
        :min="min"
        :max="max"
        :step="step"
        color="primary"
        hide-details
    >
    </v-slider>
  </v-col>
  <v-col
      :cols=" unit !== undefined ? 6 : 5"
  >
    <v-number-input
        v-model="model"
        v-bind="numberInputStyling"
        control-variant="stacked"
        :precision="1"
        :disabled="disabled"
        :step="step"
        :min="min"
        :max="max"
    >
      <template v-if="unit !== undefined" v-slot:append-inner>
        <span class="me-1">{{unit}}</span>
      </template>
    </v-number-input>
  </v-col>
</template>

<style scoped lang="scss">

</style>