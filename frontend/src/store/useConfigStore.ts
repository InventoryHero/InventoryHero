import { defineStore } from 'pinia'
import { useLocalStorage } from '@vueuse/core'
import { useTheme } from 'vuetify/lib/composables/theme.mjs'

export type Theme = 'dark' | 'system' | 'light'

export default defineStore('config', {
  state: () => ({
    initialized: false,
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
      this.theme = 'system'
      this.color = '#2196f3'
    }
    /*toggleTransitions(useTransitions: boolean) {
      this.config.useTransitions = useTransitions
    },
    setColor(color: string) {
      this.config.color = color
      const newThemes = useGenerateMaterialYouTheme(color)
      this.vuetify.theme.themes.value.light.colors = newThemes.light.colors
      this.vuetify.theme.themes.value.dark.colors = newThemes.dark.colors
    },
    reset() {
      // TODO LOAD CONFIG FROM config.json
      this.setColor('#2196f3')
      this.config.useTransitions = true
    },*/
    /*languageChange(newLanguage: string) {
      if (newLanguage === 'default') {
        this.config.language = 'default'
        //@ts-expect-error - I really couldn't figure out how to type newLanguage to not trigger an error
        this.i18n.global.locale = navigator.language || navigator.userLanguage
        return
      }
      if (this.i18n.global.availableLocales.includes(newLanguage)) {
        this.config.language = newLanguage
        this.i18n.global.locale = this.config.language
      }
    },
    init() {
      this.setColor(this.config.color)
      this.languageChange(this.config.language)
      this.initialized = true
    }*/
  }
})
