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

const emit = defineEmits<{
  (e: 'reload'): void
}>()

const handleSave = async () => {
  active.value = false
  emit('reload')
}

onBeforeRouteLeave(() => {
  if(active.value) {
    return false
  }
})

</script>

<template>
  <v-dialog
      v-model="active"
      persistent
  >
    <v-card
      title="hallo"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="emit('reload')"
        />
      </template>
      <v-card-actions>
        <v-btn
            v-bind="btnStyle"
            :text="t('items.item.instance.edit.cancel')"
            @click="active = false"
        />
        <v-spacer/>
        <v-btn
            v-bind="btnStyle"
            :text="t('items.item.instance.edit.save')"
            @click="handleSave"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>