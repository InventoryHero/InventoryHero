import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
import VueCountdown from '@chenfengyuan/vue-countdown'
import { SWhatsApp, STelegram, SEmail } from 'vue-socials'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

const app = createApp(App)

app.component('vue-countdown', VueCountdown)
app.component('SWhatsApp', SWhatsApp)
app.component('STelegram', STelegram)
app.component('SEmail', SEmail)

await registerPlugins(app)

app.mount('#app')
