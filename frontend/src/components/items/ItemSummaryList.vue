<script setup lang="ts">

import {ItemSummarySchema} from "@/api/types/items.ts";

const items = defineModel<Array<ItemSummarySchema>>({
  required: true
})

const {
  from = undefined
} = defineProps<{
  from?: string
}>()




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
  <v-row dense justify="center" class="pb-16">
    <v-col
        class="d-flex justify-center"
    >
      all items have been displayed
    </v-col>
  </v-row>

</template>

<style scoped lang="scss">

</style>