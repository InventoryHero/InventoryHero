<script setup lang="ts">
import ItemList from '@/components/storage/rooms/ItemList.vue'
import BoxesList from '@/components/storage/rooms/BoxesList.vue'
import RoomContentHeader from '@/components/storage/rooms/RoomContentHeader.vue'
import { RoomResponseSchema } from '@/api/types/storage.ts'

definePage({
  props: true,
  meta: {
    requiresAuth: true,
    requiresHousehold: true,
    title: 'titles.rooms',
    showFab: true,
    layout: 'default'
  }
})

type Tab = {
  icon: string
  value: string
  component: any
}

const { storage: storageEndpoint } = useAxios()
const { t } = useI18n()
const router = useRouter()

const { id } = defineProps<{
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
  const { success, data, error } = await storageEndpoint.getStorageDetail(id)
  if (!success) {
    await router.push('/storage/rooms')
    return
  }
  room.value = data! as RoomResponseSchema
  loading.value = false
}

onBeforeMount(() => {
  loadRoomDetail()
})
</script>

<template>
  <v-skeleton-loader
    v-if="loading || !room"
    type="heading, subtitle, paragraph, actions, divider, actions, divider, list-item@4"
  />

  <template v-else>
    <room-content-header v-model="room" />

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
      <template v-slot:tab="{ item }">
        <v-tab
          :prepend-icon="item.icon"
          :text="t(`rooms.room.tabs.${item.value}`)"
          :value="item.value"
          class="text-none"
        />
      </template>
      <template v-slot:item="{ item }">
        <v-tabs-window-item
          :value="item.value"
          class="mt-2"
        >
          <component
            :is="item.component"
            :id="id"
          />
        </v-tabs-window-item>
      </template>
    </v-tabs>
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
