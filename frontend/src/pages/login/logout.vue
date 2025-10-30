<script setup lang="ts">
import { setI18nLanguage } from '@/plugins/i18n'
import useAuthStore from '@/stores/useAuthStore'
import useConfigStore from '@/stores/useConfigStore'
import { useTheme } from 'vuetify'

const authStore = useAuthStore()
const configStore = useConfigStore()
const { t } = useI18n()
const router = useRouter()
const theme = useTheme()

onMounted(async () => {
  await authStore.logout()
  configStore.reset()
  setI18nLanguage(configStore.language)
  configStore.applyColor()
  theme.change(configStore.theme)
  router.push('/login')
})
</script>

<template>
  <v-row
    justify="center"
    class="fill-height align-content-center"
  >
    <v-col
      cols="8"
      lg="8"
      class="fill-height"
    >
      <div class="d-flex flex-column justify-center align-center pt-16">
        <v-progress-circular
          width="10"
          size="140"
          indeterminate
          color="primary"
          class="mt-2"
        />
        <span class="mt-2">
          {{ t('logging_out') }}
        </span>
      </div>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss"></style>

<route>
{
  "path": "/logout",
  "meta": {
    "requiresHousehold": false,
    "requiresAuth": true,
    "allowUnauthorized": false
  }
}
</route>
