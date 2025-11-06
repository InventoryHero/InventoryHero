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

const {
  theme,
  language,
  smtpEnabled,
  registrationAllowed,
  oidcEnabled,
  oidcName
} = storeToRefs(configStore)

const { authorized } = storeToRefs(authStore)

const initialized = ref<boolean>(false)
const initializeFailed = ref<boolean>(false)

const transition = computed(() => {
  if (configStore.useTransitions) {
    return {
      name: 'layout-fade-scale',
      mode: 'out-in'
    }
  }
  return {
    name: '',
    mode: ''
  }
})

async function initializeApp() {
  try {
    await setI18nLanguage(language.value)

    vuetifyTheme.change(theme.value)
    configStore.applyColor()
    const { success, data, error } = await config.getConfig()
    if (!success) {
      initializeFailed.value = true
      return
    }
    smtpEnabled.value = data?.smtp_enabled ?? false
    registrationAllowed.value = data?.registration_allowed ?? false
    oidcEnabled.value = data?.oidc_enabled ?? false
    oidcName.value = data?.oidc_name ?? 'SSO'
    await router.isReady()
    if (authorized.value) {
      await authStore.whoami()
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
  <router-view
    v-if="initialized && !initializeFailed"
    v-slot="{ Component, route }"
  >
    <transition v-bind="transition">
      <component
        :is="Component"
        :key="route.meta.layout"
      />
    </transition>
  </router-view>
  <template v-else-if="!initialized"></template>

  <template v-else-if="initializeFailed">
    <!-- TODO display something here-->
  </template>
</template>

<style scoped lang="scss">
.layout-fade-scale-enter-active,
.layout-fade-scale-leave-active {
  transition:
    opacity 0.4s ease,
    transform 0.45s cubic-bezier(0.25, 1, 0.5, 1);
  transform-origin: center center;
}

.layout-fade-scale-enter-from {
  opacity: 0;
  transform: scale(0.98);
}
.layout-fade-scale-leave-to {
  opacity: 0;
  transform: scale(1.02);
}
</style>
