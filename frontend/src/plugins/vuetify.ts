import {createVuetify} from "vuetify";
import 'vuetify/styles'
//@ts-expect-error colors are there but they are not properly found
import colors from 'vuetify/lib/util/colors'
import '@fortawesome/fontawesome-free/css/all.css'
import '@mdi/font/css/materialdesignicons.css'
import { fa } from 'vuetify/iconsets/fa'
import {aliases, mdi} from "vuetify/iconsets/mdi";
import * as labsComponents from 'vuetify/labs/components'
import * as components from 'vuetify/components'
import useGenerateMaterialYouTheme from "@/composables/useGenerateMaterialYouTheme.ts";


const defaultTheme = useGenerateMaterialYouTheme(colors.blue.base)

export default createVuetify({
    components: {
      ...components,
      ...labsComponents
    },
    theme : {
        defaultTheme: "dark",
        themes: defaultTheme,
    },
    icons: {
        aliases,
        sets: {
            mdi,
            fa,
        },
    },
})
