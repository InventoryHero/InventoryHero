<template>
  <v-card
    :title="title"
    :text="text"
  >
    <v-card-actions class="d-flex justify-end">
      <v-btn
        color="primary"
        :text="t('households.error.back')"
        variant="tonal"
        to="/households"
      />
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
definePage({
  meta: {
    requiresAuth: true,
    requiresHousehold: false,
    layout: 'default'
  }
})

const route = useRoute()
const { t } = useI18n()

const errorMessage = computed(() => route.query.message)

const title = computed(() => {
  switch (errorMessage.value) {
    case 'no_access':
      return t('households.error.no_access.title')
    default:
      return t('households.error.unknown_error.title')
  }
})

const text = computed(() => {
  switch (errorMessage.value) {
    case 'no_access':
      return t(`households.error.no_access.text`)
    default:
      return t('households.error.unknown_error.text')
  }
})
</script>

<style scoped></style>
