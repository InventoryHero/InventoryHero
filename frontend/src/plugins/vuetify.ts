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

export default createVuetify({
    components: {
      ...components,
      ...labsComponents
    },
    theme : {
        defaultTheme: "dark",
        themes: {
            light: {
                colors: {
                    background: '#eeefe6',
                    surface: '#f9faf1',
                    'surface-dim': '#dadbd2',
                    'surface-bright': '#f9faf1',
                    'on-surface': '#1a1c17',
                    outline: '#73796c',
                    'outline-variant': '#c3c9ba',
                    primary: '#40682c',
                    'on-primary': '#ffffff',
                    secondary: '#954648',
                    'on-secondary': '#ffffff',
                    tertiary: '#336097',
                    'on-tertiary': '#ffffff',
                    error: '#ba1a1a',
                    'on-error': '#ffffff',
                    'surface-light': '#e8e9e0',
                },
                dark: false,
                variables: {
                    'overlay-background': '#181d14',
                },
            },
            dark: {
                colors: {
                    background: '#1e201b',
                    surface: '#12140f',
                    'surface-dim': '#12140f',
                    'surface-bright': '#383a34',
                    'on-surface': '#e2e3db',
                    outline: '#8d9385',
                    'outline-variant': '#43493d',
                    primary: '#a5d48a',
                    'on-primary': '#113801',
                    secondary: '#ffb3b2',
                    'on-secondary': '#5a191d',
                    tertiary: '#a4c8ff',
                    'on-tertiary': '#00315e',
                    error: '#ffb4ab',
                    'on-error': '#690005',
                    'surface-light': '#383a34',
                },
                dark: true,
                variables: {
                    'overlay-background': '#181d14',
                },
            },
        },
    },
    icons: {
        aliases,
        sets: {
            mdi,
            fa,
        },
    },
})
