import { createVuetify } from 'vuetify'
import 'vuetify/styles'
//@ts-expect-error colors are there but they are not properly found
import colors from 'vuetify/lib/util/colors'
import '@mdi/font/css/materialdesignicons.css'
import * as labsComponents from 'vuetify/labs/components'
import * as components from 'vuetify/components'
import { createVueI18nAdapter } from 'vuetify/locale/adapters/vue-i18n'
import useGenerateMaterialYouTheme from '@/composables/useGenerateMaterialYouTheme.ts'
import { i18n } from './i18n'

const defaultTheme = useGenerateMaterialYouTheme(colors.blue.base)

export default createVuetify({
  components: {
    ...components,
    ...labsComponents
  },
  theme: {
    defaultTheme: 'system',
    themes: defaultTheme
  },
  locale: {
    adapter: createVueI18nAdapter({ i18n, useI18n })
  }
})
