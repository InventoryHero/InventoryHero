<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Storage, StorageTypes} from "@/types";
import useNewAxios from "@/composables/useAxios.ts";
import {StorageEndpoint} from "@/api/http";

export default defineComponent({
  name: "AppStorageSelect",
  setup(){

  },
  emits:{
    'update:modelValue'(payload: Storage){
      return true
    }
  },
  computed:{
    selected: {
      get(): Storage|null{
        return this.modelValue ?? null
      },
      set(value: Storage)
      {
        this.$emit('update:modelValue', value)
      }
    },
    type(){
      switch(this.selected?.type){
        case StorageTypes.Box:
          return StorageTypes.Box
        case StorageTypes.Location:
          return StorageTypes.Location
        default:
          return StorageTypes.NoStorage
      }
    },
    container(){
      return this.selected
    }
  },
  props:{
    modelValue: {
      type: Object as PropType<Storage> | null
    },
    storage: {
      type: Array<Storage>,
      default: []
    },
    density: {
      type: String,
      default: "compact"
    },
    hideDetails: {
      type: Boolean,
      default: false
    },
    storageLoading: {
      type: Boolean,
      default: false
    }
  },
  data(){
    return{
      allStorage: [] as Array<Storage>,
    }
  },
  methods:{
    getIcon(type: StorageTypes){
      switch(type){
        case StorageTypes.Location:
          return "fa:fas fa-building"
        case StorageTypes.Box:
          return "fa:fas fa-boxes"
        default:
          return ""
      }
    },
    getActive(item: Storage): boolean{
      return item.id === this.selected?.id && item.type === this.selected?.type
    }
  },
})
</script>

<template>
  <v-select
      v-bind="$attrs"
      v-model="selected"
      :density="density"
      :single-line="true"
      :hide-details="hideDetails"
      color="primary"
      variant="filled"
      :items="storage"
      item-title="name"
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
          :active="getActive(item.raw)"
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