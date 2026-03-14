import { createI18n } from 'vue-i18n'
import * as vuetifyLocales from 'vuetify/locale'
import en from '../locales/en.json'

// THESE MUST MATCH THE LOCALE.JSON FILES PRESENT in 'locales'
export const SUPPORT_LOCALES = ['en', 'de', 'it']

export const i18n = createI18n({
  legacy: false,
  locale: getBrowserOrDefault(),
  fallbackLocale: 'en',
  // english needs to be always available
  messages: {
    en: {
      ...en,
      $vuetify: {
        ...vuetifyLocales.en
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

  if (!SUPPORT_LOCALES.includes(browserLanguage)) {
    return 'en'
  }

  return browserLanguage
}

export async function setI18nLanguage(locale: string) {
  if (locale === 'default') {
    locale = getBrowserOrDefault()
  }

  //@ts-expect-error there are more available locales than 'en', but 'en' is the only one i18n recognises due to lazy loading
  if (!i18n.global.availableLocales.includes(locale)) {
    // load locale messages with dynamic import
    // maybe fetch these from the backend?
    const messages = await import(
      /* webpackChunkName: "locale-[request]" */ `@/locales/${locale}.json`
    )
    i18n.global.setLocaleMessage(locale, {
      $vuetify: {
        ...(vuetifyLocales[locale] ?? {})
      },
      ...messages.default
    })
  }

  // after loading we can set the locale
  //@ts-expect-error this is fine, even if we set an unknown locale, it should fallback to english
  i18n.global.locale.value = locale
  document.querySelector('html').setAttribute('lang', locale)
  const { api } = useAxios()
  api.defaults.headers.common['Accept-Language'] = locale

  return nextTick()
}
