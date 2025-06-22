<script setup lang="ts">

import {BoxResponseSchema, StorageType} from "@/api/types/storage.ts";
import BoxSummaryCard from "@/components/storage/boxes/BoxSummaryCard.vue";

const {storage: storageEndpoint} = useAxios()
const {t} = useI18n()
const route = useRoute()

const needle = ref<string|undefined>();
const boxes = ref<Array<BoxResponseSchema>>([])
const loading = ref<boolean>(false)



const filteredBoxes = computed(() => {
  if(!needle.value){
    return boxes.value
  }
  return boxes.value.filter(box => box.name.toLowerCase().includes(needle.value!.toLowerCase()))
})


onBeforeMount(() => {

  storageEndpoint.getAllStorage("box").then(({success, data, error}) => {
    if(!success){
      //TODO
    }
    boxes.value = (data ?? []) as Array<BoxResponseSchema>
  })
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