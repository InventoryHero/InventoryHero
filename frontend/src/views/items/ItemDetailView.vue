<script setup lang="ts">

import useAppStyling from "@/composables/useAppStyling.ts";
import {BreadcrumbSchema, ItemDetailReadSchema} from "@/api/types/items.ts";
import useStorageHelper from "@/composables/useStorageHelper.ts";
import {computed} from "vue";

const {btnStyle} = useAppStyling()
const {getStorageIcon, getStoragePath} = useStorageHelper()
const route = useRoute()
const router = useRouter()
const {items: itemEndpoint} = useAxios()
const {t, d} = useI18n()


const item = ref<ItemDetailReadSchema|undefined>()
const loading = ref<boolean>(true)


const {
  id
} = defineProps<{
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

const loadItem = async (showLoader: boolean) => {
  loading.value = showLoader
  itemEndpoint.getItemDetails(id, fromStorageId.value).then( ({success, data, error}) => {
    if(!success){
      // TODO ERROR
      loading.value = false
      return
    }
    item.value = data!
    loading.value = false
  })
}

onBeforeMount(() => {
  loadItem(true)
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

    <v-expansion-panels  class="pb-16">
      <item-detail-storage-panel
          v-for="(storage) in item.storage"
          :key="storage.id"
          :item-id="item.id"
          :items="item.items"
          :attributes="item.attributes"
          :storage="storage"
          :highlight="fromStorageId === storage.id"
          @reload="loadItem(false)"
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