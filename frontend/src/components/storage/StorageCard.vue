<script setup lang="ts">
import {computed} from 'vue'
import {ApiStorage, StorageTypes} from "@/types/api.ts";
import {useI18n} from "vue-i18n";

const {t: $t, d: $d} = useI18n()


defineOptions({
  inheritAttrs: false
})


const {storage=undefined, type=StorageTypes.Box} = defineProps<{
  storage?: ApiStorage,
  type?: StorageTypes
}>()

const name = computed(() => {
  return storage?.name
})
const creationDate = computed(() => {
  let date: string|number = storage?.creationDate ?? ''
  if(date === "")
    date = -1
  return $d(new Date(date))
})

const productAmount = computed(() => {
  return storage?.productAmount
})
const boxAmount = computed(() => {
  return storage?.boxAmount
})

const localizationBase = computed(() => {
  if(type === StorageTypes.Box){
    return "boxes.box"
  }
  if(type === StorageTypes.Location){
    return "locations.location"
  }
  return ""
})
</script>

<template>
  <v-hover
    v-slot="{ isHovering, props }"
  >
    <v-card
        :elevation="0"
        :class="{
          'hovering': isHovering
        }"
        v-bind="$attrs"
    >
      <v-card-title
        class="title"
      >
        {{ name }}
      </v-card-title>
      <v-card-subtitle
          class="mb-1"
      >
        <v-row
            :no-gutters="true"
            justify="center"
        >
          <v-col
              cols="6"
          >
            {{ $t(`${localizationBase}.created`) }}
          </v-col>
          <v-col
              cols="6"
              class="d-flex justify-end"
          >
            {{ creationDate }}
          </v-col>
        </v-row>
        <v-row

            :no-gutters="true"
            justify="center"
        >
          <v-col
              cols="6"
          >
            {{ $t(`${localizationBase}.product_amount`) }}
          </v-col>
          <v-col
              cols="6"
              class="d-flex justify-end"
          >
            {{ productAmount }}
          </v-col>
        </v-row>
        <v-row
            v-if="type === StorageTypes.Location"
            :no-gutters="true"
            justify="center"
        >
          <v-col
              cols="6"
          >
            {{ $t('locations.location.boxes_amount') }}
          </v-col>
          <v-col
              cols="6"
              class="d-flex justify-end"
          >
            {{ boxAmount }}
          </v-col>
        </v-row>
      </v-card-subtitle>
    </v-card>
    <slot name="divider" >
      <v-divider
          color="primary"
          class="border-opacity-75"
      />
    </slot>

  </v-hover>
</template>

<style scoped lang="scss">
  .title {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
  }

  .hovering{
    background-color: rgba(var(--v-theme-primary), 0.15);
  }
</style>