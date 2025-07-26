<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";

const {t} = useI18n();
const {btnStyle} = useAppStyling()
const {
  name
} = defineProps<{
  name: string
}>()

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
      width="auto"
      max-width="60vw"
  >
    <v-card>
      <v-card-title>
        <i18n-t keypath="rooms.room.delete_confirmation.title">
          <template #name>
            <span class="text-primary">{{name}}</span>
          </template>
        </i18n-t>
      </v-card-title>
      <v-card-text>
        {{t('rooms.room.delete_confirmation.text')}}
      </v-card-text>
      <v-card-actions
        justify="end"
      >
        <v-btn
            v-bind="btnStyle"
            prepend-icon="mdi-cancel"
            :text="t('rooms.room.delete_confirmation.cancel')"
            @click="deleteConfirmationVisible = false"
        />
        <v-btn
            v-bind="btnStyle"
            prepend-icon="mdi-trash-can"
            color="error"
            :text="t('rooms.room.delete_confirmation.confirm')"
            @click="emit('delete')"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>