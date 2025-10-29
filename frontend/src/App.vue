<script setup lang="ts">
import { setLanguage } from '@/lang'
import useAuthStore from '@/store/useAuthStore'
import useConfigStore from '@/store/useConfigStore.ts'
import { storeToRefs } from 'pinia'
import { useTheme } from 'vuetify'

const route = useRoute()
const router = useRouter()
const configStore = useConfigStore()
const authStore = useAuthStore()
const { t } = useI18n()
const { config } = useAxios()
const vuetifyTheme = useTheme()

const { theme, language } = storeToRefs(configStore)

const { authorized } = storeToRefs(authStore)
const isInitialized = ref(false)

vuetifyTheme.change(theme.value)
configStore.applyColor()
//setLanguage(language.value)

async function initializeApp() {
  try {
    const { success, data, error } = await config.getConfig()

    if (!success) {
      // TODO this is sadly unrecoverable
    }
    configStore.smtpEnabled = data?.smtp_enabled ?? false
    configStore.registrationAllowed = data?.registration_allowed ?? false
    await router.isReady()
    await authStore.init()
    if (authorized.value) {
      // TODO CONNECT TO SOCKETS
    }
  } catch (error) {
    console.error('Failed to initialize application:', error)
    // Handle initialization error, maybe redirect to an error page
  } finally {
    // Once everything is done (or has failed), flip the switch to render the app.
    isInitialized.value = true
  }
}

onBeforeMount(() => {
  initializeApp()
})
</script>

<template>
  <router-view v-if="isInitialized" />
  <v-app v-else>
    <v-main>
      <v-container
        fluid
        class="fill-height"
      >
        <v-row justify="center">
          <v-col
            cols="12"
            md="10"
            lg="8"
            class="pb-16"
          >
            <v-card class="fill-width">
              <template v-slot:loader>
                <v-progress-linear
                  indeterminate
                  active
                  color="primary"
                />
              </template>
              <template v-slot:text>
                <span class="d-flex justify-center">
                  {{ t('app.loading_content') }}
                </span>
              </template>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped lang="scss"></style>
