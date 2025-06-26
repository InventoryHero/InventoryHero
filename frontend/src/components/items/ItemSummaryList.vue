<script setup lang="ts">
import {ItemSummarySchema} from "@/api/types/items.ts";

const {t} = useI18n();

const items = defineModel<Array<ItemSummarySchema>>({
  required: true
})

const {
  from = undefined,
  numItems = 0
} = defineProps<{
  from?: string,
  numItems?: number
}>()

const endReachedContent = computed(() => {
  if(items.value.length > 0){
    return {
      title: t('items.all_displayed')
    }
  }
  if(numItems == 0){
    return {
      title: t('items.no_items'),
      icon: "mdi-alert-circle-outline",
      color: "warning"
    }
  }
  return {
    title: t('items.filtered_all'),
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

        v-for="item in items"
        cols="12"
        sm="6"
        md="6"
        lg="4"
        xl="3"
    >
      <item-summary-card
          :item="item"
          :from="from"
      />
    </v-col>
  </v-row>
  <v-row
      dense
      justify="center"
      class="mt-4 pb-16"
  >
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