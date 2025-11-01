// src/stores/configStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import vuetify from '@/plugins/vuetify'

export type Theme = 'dark' | 'system' | 'light'

export default defineStore('config', () => {
  // --- State ---
  const theme = useLocalStorage<Theme>('theme', 'system')
  const color = useLocalStorage<string>('color', '#2196f3')
  const useTransitions = useLocalStorage<boolean>('transitions', true)
  const language = useLocalStorage<string>('language', 'default')
  const smtpEnabled = ref<boolean>(false)
  const registrationAllowed = ref<boolean>(false)

  // --- Actions ---
  function applyColor() {
    const newThemes = useGenerateMaterialYouTheme(color.value)
    // Assuming Vuetify instance is globally accessible
    vuetify.theme.themes.value.light.colors = newThemes.light.colors
    vuetify.theme.themes.value.dark.colors = newThemes.dark.colors
  }

  function reset() {
    language.value = 'default'
    useTransitions.value = true
    theme.value = 'system'
    color.value = '#2196f3'
  }

  // --- Expose to consumers ---
  return {
    theme,
    color,
    useTransitions,
    language,
    smtpEnabled,
    registrationAllowed,
    applyColor,
    reset
  }
})
