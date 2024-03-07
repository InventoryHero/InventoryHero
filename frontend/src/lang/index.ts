import {createI18n} from "vue-i18n";
import en from "./en.json";
import de from "./de.json";
import it from "./it.json";

export const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: en,
    de: de,
    it: it
  },
  datetimeFormats: {
    en: {
      short: {
        year: 'numeric', month:'short', day: 'numeric'
      },
      longer:{
        year: 'numeric', month: 'numeric', day: 'numeric',
        hour: 'numeric', minute: 'numeric', hour12: false
      }
    }
  }
})