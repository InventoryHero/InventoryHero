<script setup lang="ts">

import {useProducts} from "@/store";
import {useI18n} from "vue-i18n";
import {ProductStorageMapping, Storage} from "@/types/api.ts";
import {computed, ref} from "vue";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";
import useUpdateProductStoredAt from "@/composables/useModifyProductStoredAt.ts";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";


const {t: $t} = useI18n()
const productStore = useProducts()
const {saving, deleting, updateStoredAt, deleteStoredAt} = useUpdateProductStoredAt()
const {redirect} = useRedirectToStorage()


const emit = defineEmits<{
  (e: 'showStoredAtDetail'): void,
  (e: 'deleted', id: number, amount: number): void
}>()

const props = defineProps<{
  storage?: ProductStorageMapping
}>()

const productName = computed(() => {
  return productStore.selectedProduct?.name
})

const productStorage = computed(() => {
  return props.storage!
})
const storage = computed(() => {
  return productStorage.value.storage
})

const {name, icon} = useStorageTitle(storage)


function deleteMe(){
  // TODO CONFIRMATION MODAL
  deleteStoredAt(productStorage.value).then((success) => {
    if(!success){
      return
    }
    emit('deleted', productStorage.value.id, productStorage.value.amount)
  })
}

function adjustAmount(increment: number){
  updateStoredAt(productStorage.value, {
    amount: productStorage.value.amount+increment,
    storage: productStorage.value.storage
  })
}

function showStoredAtDetail(){
  productStore.selectProductStoredAt(productStorage.value)
  emit('showStoredAtDetail')
}

</script>

<template>
  <v-row
      :no-gutters="true"
      justify="space-between"
      v-bind="$attrs"
  >
    <v-col
        class="d-flex justify-start align-center"
    >
        <app-storage-title
            :icon="icon"
            color="primary"
            :title="name"
            variant="tonal"
            @click="redirect(storage, productName ?? '')"
        />
    </v-col>
  </v-row>
  <v-row
      :no-gutters="true"
      justify="space-between"

  >
    <v-col
    >
      {{ $t("products.product.amount") }}
    </v-col>
    <v-col
        cols="2"
        class="d-flex justify-end"
    >
      {{ productStorage.amount }}
    </v-col>
  </v-row>
  <v-row
      :no-gutters="true"
      justify="space-between"

  >
    <v-col
    >
      {{ $t('products.product.last_used')}}
    </v-col>
    <v-col
        cols="2"
        class="d-flex justify-end"
    >
      {{ $d(new Date(productStorage.updatedAt)) }}
    </v-col>
  </v-row>
  <quick-actions
      :request-in-progress="saving || deleting"
      @delete-me="deleteMe()"
      @update-amount="adjustAmount"
      @show-details="showStoredAtDetail"
  />

  <v-divider color="primary" class="border-opacity-75"/>
</template>

<style scoped lang="scss">

</style>