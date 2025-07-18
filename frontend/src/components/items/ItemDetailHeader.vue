<script setup lang="ts">
  import {ItemReadSchema} from "@/api/types/items.ts";
  import useAppStyling from "@/composables/useAppStyling.ts";

  const {t} = useI18n()
  const {btnStyle} = useAppStyling()
  const  {items: itemEndpoint} = useAxios()
  const router = useRouter()

  const item = defineModel<ItemReadSchema>({
    required: true
  })
  const hasImage = computed(() => {
    return false
  })

  const emit = defineEmits<{
    (e: "deleting", payload: boolean): void
  }>()

  const deleteConfirmationVisible = ref<boolean>(false);
  const editDialogVisible = ref<boolean>(false);

  const edit = () => {
    // TODO
    editDialogVisible.value = true
  }
  const deleteItem = () => {
    if(!deleteConfirmationVisible.value) {
      deleteConfirmationVisible.value = true
      return
    }
    emit('deleting', true)
    itemEndpoint.deleteItem(item.value.id).then(({success, data, error}) => {
      if(!success){
        // TODO
      }
      deleteConfirmationVisible.value = false
      router.push("/items")
    })
  }


</script>

<template>
  <confirm-item-delete-dialog
    v-model="deleteConfirmationVisible"
    @delete="deleteItem"
  />
  <edit-item-dialog
    v-model="editDialogVisible"
    v-model:item="item"
  />

  <v-card
      width="100%"
  >
    <template v-slot:prepend>
      <v-avatar v-if="hasImage">
        <v-img
            src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
        />
      </v-avatar>
    </template>
    <template v-slot:title>
        <span class="text-wrap">
          {{ item.name }}
        </span>
    </template>
    <template v-slot:subtitle>
      <v-chip-group
          base-color="primary"
          show-arrows
      >
        <category-chip
            v-for="category in item.categories"
            :category="category"
        >
          {{ category.name }}
        </category-chip>
      </v-chip-group>
    </template>

    <v-card-text>

      <template v-if="item.description"> {{item.description}}</template>
    </v-card-text>
    <v-card-actions>
      <v-spacer/>

        <v-btn
            prepend-icon="mdi-trash-can"
            @click="deleteItem"
            :text="t('items.item.delete')"
            density="comfortable"
            class="text-none"
            color="error"
        />
        <v-btn
            prepend-icon="mdi-pencil"
            @click="edit"
            :text="t('items.item.edit.button')"
            density="comfortable"
            color="primary"

            class="text-none"
        />

    </v-card-actions>
  </v-card>

</template>

<style scoped lang="scss">

</style>