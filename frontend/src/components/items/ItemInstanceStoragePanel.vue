<script setup lang="ts">
import {ItemAttributesBaseSchema, ItemStorageReadSchema} from "@/api/types/items.ts";

const {t, d} = useI18n()
const {items: itemEndpoint} = useAxios()
const {
  itemId,
  instance,
  attributes
} = defineProps<{
  itemId: string
  instance: ItemStorageReadSchema,
  attributes: ItemAttributesBaseSchema
}>()

const emit = defineEmits<{
  (e: 'consume'): void,
  (e: 'reload'): void,
}>()

const quantityLoading = ref<boolean>(false)
const editItemInstanceDialogVisible = ref<boolean>(false)

const formatExpirationDate = (expirationDate: string|null|undefined) => {
  if(!expirationDate){
    return t('items.attributes.no_expiration_set')
  }
  const date = new Date(expirationDate)
  if(isNaN(date.getTime())){
    return t('items.attributes.invalid_expiration_set')
  }
  return d(date, 'short')
}

const addInstance = () => {
  // TODO ADD INSTANCE
}

const consumeInstance = async () => {
  console.log(instance)
  quantityLoading.value = true
  const {success, data, error} = await itemEndpoint.consumeItemInstance(itemId, instance.id)
  if (!success) {
    // TODO REDIRECT TO ERROR PAGE
  }
  emit('consume')
  quantityLoading.value = false
}

const edit = () => {
  editItemInstanceDialogVisible.value = true
}
const deleteAllInstances = () => {
  // TODO
}
</script>

<template>
  <edit-item-instance-dialog
      v-model="editItemInstanceDialogVisible"
      @reload="emit('reload')"
  />
  <v-card
      height="fit-content"
      max-height="400"
      variant="outlined"
      class="mt-1 mb-1 overflow-y-scroll"

  >
    <v-card-text>
      <v-list>
        <v-list-item
            :disabled="quantityLoading"
            :loading="quantityLoading"
        >
          <v-list-item-title
              class="text-wrap"

          >
            {{t('items.attributes.quantity')}}
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-icon-btn
                icon="mdi-minus"
                class="me-2"
                @click="consumeInstance"
            />
            <span>
              {{ instance.quantity }}
            </span>
            <v-icon-btn
                class="ms-2"
                icon="mdi-plus"
                @click="addInstance"
            />
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item
            :title="t('items.attributes.expiry_date')"
            :subtitle="formatExpirationDate(attributes.expiration_date)"
        />
        <v-list-item>
          <v-list-item-title
              class="text-wrap"
          >
            {{t('items.attributes.serial_number')}}
          </v-list-item-title>
          <v-list-item-subtitle
              class="text-wrap"
          >
            {{attributes.serial_number ?? ''}}
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item>
          <v-list-item-title
              class="text-wrap"
          >
            {{t('items.attributes.batch')}}
          </v-list-item-title>
          <v-list-item-subtitle
              class="text-wrap"
          >
            {{attributes.batch_code ?? ''}}
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item>
          <v-list-item-title
              class="text-wrap"
          >
            {{t('items.attributes.notes')}}
          </v-list-item-title>
          <v-list-item-subtitle
              class="text-wrap"
          >
            {{attributes.notes ?? ''}}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-spacer/>
      <v-btn
        prepend-icon="mdi-trash-can"
        :text="t('items.attributes.delete')"
        class="text-none"
        density="compact"
        variant="tonal"
        color="error"
        @click="deleteAllInstances"
      />
      <v-btn
          density="compact"
          prepend-icon="mdi-pencil"
          :text="t('items.attributes.edit')"
          class="text-none"
          color="primary"
          @click="edit"
      />
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">

</style>