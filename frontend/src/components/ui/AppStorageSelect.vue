<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Storage, StorageTypes} from "@/types";
import useNewAxios from "@/composables/useAxios.ts";
import {StorageEndpoint} from "@/api/http";

export default defineComponent({
  name: "AppStorageSelect",
  setup(){
    const {axios} = useNewAxios("storage")
    return {axios: axios as StorageEndpoint}
  },
  emits:{
    'update:modelValue'(payload: Storage){
      console.log(payload)
      return true
    }
  },
  computed:{
    storage: {
      get(): Storage|null{
        return this.modelValue ?? null
      },
      set(value: Storage)
      {
        this.$emit('update:modelValue', value)
      }
    },
    type(){
      switch(this.storage?.type){
        case StorageTypes.Box:
          return StorageTypes.Box
        case StorageTypes.Location:
          return StorageTypes.Location
        default:
          return StorageTypes.NoStorage
      }
    },
    container(){
      if(this.contentType === "product")
      {
        return this.allStorage
      }

      return this.allStorage.filter((item) => item.type === StorageTypes.Location)
    }
  },
  props:{
    modelValue: {
      type: Object as PropType<Storage> | null
    },
    contentType:{
      type: String as PropType<"box"|"product">,
      default: "box"
    },
    density: {
      type: String,
      default: "compact"
    },
    hideDetails: {
      type: Boolean,
      default: false
    }
  },
  data(){
    return{
      allStorage: [] as Array<Storage>,
      storageLoading: false,
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
      return item.id === this.storage?.id && item.type === this.storage?.type
    }
  },
  async mounted(){
    this.storageLoading = true
    let storage = (await this.axios.getStorageType({contained: false})) as Array<Storage>
    this.storageLoading = false
    this.allStorage = storage
  }
})
</script>

<template>
  <v-select
      v-bind="$attrs"
      v-model="storage"
      :density="density"
      :single-line="true"
      :hide-details="hideDetails"
      color="primary"
      variant="filled"
      :items="container"
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