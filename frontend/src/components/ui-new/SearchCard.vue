<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";

const {textFieldStyling} = useAppStyling()

const needle = defineModel<string|undefined>({
  required: true
});
</script>

<template>
  <v-card
      v-bind="$attrs"
  >
    <v-container class="pa-3" fluid>
      <v-row dense>
        <v-col>
          <v-text-field
              v-bind="textFieldStyling"
              label="Search..."
              v-model="needle"
              density="compact"
          />
        </v-col>
      </v-row>
      <slot />
    </v-container>
  </v-card>
  <v-divider class="mt-2 mb-2" :thickness="2" />
</template>

<style scoped lang="scss">

</style>