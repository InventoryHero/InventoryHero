<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";

const {t} = useI18n();
const {btnStyle} = useAppStyling()

const {name} = defineProps<{name: string}>()

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
  >
    <v-card>
      <v-card-title>
        <i18n-t keypath="boxes.box.delete_confirmation.title">
          <template #name>
              <span class="text-primary">{{ name }}</span>
          </template>
        </i18n-t>
  
      </v-card-title>
      <v-card-text>
        {{t('boxes.box.delete_confirmation.text')}}
      </v-card-text>
      <v-card-actions>
        <v-btn
            v-bind="btnStyle"
            prepend-icon="mdi-cancel"
            :text="t('boxes.box.delete_confirmation.cancel')"
            @click="deleteConfirmationVisible = false"
        />
        <v-spacer />
        <v-btn
            v-bind="btnStyle"
            prepend-icon="mdi-trash-can"
            color="error"
            :text="t('boxes.box.delete_confirmation.confirm')"
            @click="emit('delete')"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>