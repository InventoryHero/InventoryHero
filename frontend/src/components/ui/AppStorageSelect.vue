<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ApiStorage, StorageTypes} from "@/types";


export default defineComponent({
  name: "AppStorageSelect",
  setup(){

  },
  emits:{
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    'update:modelValue'(payload: ApiStorage){
      return true
    }
  },
  computed:{
    selected: {
      get(): ApiStorage|null{
        return this.modelValue ?? null
      },
      set(value: ApiStorage)
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
      type: Object as PropType<ApiStorage> | null
    },
    storage: {
      type: Array<ApiStorage>,
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
      allStorage: [] as Array<ApiStorage>,
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
    getActive(item: ApiStorage): boolean{
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