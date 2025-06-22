<script setup lang="ts">
import ItemSummaryList from "@/components/items/ItemSummaryList.vue";
import {ItemSummarySchema} from "@/api/types/items.ts";

const {storage: storageEndpoint} = useAxios()
const {t} = useI18n()
const route = useRoute()

const {
  id
} = defineProps<{
  id: string
}>()

const items = ref<Array<ItemSummarySchema>>([])

onBeforeMount(() => {
  storageEndpoint.getStorageItems(id).then(({success, data, error}) => {
    if(!success){
      //TODO
    }
    items.value = data ?? []
  })
})
</script>

<template>
  <item-summary-list
    v-model="items"
    :from="id"
  />
</template>

<style scoped lang="scss">

</style>