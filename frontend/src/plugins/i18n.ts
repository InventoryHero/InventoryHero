import { createI18n } from 'vue-i18n'
import en from '../locales/en.json'
import de from '../locales/de.json'
import it from '../locales/it.json'

import {
  en as vuetifyEn,
  de as vuetifyDe,
  it as vuetifyIt
} from 'vuetify/locale'

/*
export const SUPPORT_LOCALES = ['en', 'de'] as const
export type Locales = (typeof SUPPORT_LOCALES)[number]
const messageSchema = {
  $vuetify: {
    ...vuetifyEn
  },
  ...en
}
type MessageSchema = typeof messageSchema
*/
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
  return browserLanguage
}

// TODO: https://vue-i18n.intlify.dev/guide/advanced/lazy
export /*async*/ function setI18nLanguage(locale: string) {
  if (locale === 'default') {
    locale = getBrowserOrDefault()
  }
  i18n.global.locale.value = locale
  //const { axiosInstance } = useAxios()
  //axiosInstance.defaults.headers.common['Accept-Language'] = locale

  // load locale messages with dynamic import
  // TODO FETCH VUETIFY
  //const messages = await import(
  ///* webpackChunkName: "locale-[request]" */ `@/locales/${locale}.json`
  //)

  /*i18n.global.setLocaleMessage(locale, {
    $vuetify: {
      ...vuetifyEn
    },
    ...messages.default
  })*/

  return nextTick()
}
