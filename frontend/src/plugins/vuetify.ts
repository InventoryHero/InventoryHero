import {createVuetify} from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import colors from 'vuetify/lib/util/colors'
import '@fortawesome/fontawesome-free/css/all.css'
import { fa } from 'vuetify/iconsets/fa'
import {aliases, mdi} from "vuetify/iconsets/mdi";

export default createVuetify({
    components,
    directives,
    theme : {
        defaultTheme: "dark",
        themes: {
            dark: {
                dark: true,
                colors: {
                    primary: colors.blue.base,
                    'primary-offset': colors.blue.base,
                    secondary: '#888888', // colors.grey.darken1,
                    accent: colors.blue.accent2,
                    'card-heading': '#333337',
                    btncolor: '#4A4A4F',
                    drawer: '#28282B',
                    appbar: '#1E1E20',
                    logo: colors.blue.base
                }
            },
            light: {
                dark: false,
                colors: {
                    primary: colors.blue.darken2,
                    'primary-offset': colors.blue.darken2,
                    secondary: colors.grey.lighten1,
                    accent: colors.blue.accent2,
                    'card-heading': '#E9E9E9',
                    btncolor: '#E9E9E9',
                    drawer: '#F4F4F4',
                    appbar: '#FFFFFF',
                    logo: colors.blue.darken2
                }
            }
        }

    },
    icons: {
        aliases,
        sets: {
            mdi,
            fa,
        },
    },
})
