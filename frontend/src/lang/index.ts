import { createI18n } from 'vue-i18n'
import en from './messages/en.json'
import de from './messages/de.json'
import it from './messages/it.json'

import {
  en as vuetifyEn,
  de as vuetifyDe,
  it as vuetifyIt
} from 'vuetify/locale'

export const i18n = createI18n({
  legacy: false,
  locale: getBrowserOrDefault(),
  fallbackLocale: 'en',
  messages: {
    en: {
      ...en,
      $vuetify: {
        ...vuetifyEn
      }
    },
    de: {
      ...de,
      $vuetify: {
        ...vuetifyDe
      }
    },
    it: {
      ...it,
      $vuetify: {
        ...vuetifyIt
      }
    }
  },
  datetimeFormats: {
    en: {
      short: {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      },
      longer: {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: false
      }
    }
  }
})

function getBrowserOrDefault() {
  const browserLanguage = (navigator.language ?? 'en').split('-')[0]
  console.log(browserLanguage)
  return browserLanguage
}

// TODO: https://vue-i18n.intlify.dev/guide/advanced/lazy
export function setLanguage(locale: string) {
  if (locale === 'default') {
    locale = getBrowserOrDefault()
  }
  i18n.global.locale.value = locale
}
