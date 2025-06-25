<script setup lang="ts">
import {RoomResponseSchema} from "@/api/types/storage.ts";
import {storeToRefs} from "pinia";
import roomAddedEventBus from "@/services/roomAddedEventBus.ts";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";

type Tab = {
  icon: string,
  value: string,
  component: any
}

const {t} = useI18n()
const route = useRoute()
const {storage: storageEndpoint} = useAxios()
const contentRefreshStore = useContentRefreshStore()

const needle = ref<string|undefined>();
const rooms = ref<RoomResponseSchema[]>([])
const isLoading = ref(false)
const filteredRooms = computed(() => {
  if(!needle.value){
    return rooms.value
  }
  return rooms.value.filter(room => room.name.toLowerCase().includes(needle.value!.toLowerCase()))
})

const loadRooms = async () => {
  isLoading.value = true;
  const {success, data, error} = await storageEndpoint.getAllStorage("room")
  if(!success){
    //TODO
  }
  rooms.value = (data ?? []) as RoomResponseSchema[]
  isLoading.value = false
}

const clickOnBanner = () => {
  loadRooms().then(() => {
  })
}

roomAddedEventBus.on(() => {
  contentRefreshStore.showBanner({
    title: t('rooms.content_changed_title'),
    subtitle: t('rooms.content_changed_subtitle'),
    callback: clickOnBanner
  })
})

onBeforeMount(() => {
  loadRooms()
})
</script>

<template>
  <search-card
      v-model="needle"
  />

  <template v-if="!isLoading">
    <v-row dense>
      <v-col
          v-for="room in filteredRooms"
          cols="12"
          sm="6"
          md="6"
          lg="4"
          xl="3"
      >
        <room-summary-card
            :room="room"
        />
      </v-col>
    </v-row>
    <v-row
        dense
        justify="center"
        class="mt-4 pb-16"
    >
      <v-col
          class="d-flex justify-center"
      >
        <v-sheet
            v-if="rooms.length > 0"
            color="transparent"
            class="text-center pa-4"
        >
          <v-icon
              icon="mdi-check-circle-outline"
              color="success"
              size="x-large"
              class="mb-2"
          ></v-icon>
          <p class="text-medium-emphasis">{{t('rooms.all_displayed')}}</p>
        </v-sheet>
      </v-col>
    </v-row>
  </template>
  <v-skeleton-loader
    v-else
    :loading="isLoading"
    type="list-item-avatar-three-line@4"
  />
</template>

<style scoped lang="scss">

</style>