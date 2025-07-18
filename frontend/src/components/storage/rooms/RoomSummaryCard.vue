<script setup lang="ts">
import {RoomResponseSchema} from "@/api/types/storage.ts";

const router = useRouter()
const {t} = useI18n()

const {
  room
} = defineProps<{
  room: RoomResponseSchema
}>()

const to = computed(() => {
  return router.resolve({
    name: "/storage/rooms/room.[id]",
    params: {
      id: room.id
    }
  } )
})



</script>

<template>
  <v-card
      max-height="140px"
      class="pl-0"
      elevation="0"
      density="compact"
      :to="to"
  >
    <template v-slot:prepend>
      <v-icon icon="mdi-package-variant" />
    </template>
    <template v-slot:title>
            <span
                class="text-truncate"
            >
              {{ room.name }}
            </span>
    </template>
    <template v-slot:subtitle>
      <span
          class="text-medium-emphasis text-overline text-center"
      >
        <v-icon
            icon="mdi-invoice-list"
            class="me-1"
        />
        {{t('rooms.room.items_quantity', room.num_items ?? 0)}}
      </span> <br/>
      <span
          class="text-medium-emphasis text-overline text-center"
      >
        <v-icon
            icon="mdi-package-variant"
            class="me-1"
        />
        {{t('rooms.room.boxes_quantity', room.num_boxes ?? 0)}}
      </span>
    </template>
  </v-card>
</template>

<style scoped lang="scss">

</style>