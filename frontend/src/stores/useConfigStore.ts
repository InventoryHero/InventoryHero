import { defineStore } from 'pinia'
import { useLocalStorage } from '@vueuse/core'

export type Theme = 'dark' | 'system' | 'light'

export default defineStore('config', {
  state: () => ({
    theme: useLocalStorage('theme', 'system'),
    color: useLocalStorage('color', '#2196f3'),
    useTransitions: useLocalStorage('transitions', true),
    language: useLocalStorage('language', 'default'),
    smtpEnabled: false,
    registrationAllowed: false
  }),

  actions: {
    applyColor() {
      const newThemes = useGenerateMaterialYouTheme(this.color)
      this.vuetify.theme.themes.value.light.colors = newThemes.light.colors
      this.vuetify.theme.themes.value.dark.colors = newThemes.dark.colors
    },
    reset() {
      this.language = 'default'
      this.useTransitions = true
      this.theme = 'system'
      this.color = '#2196f3'
    }
  }
})
