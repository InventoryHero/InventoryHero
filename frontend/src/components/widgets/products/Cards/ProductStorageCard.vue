<script setup lang="ts">

import {useProducts} from "@/store";
import {useI18n} from "vue-i18n";
import {ProductStorageMapping} from "@/types/api.ts";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import useUpdateProductStoredAt from "@/composables/useModifyProductStoredAt.ts";

const {t: $t} = useI18n()
const productStore = useProducts()
const {saving, deleting, updateStoredAt, deleteStoredAt} = useUpdateProductStoredAt()



const emit = defineEmits<{
  (e: 'showStoredAtDetail'): void,
  (e: 'deleted'): void,
  (e: 'redirect'): void
}>()

const props = defineProps<{
  storage?: ProductStorageMapping,
  fromStorage?: boolean,
  productName?: string
}>()

const fromStorage = computed(() => props.fromStorage ?? false)

const productStorage = computed(() => {
  return props.storage!
})
const productStoredAt = computed(() => {
  return productStorage.value.storage
})

const {name, icon} = useStorageTitle(productStoredAt)
const title = computed(() => {
  if(fromStorage.value){
    const productName = productStore.products.find(p => p.id === productStorage.value?.productId)?.name ?? ''
    return {
      name: productName,
      icon: "mdi-cart"
    }
  }

  return {
    name: name.value,
    icon: icon.value
  }
})


function deleteMe(){
  // TODO CONFIRMATION MODAL
  deleteStoredAt(productStorage.value).then((success) => {
    if(!success){
      return
    }
    emit('deleted')
  })
}

function adjustAmount(increment: number){
  updateStoredAt(productStorage.value, {
    amount: productStorage.value.amount+increment,
    storage: productStorage.value.storage
  })
}

function showStoredAtDetail(){
  emit('showStoredAtDetail')
}

</script>

<template>

  <v-card
    elevation="0"
    density="compact"
  >
    <v-card-text
      class="pb-0 mb-0 pt-3 mt-0"
    >
      <v-row
        dense
      >
        <app-storage-title
            :icon="title.icon"
            :title="title.name"
            color="primary"
            variant="tonal"
            @click="emit('redirect')"
        />
      </v-row>
      <v-row
          dense
          justify="space-between"
      >
        <span>
          {{ $t("products.product.amount") }}
        </span>
        <span>
          {{ productStorage.amount }}
        </span>
      </v-row>
      <v-row
          dense
          justify="space-between"
      >
        <span
        >
          {{ $t('products.product.last_used')}}
        </span>
        <span>
          {{ $d(new Date(productStorage.updatedAt)) }}
        </span>
      </v-row>
      <quick-actions
          :request-in-progress="saving || deleting"
          @delete-me="deleteMe()"
          @update-amount="adjustAmount"
          @show-details="showStoredAtDetail"
      />
    </v-card-text>


    <v-divider color="primary" class="border-opacity-75"/>
  </v-card>
</template>

<style scoped lang="scss">

</style>