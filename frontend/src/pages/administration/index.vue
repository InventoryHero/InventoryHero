<template>
  <test-email-dialog v-model:active="testMailDialog" />
  <v-skeleton-loader v-if="loading" />
  <template v-else>
    <div class="text-high-emphasis">
      {{ t('configuration.title') }}
    </div>
    <v-divider class="mt-2" />
    <v-list>
      <v-list-item
        :title="t('configuration.app_version')"
        :subtitle="appConfig?.app_version"
      >
        <template v-slot:prepend>
          <v-icon
            size="x-large"
            v-bind="appVersionIcon"
          />
        </template>
      </v-list-item>
      <v-divider class="mt-2 mb-2" />
      <v-list-item
        :title="t('configuration.base_url')"
        :subtitle="appConfig?.base_url"
      >
        <template v-slot:prepend>
          <v-icon
            v-tooltip:top="appUrlTooltip"
            size="x-large"
            :icon="
              appConfig?.base_url_default
                ? 'mdi-alert-circle'
                : 'mdi-check-circle'
            "
            :color="appConfig?.base_url_default ? 'warning' : 'success'"
          />
        </template>
      </v-list-item>
      <v-divider class="mb-2 mt-2" />
      <v-list-item
        :title="t('configuration.registration_allowed')"
        :subtitle="appConfig?.registration_allowed ?? false"
      >
        <template v-slot:prepend>
          <v-icon
            size="x-large"
            icon="mdi-pencil-circle"
          />
        </template>
      </v-list-item>
      <v-divider class="mb-2 mt-2" />
      <v-list-item
        :title="t('configuration.smtp_enabled')"
        :subtitle="appConfig?.smtp_enabled"
      >
        <template v-slot:prepend>
          <v-icon
            :icon="
              appConfig?.smtp_enabled ? 'mdi-check-circle' : 'mdi-alert-circle'
            "
            :color="appConfig?.smtp_enabled ? 'success' : 'warning'"
            size="x-large"
            v-tooltip:top="appConfigSmtpTooltip"
          />
        </template>
        <template v-slot:append>
          <v-btn
            v-bind="btnStyle"
            prepend-icon="mdi-email"
            :text="t('configuration.send_test_email')"
            :disabled="!appConfig?.smtp_enabled"
            @click="testMailDialog = true"
          />
        </template>
      </v-list-item>
      <v-divider class="mt-2 mb-2" />
      <v-list-item :title="t('configuration.database')">
        <v-list-item-subtitle>
          {{ appConfig?.database_type }}
        </v-list-item-subtitle>
        <v-list-item-subtitle>
          {{ appConfig?.database_connection }}
        </v-list-item-subtitle>
        <template v-slot:prepend>
          <v-icon icon="mdi-database" />
        </template>
      </v-list-item>
    </v-list>
  </template>
</template>

<script setup lang="ts">
import { AppConfig } from '@/api/types/config'

definePage({
  meta: {
    requiresAuth: true,
    requiresAdmin: true,
    requiresHousehold: false,
    layout: 'admin'
  }
})

const { t } = useI18n()
const { admin } = useAxios()
const router = useRouter()
const { btnStyle } = useAppStyling()

const loading = ref<boolean>(true)
const appConfig = ref<AppConfig>()
const testMailDialog = ref<boolean>(false)

const appVersionIcon = computed(() => {
  // todo change if not most recent
  return {
    icon: 'mdi-check-circle',
    color: 'success'
  }
})

const appUrlTooltip = computed(() => {
  if (!appConfig.value?.base_url_default) {
    return {
      text: '',
      openOnClick: false,
      openOnHover: false
    }
  }
  return {
    text: t('configuration.base_url_is_default'),
    openOnClick: true,
    openOnHover: true,
    persistent: false
  }
})

const appConfigSmtpTooltip = computed(() => {
  if (appConfig.value?.smtp_enabled) {
    return {
      text: '',
      openOnClick: false,
      openOnHover: false
    }
  }
  return {
    text: t('configuration.smtp_not_set_or_invalid'),
    openOnClick: true,
    openOnHover: true,
    persistent: false
  }
})

onBeforeMount(async () => {
  loading.value = true
  const { success, data } = await admin.getAppConfig()
  if (!success) {
    await router.push('/')
    return
  }
  appConfig.value = data!
  loading.value = false
})
</script>

<style scoped lang="scss"></style>
