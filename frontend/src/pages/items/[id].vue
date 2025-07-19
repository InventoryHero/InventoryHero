<script setup lang="ts">

import {ItemDetailReadSchema} from "@/api/types/items.ts";
import useStorageHelper from "@/composables/useStorageHelper.ts";
import {computed} from "vue";
import itemAddedEventBus from "@/services/itemAddedEventBus.ts";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";

const contentRefreshStore = useContentRefreshStore()
const {getStorageIcon, getStoragePath} = useStorageHelper()
const route = useRoute()
const {items: itemEndpoint} = useAxios()
const {t} = useI18n()

const item = ref<ItemDetailReadSchema|undefined>()
const loading = ref<boolean>(true)
const loadingStoragePanel = ref<string|undefined>(undefined)


const props = defineProps<{
  id: string
}>()




const fromStorageId = computed(() => {
  const fromStorageParam = route.query.fromStorage;
  if(!fromStorageParam) {
    return undefined
  }
  if (Array.isArray(fromStorageParam)) {
    return fromStorageParam[0] as string;
  }
  return fromStorageParam
});

const breadcrumbs = computed(() => {
  if(!item.value?.breadcrumbs){
    return []
  }
  return item.value.breadcrumbs
})

const loadItem = async (showLoader: boolean, loadRequestingStorage: string|undefined = undefined) => {
  loading.value = showLoader
  loadingStoragePanel.value = loadRequestingStorage
  itemEndpoint.getItemDetails(props.id, fromStorageId.value).then( ({success, data, error}) => {
    if(!success){
      // TODO ERROR
      loading.value = false
      return
    }
    item.value = data!
    loading.value = false
    loadingStoragePanel.value = undefined
  })
}

onBeforeMount(() => {
  loadItem(true)
})

itemAddedEventBus.on((item_id) => {
  if (props.id !== item_id){
    return
  }
  contentRefreshStore.showBanner({
    title: t('items.item.content_changed_title'),
    subtitle: t('items.item.content_changed_subtitle'),
    callback: () => (loadItem(true))
  })
})

</script>

<template>
  <div v-if="loading" class="text-center ">
    <v-skeleton-loader
      type="heading, subtitle, paragraph, actions, divider, list-item@4"
    />
  </div>
  <template v-else-if="item">
    <v-breadcrumbs
        v-if="breadcrumbs.length > 0"
        density="compact"
    >
      <template
          v-if="breadcrumbs.length > 2"
      >
        <v-breadcrumbs-item
           title="..."
           disabled
        />
        <v-icon
            icon="mdi-chevron-right"
        />
      </template>
      <template v-for="(item, index) in breadcrumbs.slice(-2)" :key="item.id">
        <v-breadcrumbs-item
          :to="getStoragePath(item.id, item.type)"
        >
          <span
            class="d-flex align-center"
          >
            <v-icon
                :icon="getStorageIcon(item.type)"

            />
            {{ item.name }}
          </span>
        </v-breadcrumbs-item>
        <v-icon
            v-if="index < breadcrumbs.length-1"
            icon="mdi-chevron-right"
        />
      </template>

    </v-breadcrumbs>
    <item-detail-header
        v-model="item"
        @deleting="deleting => {loading = deleting}"
    />
    <v-divider opacity="50" class="mt-4 mb-4"/>

    <v-expansion-panels  class="pb-16" >
      <item-detail-storage-panel
          v-for="(storage) in item.storage"
          :key="storage.id"
          :item-id="item.id"
          :item-name="item.name"
          :items="item.items"
          :attributes="item.attributes"
          :storage="storage"
          :highlight="fromStorageId === storage.id"
          :loading="loadingStoragePanel === storage.id"
          @reload="(id) => loadItem(false, id)"
      >
      </item-detail-storage-panel>
    </v-expansion-panels>
  </template>
  <div v-else><!--TODO REDIRECT TO ERROR VIEW--></div>
</template>

<style scoped lang="scss">
:deep(.v-card-item){
  padding-bottom: 0;
  margin-bottom: 0;
}
</style>

<route>
{
  "props": true,
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": true,
    "showFab": true
  }
}
</route>