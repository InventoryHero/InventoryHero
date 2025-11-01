<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore'
import useConfigStore from '@/stores/useConfigStore'
import { storeToRefs } from 'pinia'
import { useTheme } from 'vuetify'
import { setI18nLanguage } from './plugins/i18n'

const router = useRouter()
const configStore = useConfigStore()
const authStore = useAuthStore()
const { t } = useI18n()
const { config } = useAxios()
const vuetifyTheme = useTheme()

const { theme, language, smtpEnabled, registrationAllowed } =
  storeToRefs(configStore)

const { authorized } = storeToRefs(authStore)

const initialized = ref<boolean>(false)

async function initializeApp() {
  try {
    await setI18nLanguage(language.value)

    vuetifyTheme.change(theme.value)
    configStore.applyColor()
    const { success, data, error } = await config.getConfig()
    if (!success) {
      // TODO this is sadly unrecoverable
      // maybe redirect to error view?
      return
    }
    smtpEnabled.value = data?.smtp_enabled ?? false
    registrationAllowed.value = data?.registration_allowed ?? false
    await router.isReady()
    if (authorized.value) {
      await authStore.whoami()
      // TODO CONNECT TO SOCKETS
    }

    initialized.value = true
  } catch (error) {
    console.error('Failed to initialize application:', error)
    // Handle initialization error, maybe redirect to an error page
  }
}

onBeforeMount(() => {
  initializeApp()
})
</script>

<template>
  <router-view v-if="initialized" />
</template>

<style scoped lang="scss"></style>
