<script setup lang="ts">

import {RoomResponseSchema, BoxResponseSchema} from "@/api/types/storage.ts";

const {t} = useI18n();
const {mdAndUp, xs, sm, md} = useDisplay()

const selectedItems = defineModel<{
  [key: string]: boolean
}>({
  required: true
})

const {
  objects,
  numSelectedObjects,
  type
} = defineProps<{
  objects: Array<RoomResponseSchema|BoxResponseSchema>,
  numSelectedObjects: number,
  type: 'room'|'box'
}>()

const selectAllTitle = computed(() => {
  if(numSelectedObjects === objects.length) {
    return t('qr.label.deselect_all')
  }
  return t('qr.label.select_all')
})

const selectAll = () => {
  const selectOrDeselectAll = objects.length === numSelectedObjects
  objects.forEach((_, index) => {
    selectedItems.value[`${type}-${index}`] = !(selectOrDeselectAll)
  })
}

</script>

<template>
  <v-list
      :height="mdAndUp ? '55vh' : '35vh'"
  >
    <v-list-item
        v-for="(box, index) in objects"
        :key="box.id"
        class="mb-2"
        rounded="lg"
        :title="box.name"
    >
      <template v-slot:prepend>
        <v-checkbox-btn
            v-model="selectedItems[`${type}-` + index]"
        />
      </template>

    </v-list-item>

  </v-list>
  <v-list-item
      :title="selectAllTitle"

  >
    <template v-slot:prepend>
      <v-checkbox-btn
          :model-value="numSelectedObjects === objects.length"
          :indeterminate="numSelectedObjects > 0 && numSelectedObjects !== objects.length"
          @click="selectAll"
      />
    </template>
  </v-list-item>
</template>

<style scoped lang="scss">

</style>