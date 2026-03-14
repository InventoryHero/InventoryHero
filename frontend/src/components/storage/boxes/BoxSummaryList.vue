<script setup lang="ts">

import {BoxResponseSchema} from "@/api/types/storage.ts";

const {t} = useI18n()
const boxes = defineModel<Array<BoxResponseSchema>>({
  required: true
})

const {
  numBoxes = 0
} = defineProps<{
  numBoxes?: number
}>()

const endReachedContent = computed(() => {
  if(boxes.value.length > 0){
    return {
      title: t('boxes.all_displayed')
    }
  }
  if(numBoxes == 0){
    return {
      title: t('boxes.no_boxes'),
      icon: "mdi-alert-circle-outline",
      color: "warning"
    }
  }
  return {
    title: t('boxes.filtered_all'),
    icon: "mdi-magnify-close",
    color: "info"
  }
})

</script>

<template>
  <v-row
      dense
  >
    <v-col

        v-for="box in boxes"
        cols="12"
        sm="6"
        md="6"
        lg="4"
        xl="3"
    >
      <box-summary-card
          :box="box"
      />
    </v-col>
  </v-row>
  <v-row dense justify="center" class="pb-16">
    <v-col
        class="d-flex justify-center"
    >
      <all-displayed
        v-bind="endReachedContent"
      />
    </v-col>
  </v-row>

</template>

<style scoped lang="scss">

</style>