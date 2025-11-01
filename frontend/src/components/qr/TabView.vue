<script setup lang="ts">
import {
  RoomResponseSchema,
  BoxResponseSchema,
  StorageType
} from '@/api/types/storage.ts'
import useAppStyling from '@/composables/useAppStyling.ts'
import { ref } from 'vue'

const { t } = useI18n()
const { mdAndUp, xs, sm, md } = useDisplay()
const { textFieldStyling } = useAppStyling()

const selectedItems = defineModel<{ [key in StorageType]: Array<string> }>({
  required: true
})

const { objects, numSelectedObjects, type } = defineProps<{
  objects: Array<RoomResponseSchema | BoxResponseSchema>
  numSelectedObjects: number
  type: StorageType
}>()

const search = ref<string | null | undefined>('')
const filteredObjects = computed(() => {
  if (!search.value || search.value === '') {
    return objects
  }
  return objects.filter((x) => x.name.includes(search.value!))
})

const selectAllTitle = computed(() => {
  if (numSelectedObjects === objects.length) {
    return t('qr.label.deselect_all')
  }
  return t('qr.label.select_all')
})

const selectAll = () => {
  if (objects.length === numSelectedObjects) {
    selectedItems.value[type] = []
    return
  }

  objects.forEach((obj) => {
    if (!selectedItems.value[type].includes(obj.id)) {
      selectedItems.value[type].push(obj.id)
    }
  })
}
</script>

<template>
  <v-card class="d-flex flex-column fill-height">
    <v-card-text class="flex-grow-1 overflow-auto pt-0 mt-0">
      <v-sheet
        class="position-sticky pt-4"
        style="top: 0; z-index: 2"
      >
        <v-text-field
          v-bind="textFieldStyling"
          v-model="search"
          :label="t(`qr.label.search_${type}`)"
          prepend-inner-icon="mdi-magnify"
        />
      </v-sheet>
      <v-list
        v-model:selected="selectedItems[type]"
        select-strategy="leaf"
      >
        <v-list-item
          v-for="object in filteredObjects"
          :key="object.id"
          :title="object.name"
          :value="object.id"
        >
          <template v-slot:prepend="{ isSelected, select }">
            <v-list-item-action start>
              <v-checkbox-btn
                :model-value="isSelected"
                @update:model-value="select"
              ></v-checkbox-btn>
            </v-list-item-action>
          </template>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions class="flex-0-0">
      <v-list-item
        :title="selectAllTitle"
        class="position-sticky"
        style="z-index: 2"
      >
        <template v-slot:prepend>
          <v-checkbox-btn
            :model-value="numSelectedObjects === objects.length"
            :indeterminate="
              numSelectedObjects > 0 && numSelectedObjects !== objects.length
            "
            @click="selectAll"
          />
        </template>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss"></style>
