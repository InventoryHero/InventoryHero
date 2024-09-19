<script setup lang="ts">

import {useContentFilterStore, useProducts, useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {LocationEndpoint} from "@/api/http";
import {StorageTypes} from "@/types";
import {TabType} from "@/types/TabType.ts";
import {ref} from "vue";
import useConfirmationSetup from "@/composables/useConfirmationSetup.ts";

provide("storageType", StorageTypes.Location)

const storageStore = useStorage()
const productStore = useProducts()
const contentFilterStore = useContentFilterStore()
const route = useRoute()
const {t} = useI18n()
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")
const {goBackOneLevel} = useGoBackOneLevel()



const location = computed(() => storageStore.selectedLocation)

const locationBoxes = computed(() => {
  return storageStore.boxes
})

const locationProducts = computed(() => {
  return productStore.productStorage
})



const locationName = computed({
  get(){
    if(newName.value !== undefined){
      return newName.value
    }
    return location.value?.name
  },
  set(value: string){
    newName.value = value
  }
})


const loadingContent = computed(() => storageStore.loadingContent)
const loadingLocation = computed(() => storageStore.loadingStorage)

const saving = ref(false)
const deleting = ref(false)
const newName = ref<string|undefined>(undefined)
const nameRequiredRule = (value: string) => value !== '' || t('locations.location.rules.new_name_empty')
const editClicked = ref(false)

function cancelEdit(){
  newName.value = undefined
  editClicked.value = false
}
function saveChanges(){
  if(newName.value === ''){
    return
  }
  saving.value = true
  locationEndpoint.updateLocation(location.value?.id ?? -1, {
    name: newName.value
  }).then(({updated}) => {
    if(updated){
      storageStore.updateLocation(updated)
    }
    saving.value = false
    cancelEdit()
  })

}
function deleteLocation(){
  deleting.value = true
  const id = location.value?.id ?? -1
  locationEndpoint.deleteStorage(location.value?.id ?? -1).then((success) => {
    deleting.value = false
    if(!success){
      return
    }
    goBackOneLevel().then(() => {
      storageStore.deleteLocation(id)
    })
  })
}

const {
  confirmationDialog,
  saveAction: saveDelete,
  reallyDo
} = useConfirmationSetup(deleteLocation)


function closeLocation(){
  goBackOneLevel()
}

const tab = ref<TabType>(TabType.Box)
onMounted(() => {
  tab.value= contentFilterStore.popTab(route.fullPath) ?? TabType.Box

})
</script>

<template>
  <confirmation-dialog
      :dialog-opened="confirmationDialog"
      :title="$t('locations.confirm_delete.title')"
      :text="$t('locations.confirm_delete.text')"
      :confirm-text="$t('locations.confirm_delete.confirm')"
      :cancel-text="$t('locations.confirm_delete.cancel')"
      confirm-icon="mdi-delete-outline"
      cancel-icon="mdi-cancel"
      :on-cancel="() => confirmationDialog = false"
      :on-confirm="reallyDo"
  />
  <v-card
      class="position-relative d-flex flex-column fill-height fill-width"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="loadingContent || loadingLocation || deleting || saving"
          color="primary"
      />
    </template>
    <template
        v-if="!loadingLocation"
    >
      <app-content-title
          v-model:edit="editClicked"
          v-model:title="locationName"
          :rules="[nameRequiredRule]"
          edit-toggles-textfield
          :disabled="deleting || saving"
          @close="closeLocation"
      />
      <v-card-subtitle>
        <v-tabs
            :disabled="loadingContent"
            density="compact"
            color="primary"
            v-model="tab"
        >
          <v-tab
              :value="TabType.Box"
          >
            {{ t('locations.tabs.box') }}
          </v-tab>
          <v-tab
              :value="TabType.Product"
          >
            {{ t('locations.tabs.product') }}
          </v-tab>
        </v-tabs>
      </v-card-subtitle>
      <div class="flex-1-1 fill-width">
        <v-tabs-window
            v-if="!loadingContent"
            v-model="tab"
            class="fill-height fill-width"
        >
          <location-tab
            :tab="TabType.Box"
            :items="locationBoxes"
            :loading-content="loadingContent"
          />
          <location-tab
            :tab="TabType.Product"
            :items="locationProducts"
            :loading-content="loadingContent"
          />
        </v-tabs-window>
        <app-content-scroll-after
          v-else
          class="mt-2"
          :text="t('locations.location.loading_content') "
        />
      </div>
      <app-content-actions
        :active="editClicked"
        :saving="saving"
        :deleting="deleting"
        @cancel="cancelEdit"
        @save="saveChanges"
        @delete="saveDelete"
      />
      <v-card-actions
          v-if="!editClicked"
          class="pb-0 pt-0 mt-0 mb-0"
      >
        <app-storage-qr-code-btn
            color="primary"
            use-preselected
        />
      </v-card-actions>
    </template>
    <app-content-scroll-after
        v-else
        class="mt-2"
        :text="t('locations.loading')"
    />
  </v-card>
</template>

<style scoped lang="scss">

</style>