<script setup lang="ts">

import {BoxResponseSchema, StorageType} from "@/api/types/storage.ts";
import boxAddedEventBus from "@/services/boxAddedEventBus.ts";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";

const {storage: storageEndpoint} = useAxios()
const {t} = useI18n()
const route = useRoute()
const contentRefreshStore = useContentRefreshStore()

const needle = ref<string|undefined>();
const boxes = ref<Array<BoxResponseSchema>>([])
const loading = ref<boolean>(false)



const filteredBoxes = computed(() => {
  if(!needle.value){
    return boxes.value
  }
  return boxes.value.filter(box => box.name.toLowerCase().includes(needle.value!.toLowerCase()))
})

const loadBoxes = async () => {
  storageEndpoint.getAllStorage("box").then(({success, data, error}) => {
    if(!success){
      //TODO
    }
    boxes.value = (data ?? []) as Array<BoxResponseSchema>
  })
}

const clickOnBanner = () => {
  loadBoxes().then(() => {
  })
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
  <search-card
    v-model="needle"
  />

  <box-summary-list v-model="filteredBoxes" />
</template>

<style scoped lang="scss">

</style>