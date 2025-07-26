<script setup lang="ts">
import {ItemSummarySchema} from "@/api/types/items.ts";
import {BoxResponseSchema} from "@/api/types/storage.ts";

const {storage: storageEndpoint} = useAxios()
const {t} = useI18n()
const router = useRouter()
const {openModal} = useGlobalModal()

const {
  id
} = defineProps<{
  id: string
}>()

const loading = ref<boolean>(false)

const box = ref<BoxResponseSchema>()
const items = ref<Array<ItemSummarySchema>>([])
const deleteBoxModalVisible = ref(false)

const loadBox = async () => {
  const {success, data, error} = await storageEndpoint.getStorageDetail(id)
  if(!success){
    // TODO REDIRECT TO ERROR PAGE
  }
  box.value = data! as BoxResponseSchema
}

const loadBoxContent = async () => {
  const {success, data, error} = await storageEndpoint.getStorageItems(id)

  if(!success){
    // TODO REDIRECT TO ERROR PAGE
  }

  items.value = data ?? []
}

const deleteBox = async (confirmed: boolean) => {
  if(!confirmed){
    deleteBoxModalVisible.value = true
    return
  }

  const {success, error} = await storageEndpoint.deleteStorage(id)
  if(!success){
    // TODO
    return
  }
  deleteBoxModalVisible.value = false
  router.push(`/storage/boxes`)
}
const editBox = async () => {
  openModal("editBoxModal", {
    box: box.value,
    'onUpdate:box': (newValue: BoxResponseSchema) => box.value = newValue
  })
}

onBeforeMount(async () => {
  loading.value = true
  await loadBox()
  await loadBoxContent()
  loading.value = false
})
</script>

<template>
  <confirm-box-delete-modal
    v-model="deleteBoxModalVisible"
    @delete="deleteBox(true)"
  />
  <div
      v-if="loading"
  >
    this loading
  </div>
  <template v-else-if="items && box">
    <v-card>
      <template v-slot:prepend>
        <v-icon
          icon="mdi-package-variant"
        />
      </template>
      <template v-slot:title>
        {{ box.name }}
      </template>
      <template v-if="box.parent_id" v-slot:subtitle>
        {{ t(`boxes.box.stored_at`, {parent: box.parent?.name}) }}
      </template>
      <v-card-actions>
        <v-spacer/>
        <v-btn
            prepend-icon="mdi-trash-can"
            @click="deleteBox(false)"
            :text="t('boxes.box.delete')"
            density="comfortable"
            color="error"
            varaint="tonal"
            class="text-none"
        />
        <v-btn
            prepend-icon="mdi-pencil"
            @click="editBox"
            :text="t('boxes.box.edit')"
            density="comfortable"
            color="primary"
            class="text-none"
        />
      </v-card-actions>
    </v-card>

    <v-divider class="mt-2 mb-2" :thickness="2" />

    <v-row dense v-if="!loading" class="pb-16">
      <v-col
          v-for="item in items"
          cols="12"
          sm="6"
          md="6"
          lg="4"
          xl="3"
      >
        <item-summary-card
            :item="item"
            :from="id"
        />
      </v-col>
    </v-row>
  </template>
  <div v-else><!--TODO REDIRECT TO ERROR VIEW--></div>
</template>

<style scoped lang="scss">

</style>

<route>
{
  "props": true,
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": true,
    "title": 'titles.boxes',
    "showFab": true
  }
}
</route>