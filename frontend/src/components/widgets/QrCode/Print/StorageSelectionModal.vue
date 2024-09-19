<script setup lang="ts">

import {useStorage} from "@/store";
import {StorageTypes} from "@/types";
import {useTemplateRef} from "vue";

const storageStore = useStorage();
const {t} = useI18n()

const storageType = inject('storageType') as StorageTypes
const storage = computed(() => {
  return storageStore.getStorage(storageType) ?? []
})

const selected = computed(() => {
  return storageStore.printSelection
})

const scroller = useTemplateRef('scroller')

const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'selectionConfirmed'): void
}>()

const allSelected = computed(() => {
  return storage.value.length === selected.value.length
})

const someSelected = computed(() => {
  return selected.value.length > 0 && storage.value.length !== selected.value.length

})

function selectItem(id: number){
  storageStore.selectForPrinting(id)
}

function toggleAll(){
  if(allSelected.value){
    storageStore.deselectAllFromPrinting()
    return
  }
  storage.value.forEach((s) => {
    storageStore.selectForPrinting(s.id, true)
  })
}


onBeforeMount(() => {
  storageStore.deselectAllFromPrinting()
})

</script>

<template>

 <v-card
     class="position-relative d-flex flex-column fill-height"
 >
   <v-card-title
      class="d-flex justify-space-between align-center"
   >
     <span>
       {{ $t('storage_selection.title') }}
     </span>

     <app-icon-btn
       icon="mdi-close"
       @click="emit('close')"
     />
   </v-card-title>
   <v-card-text
       class="flex-1-1 overflow-hidden"
   >
     <v-virtual-scroll
         ref="scroller"
         :items="storage"
         style="height: 100%"
     >
       <template v-slot:default="{item}">
         <v-checkbox
             color="primary"
             :model-value="selected.includes(item.id)"
             @update:model-value="selectItem(item.id)"
             hide-details
             density="compact"

         >
           <template v-slot:label>
             <span
              class="ms-2 text-subtitle-1"
             >
               {{ item.name }}
             </span>
           </template>
         </v-checkbox>
       </template>
     </v-virtual-scroll>
   </v-card-text>
   <v-card-actions
       class="d-flex justify-space-between"
   >
       <v-checkbox
         :hide-details="true"
         :model-value="allSelected"
         :indeterminate="someSelected && !allSelected"
         @click="toggleAll"
         color="primary"
         density="compact"
       >
         <template v-slot:label>
           <span
            class="ms-2 text-subtitle-1"
           >
             {{!allSelected ? $t('storage_selection.select_all') : $t('storage_selection.deselect_all')}}
           </span>
         </template>
      </v-checkbox>
      <v-btn
        prepend-icon="mdi-plus-box-outline"
        @click="emit('selectionConfirmed')"
      >
        {{ t('storage_selection.select_ok') }}
      </v-btn>
   </v-card-actions>
 </v-card>
</template>

<style scoped lang="scss">

</style>