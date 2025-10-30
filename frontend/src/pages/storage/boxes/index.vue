<script setup lang="ts">
import { BoxResponseSchema, StorageType } from '@/api/types/storage.ts'
import boxAddedEventBus from '@/services/boxAddedEventBus.ts'
import useContentRefreshStore from '@/stores/useContentRefreshStore'

const { storage: storageEndpoint } = useAxios()
const { t } = useI18n()
const route = useRoute()
const contentRefreshStore = useContentRefreshStore()

const needle = ref<string | undefined>()
const boxes = ref<Array<BoxResponseSchema>>([])
const loading = ref<boolean>(false)

const filteredBoxes = computed(() => {
  if (!needle.value) {
    return boxes.value
  }
  return boxes.value.filter((box) =>
    box.name.toLowerCase().includes(needle.value!.toLowerCase())
  )
})

const loadBoxes = async () => {
  loading.value = true
  const { success, data } = await storageEndpoint.getAllStorage('box')
  if (!success) {
    boxes.value = []
    loading.value = false
    return
  }
  boxes.value = (data ?? []) as Array<BoxResponseSchema>
  loading.value = false
}

const clickOnBanner = () => {
  loadBoxes().then(() => {})
}

boxAddedEventBus.on(() => {
  contentRefreshStore.showBanner({
    title: t('boxes.content_changed_title'),
    subtitle: t('boxes.content_changed_subtitle'),
    callback: clickOnBanner
  })
})

onBeforeMount(() => {
  loadBoxes()
})
</script>

<template>
  <search-card v-model="needle" />

  <box-summary-list
    v-if="!loading"
    v-model="filteredBoxes"
    :num-boxes="boxes.length"
  />
  <v-skeleton-loader
    v-else
    :loading="loading"
    type="list-item-avatar-three-line@4"
  />
</template>

<style scoped lang="scss"></style>

<route>
{
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": true,
    "title": 'titles.boxes',
    "showFab": true
  }
}
</route>
