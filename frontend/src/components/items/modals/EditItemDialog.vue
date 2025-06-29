<script setup lang="ts">
import {CategoryReadSchema, ItemReadSchema, ItemSummarySchema, ItemUpdateSchema} from "@/api/types/items.ts";
import useAppStyling from "@/composables/useAppStyling.ts";
import {StorageResponseSchema} from "@/api/types/storage.ts";

const {t} = useI18n();
const {btnStyle, textFieldStyling, selectStyling, textAreaStyle} = useAppStyling()
const {items: itemEndpoint} = useAxios()

const active = defineModel<boolean>({
  required: true
})

const item = defineModel<ItemReadSchema>('item', {
  required: true
})

const nameRules = ref([
  (v: string|null|ItemSummarySchema) => {
    if (!v) {
      return t('items.item.edit.name_required')
    }
    if (typeof v === 'object') {
      return !!(v as ItemSummarySchema).name?.trim() || t('items.item.edit.name_required')
    }
    return !!String(v).trim() || t('items.item.edit.name_required')
  }
])
const descriptionRules = ref([
  (v: string|null) => (v ?? '').length < 1024 || t('items.item.edit.description_too_long')
])

const editForm = useTemplateRef("editForm")
const name = ref<string|null>(item.value.name)
const description = ref<string|null|undefined>(item.value.description)
const selectedCategories = ref<string[]>(item.value.categories.map(cat => cat.id))
const loadingCategories = ref<boolean>(false)
const categories = ref<CategoryReadSchema[]>([])
const loading = ref<boolean>(false)

const categoriesChanged = computed(() => {
  if(item.value.categories.length !== selectedCategories.value.length){
    return true
  }
  const selected = new Set(selectedCategories.value)
  for (const category of item.value.categories){
    if (!selected.has(category.id)) {
      return true
    }
  }
  return false
})

const loadCategories = async () => {
  loadingCategories.value = true
  const {success, data, error} = await itemEndpoint.getAllCategories()
  if(!success) {
    // TODO
  }
  categories.value = (data ?? []) as CategoryReadSchema[]
  loadingCategories.value = false
}

const handleResetName = () => {
  name.value = item.value.name
}

const handleResetDescription = () => {
  description.value = item.value.description
}

const handleResetCategories = () => {
  selectedCategories.value = item.value.categories.map(cat => cat.id)
}

const handleSave = async () => {
  const {valid} = await editForm.value.validate()
  if(!valid){
    return
  }
  loading.value = true
  const currentSet = new Set(selectedCategories.value)
  const originalSet = new Set(item.value.categories.map(cat => cat.id))

  let updateData: ItemUpdateSchema = {
    name: name.value !== item.value.name ? name.value : undefined,
    description: description.value !== item.value.description ? description.value ?? "" : undefined,
    categories_to_add: [...currentSet].filter(id => !originalSet.has(id)),
    categories_to_remove: [...originalSet].filter(id => !currentSet.has(id))
  }
  console.log(updateData)
  const {success, data, error} = await itemEndpoint.updateItem(item.value.id, updateData)
  if(!success){
    // TODO
  }

  item.value.name = data!.name
  item.value.description = data!.description
  item.value.categories = data!.categories

  handleResetName()
  handleResetDescription()
  handleResetCategories()

  loading.value = false
}

onBeforeRouteLeave(() => {
  if(active.value) {
    return false
  }
})
onBeforeMount(() => {
  loadCategories()
})
</script>

<template>
<v-dialog
  v-model="active"
  persistent
>
  <v-card
    :loading="loading"
    :disabled="loading"
    :title="t('items.item.edit.title')"
  >
    <template v-slot:append>
      <v-icon-btn
        icon="mdi-close"
        @click="active = false"
      />
    </template>
    <v-card-text>
      <v-form
        ref="editForm"
        @submit.prevent=""
      >
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-bind="textFieldStyling"
              :label="t('items.item.edit.name')"
              v-model="name"
              :rules="nameRules"
              :append-inner-icon="item.name !== name ? 'mdi-undo' : ''"
              @click:append-inner="handleResetName"
           />
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-bind="textAreaStyle"
              :label="t('items.item.edit.description')"
              v-model="description"
              :rules="descriptionRules"
              :counter="1024"
              @click:clear="description = undefined"
              :append-inner-icon="item.description !== description ? 'mdi-undo' : ''"
              @click:append-inner="handleResetDescription"
            />
          </v-col>
          <v-col cols="12">
            <v-select
              v-bind="selectStyling"
              :label="t('items.item.edit.categories')"
              v-model="selectedCategories"
              :items="categories"
              :loading="loadingCategories"
              item-title="name"
              item-value="id"
              multiple
              :append-icon="categoriesChanged ? 'mdi-undo' : ''"
              @click:append="handleResetCategories"
            >
              <template v-slot:selection="{ item, index }">
                <v-chip
                    v-if="index < 2"
                    :text="item.title"
                    density="comfortable"
                />
                <v-chip
                    v-if="index === 2"
                    density="comfortable"
                    :text="t('items.item.edit.categories_overflow', selectedCategories.length - 2)"
                />
              </template>
            </v-select>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn
        v-bind="btnStyle"
        :text="t('items.item.edit.cancel')"
        @click="active = false"
      />
      <v-spacer/>
      <v-btn
          v-bind="btnStyle"
          :text="t('items.item.edit.save')"
          @click="handleSave"
      />
    </v-card-actions>
  </v-card>
</v-dialog>
</template>

<style scoped lang="scss">

</style>