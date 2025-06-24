<script setup lang="ts">
import {ItemSummarySchema} from "@/api/types/items.ts";

const {t} = useI18n();

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
  <v-row
      dense
      justify="center"
      class="mt-4 pb-16"
  >
    <v-col
        class="d-flex justify-center"
    >
      <v-sheet
          v-if="items.length > 0"
          color="transparent"
          class="text-center pa-4"
      >
        <v-icon
            icon="mdi-check-circle-outline"
            color="success"
            size="x-large"
            class="mb-2"
        ></v-icon>
        <p class="text-h6">You're all caught up!</p>
        <p class="text-medium-emphasis">All items have been displayed.</p>
      </v-sheet>
    </v-col>
  </v-row>

</template>

<style scoped lang="scss">

</style>