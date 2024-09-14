<script setup lang="ts">
import {ApiStorage, StorageTypes} from "@/types";

defineOptions({
  inheritAttrs: false
})

const selected = defineModel<ApiStorage|null>()

const {
  storageLoading=false,
  storage = []
} = defineProps<{
  storageLoading?: boolean,
  storage?: Array<ApiStorage>
}>()

function getIcon(type: StorageTypes){
  switch(type){
    case StorageTypes.Location:
      return "mdi-archive-marker"
    case StorageTypes.Box:
      return "mdi-package-variant"
    default:
      return "mdi-archive-off"
  }
}
</script>

<template>
  <v-select
      v-bind="$attrs"
      v-model="selected"
      :single-line="true"
      color="primary"
      variant="filled"
      :items="storage"
      item-title="name"
      item-value="id"
      :chips="true"
      :clearable="true"
      :persistent-clear="true"
      :loading="storageLoading"
      :return-object="true"
      :disabled="storageLoading"
  >
    <template v-slot:item="{props, item}">
      <v-list-item
          v-bind="props"
          :title="item.title"
          :prepend-icon="getIcon(item.raw.type)"
      >
        <template v-slot:prepend>
          <v-icon size="small"/>
        </template>
      </v-list-item>
    </template>
    <template #append>
      <slot name="hint" />
    </template>
    <template #no-data>
      <v-list-item
      >
        <v-list-item-title
          class="text-wrap"
        >
          {{ $t('storage.select.no_storage') }}
        </v-list-item-title>

      </v-list-item>
    </template>
  </v-select>

</template>

<style scoped lang="scss">
</style>