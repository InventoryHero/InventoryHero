<script setup lang="ts">
import {ItemReadSchema} from "@/api/types/items.ts";
import {RoomResponseSchema} from "@/api/types/storage.ts";

const {t} = useI18n()
const {storage} = useAxios()
const router = useRouter()
const {openModal} = useGlobalModal()

const room = defineModel<RoomResponseSchema>({
  required: true
})

const roomDeleteConfirmationVisible = ref<boolean>(false)

const deleteRoom = async (confirmed: boolean) => {
  if(!confirmed){
    roomDeleteConfirmationVisible.value = true
    return
  }

  const {success, error} = await storage.deleteStorage(room.value.id)
  if(!success){
    // TODO
    return
  }
  roomDeleteConfirmationVisible.value = false
  router.push("/storage/rooms")


}
const editRoom = () => {
  openModal("editRoomModal", {
    room: room.value,
    'onUpdate:room': (newValue: RoomResponseSchema) => room.value = newValue,
  })
}

</script>

<template>
  <confirm-room-delete-modal
    v-model="roomDeleteConfirmationVisible"
    @delete="deleteRoom(true)"
    :name="room.name"
  />
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
          @click="deleteRoom(false)"
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