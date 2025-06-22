<script setup lang="ts">
import ItemList from "@/components/storage/rooms/ItemList.vue";
import {ItemSummarySchema} from "@/api/types/items.ts";
import BoxesList from "@/components/storage/rooms/BoxesList.vue";
import RoomContentHeader from "@/components/storage/rooms/RoomContentHeader.vue";
import {RoomResponseSchema} from "@/api/types/storage.ts";

type Tab = {
  icon: string,
  value: string,
  component: any
}

const {storage: storageEndpoint} = useAxios()
const {t} = useI18n()
const route = useRoute()

const {
  id
} = defineProps<{
  id: string
}>()

const room = ref<RoomResponseSchema>()
const loading = ref<boolean>(false)

const tab = ref<string>('items')
const tabs = shallowRef<Array<Tab>>([
  {
    icon: 'mdi-invoice-list',
    value: 'items',
    component: ItemList
  },
  {
    icon: 'mdi-package-variant',
    value: 'boxes',
    component: BoxesList
  }
])

const loadRoomDetail = async () => {
  loading.value = true
  const {success, data, error} = await storageEndpoint.getStorageDetail(id)
  if(!success) {
    // TODO
  }
  console.log(room)
  room.value = data! as RoomResponseSchema
  loading.value = false
}

onBeforeMount(() => {
  loadRoomDetail()
})
</script>

<template>

  <template v-if="!loading">
    <room-content-header
      v-model="room!"
    />

    <v-tabs
        align-tabs="end"
        show-arrows
        v-model="tab"
        :items="tabs"
        color="white"
        slider-color="primary"
        density="comfortable"
        center-active
        class="sticky-tabs"

    >
      <template v-slot:tab="{item}">
        <v-tab
            :prepend-icon="item.icon"
            :text="t(`rooms.room.tabs.${item.value}`)"
            :value="item.value"
            class="text-none"

        />
      </template>
      <template v-slot:item="{item}">
        <v-tabs-window-item
            :value="item.value"
            class="mt-1"
        >
          <component
              :is="item.component"
              :id="id"
          />
        </v-tabs-window-item>
      </template>

    </v-tabs>
  </template>
  <template v-else>
    <!-- TODO v-skeleton-loader -->
  </template>

</template>

<style scoped lang="scss">
.sticky-tabs {
  /* This is the magic that makes the tabs stick */
  position: sticky;
  top: var(--v-layout-top);
  z-index: 2;
  background-color: rgb(var(--v-theme-surface));
}
</style>