<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";

const {t} = useI18n();
const {btnStyle} = useAppStyling()

const deleteConfirmationVisible = defineModel<boolean>({
  required: true
})

const emit = defineEmits<{
  (e: "delete"): void
}>()

onBeforeRouteLeave(() => {
  if(deleteConfirmationVisible.value) {
    return false
  }
})
</script>

<template>
  <v-dialog
      v-model="deleteConfirmationVisible"
      persistent
      :close-on-back="false"
  >
    <v-card>
      <v-card-title>
        {{t('items.item.delete_confirmation.title')}}
      </v-card-title>
      <v-card-text>
        {{t('items.item.delete_confirmation.text')}}
      </v-card-text>
      <v-card-actions>
        <v-btn
            v-bind="btnStyle"
            :text="t('items.item.delete_confirmation.cancel')"
            @click="deleteConfirmationVisible = false"
        />
        <v-spacer />
        <v-btn
            v-bind="btnStyle"
            :text="t('items.item.delete_confirmation.confirm')"
            @click="emit('delete')"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>