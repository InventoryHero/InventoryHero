<script setup lang="ts">
import {RoomResponseSchema} from "@/api/types/storage.ts";
import ItemList from "@/components/storage/rooms/ItemList.vue";

type Tab = {
  icon: string,
  value: string,
  component: any
}

const {storage: storageEndpoint} = useAxios()
const {t} = useI18n()
const route = useRoute()

const needle = ref<string|undefined>();
const rooms = ref<Array<RoomResponseSchema>>([])
const loading = ref<boolean>(false)


const filteredRooms = computed(() => {
  if(!needle.value){
    return rooms.value
  }
  return rooms.value.filter(room => room.name.toLowerCase().includes(needle.value!.toLowerCase()))
})


onBeforeMount(() => {


  storageEndpoint.getAllStorage("room").then(({success, data, error}) => {
    if(!success){
      //TODO
    }
    rooms.value = (data ?? []) as RoomResponseSchema[]
  })
})
</script>

<template>
  <search-card
      v-model="needle"
  />

  <v-row dense v-if="!loading" class="pb-16">
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
</template>

<style scoped lang="scss">

</style>