<script setup lang="ts">
import {ItemReadSchema} from "@/api/types/items.ts";
import {RoomResponseSchema} from "@/api/types/storage.ts";

const {t} = useI18n()

const room = defineModel<RoomResponseSchema>({
  required: true
})

const deleteRoom = () => {
  // TODO
}
const editRoom = () => {
  // TODO
}

</script>

<template>
  <v-card>
    <template v-slot:prepend>
      <v-icon
          icon="mdi-package-variant"
      />
    </template>
    <template v-slot:title>
      {{ room.name }}
    </template>
    <v-card-actions>
      <v-spacer/>
      <v-btn
          prepend-icon="mdi-trash-can"
          @click="deleteRoom"
          :text="t('rooms.room.delete')"
          density="comfortable"
          color="error"
          varaint="tonal"
          class="text-none"
      />
      <v-btn
          prepend-icon="mdi-pencil"
          @click="editRoom"
          :text="t('rooms.room.edit')"
          density="comfortable"
          color="primary"
          class="text-none"
      />
    </v-card-actions>
  </v-card>

  <v-divider class="mt-2 mb-2" :thickness="2" />
</template>

<style scoped lang="scss">

</style>