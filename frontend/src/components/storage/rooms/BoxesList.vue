<script setup lang="ts">
import ItemSummaryList from "@/components/items/ItemSummaryList.vue";
import {ItemSummarySchema} from "@/api/types/items.ts";
import {BoxResponseSchema} from "@/api/types/storage.ts";

const {storage: storageEndpoint} = useAxios()
const {t} = useI18n()
const route = useRoute()

const {
  id
} = defineProps<{
  id: string
}>()

const boxes = ref<Array<BoxResponseSchema>>([])

onBeforeMount(() => {
  storageEndpoint.getStorageBoxes(id).then(({success, data, error}) => {
    if(!success){
      //TODO
    }
    boxes.value = data ?? []
  })
})
</script>

<template>
  <box-summary-list
    v-model="boxes"
  />
</template>

<style scoped lang="scss">

</style>