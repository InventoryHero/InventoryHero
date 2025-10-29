<script setup lang="ts">
import { templateRef } from '@vueuse/core'
import {
  RoomResponseSchema,
  BoxResponseSchema,
  StorageType
} from '@/api/types/storage.ts'
import usePrintSettingsStore, {
  paperSizes
} from '@/stores/usePrintSettingsStore'
import { storeToRefs } from 'pinia'
import { useVueToPrint } from 'vue-to-print'

const printSettings = usePrintSettingsStore()
const { handlePrint } = useVueToPrint({
  content: () => page.value,
  onAfterPrint: () => {
    //loadingPrint.value = false
  },
  removeAfterPrint: true
})

const selectedObjects = defineModel<{
  [key in StorageType]: Array<string>
}>({
  required: true
})
const { rooms, boxes } = defineProps<{
  rooms: Array<RoomResponseSchema>
  boxes: Array<BoxResponseSchema>
}>()
const page = templateRef('page')
const zoomLevel = ref(0.8)
const { columns, rows, margins, paper, borderThickness } =
  storeToRefs(printSettings)
const scrollContainer = templateRef('scrollContainer')
const isDragging = ref(false)
const lastPos = reactive({ x: 0, y: 0 })

const objects = computed<(RoomResponseSchema | BoxResponseSchema)[]>(() => {
  if (!selectedObjects.value) {
    return []
  }
  const selectedRooms = rooms.filter((room) =>
    selectedObjects.value.room.includes(room.id)
  )
  const selectedBoxes = boxes.filter((box) =>
    selectedObjects.value.box.includes(box.id)
  )

  console.log(selectedRooms.length, selectedBoxes.length)
  return [...selectedRooms, ...selectedBoxes]
})

const labelsPerPage = computed(() => {
  return rows.value * columns.value
})

const totalPages = computed(() => {
  const totalLabels = objects.value.length
  console.log(labelsPerPage.value)
  console.log(totalLabels)
  console.log(Math.ceil(totalLabels / labelsPerPage.value))
  return Math.ceil(totalLabels / labelsPerPage.value)
})

const colSize = computed(() => Math.floor(12 / columns.value))

const border = computed(() => {
  if (borderThickness.value === 0) {
    return ''
  }
  return `rgb(var(--v-theme-primary)) ${borderThickness.value}px solid`
})

const labelHeightInMm = computed(() => {
  const height =
    (paperSizes[paper.value].height -
      margins.value.top -
      margins.value.bottom) /
    rows.value
  console.log(height)

  return `${Math.floor(height)}mm`
})

const getStorageIndex = (page: number, row: number, col: number) => {
  return (
    (page - 1) * labelsPerPage.value + (row - 1) * columns.value + (col - 1)
  )
}

const zoomIn = () => {
  zoomLevel.value = Math.min(3, zoomLevel.value + 0.1)
}
const zoomOut = () => {
  zoomLevel.value = Math.max(0.1, zoomLevel.value - 0.1)
}

const onMouseDown = (event: MouseEvent) => {
  if (!scrollContainer.value) return
  isDragging.value = true
  scrollContainer.value.style.cursor = 'grabbing'
  lastPos.x = event.clientX
  lastPos.y = event.clientY
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

const onMouseMove = (event: MouseEvent) => {
  if (!isDragging.value || !scrollContainer.value) return
  const dx = event.clientX - lastPos.x
  const dy = event.clientY - lastPos.y
  scrollContainer.value.scrollLeft -= dx
  scrollContainer.value.scrollTop -= dy
  lastPos.x = event.clientX
  lastPos.y = event.clientY
}

const onMouseUp = () => {
  if (!scrollContainer.value) return
  isDragging.value = false
  scrollContainer.value.style.cursor = 'grab'
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
}
</script>

<template>
  <v-card
    class="d-flex flex-column fill-height"
    elevation="0"
  >
    <v-card-text class="text-center flex-1-1 overflow-hidden">
      <div class="preview-wrapper">
        <div
          class="scroll-container"
          ref="scrollContainer"
          @mousedown="onMouseDown"
        >
          <div
            :style="{
              transform: `scale(${zoomLevel})`,
              'transform-origin': 'top left'
            }"
          >
            <div ref="page">
              <v-sheet
                v-for="page in totalPages"
                color="white"
                :width="`${paperSizes[paper].width}mm`"
                :height="`${paperSizes[paper].height}mm`"
                :style="{
                  border: '2px solid rgb(var(--v-theme-outline))',
                  padding: `${margins.top}mm ${margins.right}mm ${margins.bottom}mm ${margins.left}mm`
                }"
              >
                <v-row
                  v-for="row in rows"
                  justify="space-between"
                  :style="{
                    height: labelHeightInMm
                  }"
                  dense
                >
                  <v-col
                    v-for="col in columns"
                    :cols="colSize"
                    :key="col"
                    class="fill-height"
                    :style="{
                      border:
                        getStorageIndex(page, row, col) < objects.length
                          ? border
                          : undefined
                    }"
                  >
                    <!-- todo get correct storage with row col offset-->
                    <inventory-hero-label
                      v-if="getStorageIndex(page, row, col) < objects.length"
                      :object="objects[getStorageIndex(page, row, col)]"
                    />
                  </v-col>
                </v-row>
              </v-sheet>
            </div>
          </div>
        </div>
      </div>
    </v-card-text>
    <v-card-actions class="flex-0-0">
      <v-slider
        v-model="zoomLevel"
        color="primary"
        min="0.1"
        max="3"
        step="0.1"
        append-icon="mdi-magnify-plus-outline"
        prepend-icon="mdi-magnify-minus-outline"
        @click:append="zoomIn"
        @click:prepend="zoomOut"
      />
    </v-card-actions>
  </v-card>
  <slot :print="handlePrint" />
</template>

<style scoped lang="scss">
.scroll-container {
  overflow: auto;
}
.preview-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}
</style>
