<script setup lang="ts">

const {t} = useI18n()

const loading = inject("loading", ref({
  loadingBoxes: true,
  loadingLocations: true,
  loadingProducts: true
}))

const emit = defineEmits<{
  (e: 'clear'): void,
  (e: 'save'): void
}>()

const resourcesLoading = computed(() => Object.values(loading.value).some(value => value))

const {
  requestInProgress=false,
  title
} = defineProps<{
  requestInProgress?: boolean,
  title: string
}>()

function save(){
  if(!resourcesLoading.value){
    emit('save')
  }
}
</script>

<template>
  <v-card
    :loading="requestInProgress || resourcesLoading"
  >
    <template v-slot:loader="{ isActive }">
      <v-progress-linear
          :indeterminate="true"
          :active="isActive"
          color="primary"
      />
    </template>
    <v-card-title
        class="shadowed mb-4"
    >
      {{ title }}
    </v-card-title>
    <v-card-text
        class="create-card-content"
    >
      <slot />
    </v-card-text>

    <v-card-actions
        class="d-flex justify-space-between shadowed mt-4"
    >
      <v-btn
          color="red-lighten-1"
          variant="outlined"
          @click="emit('clear')"
          prepend-icon="mdi-trash-can"
          :text="t('add.clear')"
      />
      <v-btn
          color="primary"
          variant="elevated"
          prepend-icon="mdi-content-save"
          :disabled="resourcesLoading"
          @click="save"
          :text="t('add.save')"
      />
    </v-card-actions>
  </v-card>

</template>

<style scoped lang="scss">

</style>