// import css
import '@/global.scss'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'


// import components
import {createApp, markRaw} from 'vue'
import VueVirtualScroller from "vue-virtual-scroller"
// TODO MAYBE THIS PACKAGE CAN BE REMOVED
import FloatingVue from 'floating-vue'
import Notifications from '@kyvg/vue3-notification'
import vueQr from 'vue-qr/src/packages/vue-qr.vue'
import VueCountdown from '@chenfengyuan/vue-countdown';
import { SWhatsApp, STelegram, SEmail} from 'vue-socials';


import vuetify from "@/plugins/vuetify.ts";
import router from '@/router'
import {i18n} from "@/lang"
import pinia from "@/store";

import App from './App.vue'

const app = createApp(App)

pinia.use(({store}) => {
    store.$router = markRaw(router)
    store.vuetify = markRaw(vuetify)
    store.i18n = markRaw(i18n)

})

app.component('vue-qr', vueQr)
app.component("vue-countdown", VueCountdown);
app.component('SWhatsApp', SWhatsApp)
app.component('STelegram', STelegram)
app.component('SEmail', SEmail)
app.use(VueVirtualScroller)
app.use(FloatingVue)
app.use(Notifications)

app.use(pinia)
app.use(vuetify)
app.use(i18n)
app.use(router)
app.mount('#app')

