<script setup lang="ts">

const emit = defineEmits<{
  (e: 'cancel'): void,
  (e: 'delete'): void,
  (e: 'save'): void
}>()

const {
  active,
  saving=false,
  deleting=false
} = defineProps<{
  active: boolean,
  saving?: boolean,
  deleting?: boolean,
}>()
</script>

<template>
  <v-card-actions
      v-if="active"
      class="overflow-auto"
  >
    <v-btn
        prepend-icon="mdi-cancel"
        @click="emit('cancel')"
        :text="$t('cancel')"
        :disabled="saving||deleting"
    />
    <v-spacer />
    <v-btn
        variant="tonal"
        color="red"
        prepend-icon="mdi-trash-can"
        :text="$t('delete')"
        @click="emit('delete')"
        :disabled="saving"
        :loading="deleting"
    />
    <v-btn
        :text="$t('save')"
        prepend-icon="mdi-content-save-all"
        color="primary"
        variant="elevated"
        :loading="saving"
        :disabled="deleting"
        @click="emit('save')"
    />
  </v-card-actions>
</template>

<style scoped lang="scss">

</style>