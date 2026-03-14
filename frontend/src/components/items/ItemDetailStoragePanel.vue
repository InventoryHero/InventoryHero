<script setup lang="ts">
import {StorageResponseSchema, StorageType} from "@/api/types/storage.ts";
import useStorageHelper from "@/composables/useStorageHelper.ts";
import {ItemAttributesBaseSchema, ItemStorageReadSchema} from "@/api/types/items.ts";
import ItemInstanceStoragePanel from "@/components/items/ItemInstanceStoragePanel.vue";
const router = useRouter()
const {getStorageIcon, getStoragePath} = useStorageHelper()

type StorageMap = Record<string, ItemStorageReadSchema[]>
type AttributeMap = Record<string, ItemAttributesBaseSchema>



const {
  itemId,
  itemName,
  storage,
  items,
  attributes,
  highlight = false,
  loading = false,
} = defineProps<{
  itemId: string,
  itemName: string,
  storage: StorageResponseSchema,
  items: StorageMap
  attributes: AttributeMap,
  highlight?: boolean,
  loading?: boolean,
}>()


const emit = defineEmits<{
  (e: 'reload', id: string): void
}>()
const color = computed(() => {
  if(highlight){
    return 'primary'
  }
  return undefined
})

const goToStorage = (id: string, type: StorageType) => {
  router.push(getStoragePath(id, type))
}


</script>

<template>

  <v-expansion-panel
      :key="storage.id"

  >
    <v-expansion-panel-title
      :readonly="loading"
    >
      <v-icon
          :icon="getStorageIcon(storage.storage_type)"
          class="me-2"
          :color="color"

      /> <span :class="`text-${color}`">{{storage.name}}</span>
      <template v-slot:actions="{ expanded }">
        <v-icon
            @click.stop="goToStorage(storage.id, storage.storage_type)"
            icon="mdi-arrow-right"
            class="me-2"
        />
        <v-icon :icon="expanded ? 'mdi-chevron-up' : 'mdi-chevron-down'"></v-icon>
      </template>
    </v-expansion-panel-title>
    <v-expansion-panel-text>
      <v-row dense>
        <v-col
            cols="12"
            sm="6"
            md="6"
            lg="4"
            xl="3"
            v-for="(instance) in items[storage.id]" :key="instance.id"
        >
          <item-instance-storage-panel
              :item-id="itemId"
              :item-name="itemName"
              :storage-name="storage.name"
              :instance="instance"
              :attributes="attributes[instance.product_attribute_id]"
              @consume="instance.quantity--"
              @add="instance.quantity++"
              @reload="emit('reload', storage.id)"
              :loading="loading"
          />
        </v-col>
      </v-row>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<style scoped lang="scss">

</style>