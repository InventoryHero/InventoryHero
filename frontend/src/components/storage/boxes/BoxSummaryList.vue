<script setup lang="ts">

import {BoxResponseSchema} from "@/api/types/storage.ts";

const boxes = defineModel<Array<BoxResponseSchema>>({
  required: true
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
      all items have been displayed
    </v-col>
  </v-row>

</template>

<style scoped lang="scss">

</style>