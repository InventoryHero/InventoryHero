<script setup lang="ts">

import {templateRef} from "@vueuse/core";
import {RoomResponseSchema, BoxResponseSchema} from "@/api/types/storage.ts";

const selectedObjects = defineModel<{
  [key: string]: boolean
}>()
const {
  rooms,
  boxes
} = defineProps<{
  rooms: Array<RoomResponseSchema>,
  boxes: Array<BoxResponseSchema>
}>()

const objects = computed(() => {
  if(!selectedObjects.value)
    return []
  return Object.keys(selectedObjects.value).reduce((accumulator, key) => {
    if (!(selectedObjects.value![key] ?? false)) {
      return accumulator
    }


    const parts = key.split('-');
    switch(parts[0]){
      case 'room':
        accumulator.push(rooms[parseInt(parts[1], 10)])
        break
      case 'box':
        accumulator.push(boxes[parseInt(parts[1], 10)])
        break
    }
    return accumulator
  }, [] as (RoomResponseSchema|BoxResponseSchema)[])
})

const zoomLevel = ref(3)

const zoomIn = () => {
  zoomLevel.value = Math.min(3, zoomLevel.value + 0.1);
};
const zoomOut = () => {
  zoomLevel.value = Math.max(0.1, zoomLevel.value - 0.1);
};

const scrollContainer = templateRef("scrollContainer");
const isDragging = ref(false);
const lastPos = reactive({ x: 0, y: 0 });
const onMouseDown = (event: MouseEvent) => {
  if (!scrollContainer.value) return;
  isDragging.value = true;
  scrollContainer.value.style.cursor = 'grabbing';
  lastPos.x = event.clientX;
  lastPos.y = event.clientY;
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', onMouseUp);
};

const onMouseMove = (event: MouseEvent) => {
  if (!isDragging.value || !scrollContainer.value) return;
  const dx = event.clientX - lastPos.x;
  const dy = event.clientY - lastPos.y;
  scrollContainer.value.scrollLeft -= dx;
  scrollContainer.value.scrollTop -= dy;
  lastPos.x = event.clientX;
  lastPos.y = event.clientY;
};

const onMouseUp = () => {
  if (!scrollContainer.value) return;
  isDragging.value = false;
  scrollContainer.value.style.cursor = 'grab';
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', onMouseUp);
};

</script>

<template>
  <v-card class="pa-2 sticky-preview " elevation="4">
    <v-card-text class="text-center">
      <h2 class="text-h6 font-weight-semibold mb-4">Page Preview</h2>
      <div class="preview-wrapper">
        <div
            class="scroll-container"
            ref="scrollContainer"
            @mousedown="onMouseDown"
        >
          <v-sheet
              color="white"
              width="210"
              height="297"
              class="d-flex flex-wrap pa-2 ga-1 align-content-start"
              :style="{
                transform:  `scale(${zoomLevel})`,
                'transform-origin': 'top leftq',
                border: '2px solid rgb(var(--v-theme-outline))',
              }"
          >
            <template v-for="(item) in objects" :key="item.id">
              <v-sheet color="grey-lighten-3" class="d-flex align-center justify-center">
                <v-icon size="x-small">mdi-qrcode</v-icon>
                <p>{{item.name}}</p>
              </v-sheet>
            </template>
          </v-sheet>
        </div>
      </div>

    </v-card-text>
    <v-card-actions>
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
</template>

<style scoped lang="scss">
.scroll-container {
  flex-grow: 1;
  overflow: auto;
  padding: 16px;
}

.preview-wrapper {
  display: flex;
  flex-direction: column;
  height: 70vh;
  width: 100%;
}
</style>