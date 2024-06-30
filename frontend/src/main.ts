import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import 'font-awesome/scss/font-awesome.scss'
import '@/global.scss'
import "vue-toastification/dist/index.css";
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'
import {applyStorage} from "axios-jwt/src/applyStorage.ts";
import {getAccessToken, getBrowserLocalStorage} from "axios-jwt";

applyStorage(getBrowserLocalStorage())
import {createApp, markRaw} from 'vue'

import App from './App.vue'
import VueSidebarMenu from 'vue-sidebar-menu'

import {router} from "./router";
import {i18n} from "./lang";
import Toast, {POSITION} from "vue-toastification";
import {library} from "@fortawesome/fontawesome-svg-core";
import {fas} from "@fortawesome/free-solid-svg-icons";
import {far} from "@fortawesome/free-regular-svg-icons";
import {fab} from "@fortawesome/free-brands-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import VueVirtualScroller from "vue-virtual-scroller"




import pinia, {useAuthStore, useConfigStore, useGeneralSocketStore} from "@/store";
import FloatingVue from 'floating-vue'
import Notifications from '@kyvg/vue3-notification'

import vuetify from "@/plugins/vuetify.ts";

import {TinyEmitter} from "tiny-emitter";

import QrcodeVue from "qrcode.vue";
import vueQr from 'vue-qr/src/packages/vue-qr.vue'
import VueCountdown from '@chenfengyuan/vue-countdown';
import { SWhatsApp, STelegram, SEmail} from 'vue-socials';


// TODO OPTION TO DISABLE REGISTER AND INVITE USERS
// TODO ADMINISTRATION ROUTE

const app = createApp(App)


pinia.use(({store}) => {
    store.$router = markRaw(router)

})
const toastOptions = {
    // You can set your default options here
    position: POSITION.TOP_RIGHT,
    closeOnClick: true,
    pauseOnFocusLoss: false,
    pauseOnHover: true,
    draggable: true,
    showCloseButtonOnHover: false,
    closeButton: false,
    maxToasts: 5,
    newestOnTop: true,
    transition: "Vue-Toastification__fade",
};


library.add(fas, far, fab);
app.component('font-awesome-icon', FontAwesomeIcon);
app.component('qrcode-vue', QrcodeVue)
app.component('vue-qr', vueQr)

app.component("vue-countdown", VueCountdown);

app.component('SWhatsApp', SWhatsApp)
app.component('STelegram', STelegram)
app.component('SEmail', SEmail)



app.use(VueVirtualScroller)
app.use(FloatingVue)
app.use(Notifications)

app.use(pinia)

// TODO THE PROBLEM WITH AWAIT GETACCESSTOKEN IS THE REGISTRATION OF THE AXIOS INSTANCE ... IT WOULD BE BEST TO HAVE A GLOBAL AXIOS INSTANCE
// THATS CREATED AT STARTUP AND THE use... ENDPOINTS ONLY USE THIS GLOBAL INSTANCE INTERNALLY 
const authStore = useAuthStore()

const configStore= useConfigStore()
configStore.init()



app.use(vuetify)
let emitter = new TinyEmitter()
app.config.globalProperties.$emitter = emitter


app.use(i18n);
app.use(VueSidebarMenu)
app.use(Toast, toastOptions)

// let auth store initialization finish before loading router

authStore.init().then(() => {
    app.use(router)
    app.mount('#app')
})
