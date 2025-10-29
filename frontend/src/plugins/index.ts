/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from './vuetify'
import pinia from '../stores'
import router from '../router'

import Notifications from '@kyvg/vue3-notification'
import {VueQrcodeReader} from "vue-qrcode-reader";

import { i18n, setI18nLanguage } from './i18n'

// Types
import type { App } from 'vue'

export async function registerPlugins(app: App) {

  const configStore = useConfigStore()

  setI18nLanguage(configStore.language)

  pinia.use(({store}) => {
    store.$router = markRaw(router)
    store.vuetify = markRaw(vuetify)
    //@ts-expect-error don't know how to type this
    store.i18n = markRaw(i18n)

})
  app.use(vuetify).use(router).use(pinia).use(i18n).use(Notifications).use(VueQrcodeReader)
}
