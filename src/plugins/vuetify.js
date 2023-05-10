// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import '@fortawesome/fontawesome-free/css/all.css'

// Vuetify
import { createVuetify } from 'vuetify'
import {  fa } from 'vuetify/iconsets/fa'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            fa,
            mdi,
        },
    },
})
